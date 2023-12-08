import torch.nn as nn
import torch
from pathlib import Path
from model import ACModel
from .textual_minigrid import gpt_skill_planning, llama_skill_planning, human_skill_planning
from .format import Vocabulary
from torch_ac.utils.dictlist import DictList
import torch_ac
from torch.distributions import Categorical
from .other import device


SKILL_MDL_PATH = [
    "storage/skill-model-v1/BabyAI-GoToObj-v0_ppo_Nollm_seed1_23-11-26-20-13-04",
    "storage/skill-model-v1/BabyAI-OpenDoor-v0_ppo_Nollm_seed1_23-11-26-20-38-31",
    "storage/skill-model-v1/BabyAI-PickupDist-v0_ppo_Nollm_seed1_23-11-26-21-02-46",
    "storage/skill-model-v1/BabyAI-PutNextLocalS5N3-v0_ppo_Nollm_seed1_23-11-26-22-15-24",
    "storage/skill-model-v1/BabyAI-UnlockLocal-v0_ppo_Nollm_seed2_23-11-27-03-01-30",
    "storage/skill-model-v1/BabyAI-FindObjS5-v0_ppo_Nollm_seed1_23-11-27-02-54-00",
    "storage/skill-model-v1/MiniGrid-FourRooms-v0_ppo_Nollm_seed1_23-11-27-04-41-55"
]

class PlannerPolicy(nn.Module, torch_ac.RecurrentACModel):
    '''ask_cooldown: how many steps to wait before asking GPT again. For synchronization.'''
    
    def __init__(self, obs_space, action_space, vocab, llm_variant, ask_cooldown, num_procs, use_memory=False, use_text=False, num_skills=7):
        super().__init__()
        # adapted from ACModel
        self.use_memory = use_memory
        self.use_text = use_text

        n = obs_space["image"][0]
        m = obs_space["image"][1]
        self.image_embedding_size = ((n-1)//2-2)*((m-1)//2-2)*64

        if self.use_text:
            self.word_embedding_size = 32
            self.text_embedding_size = 128

        self.embedding_size = self.semi_memory_size
        if self.use_text:
            self.embedding_size += self.text_embedding_size

        self.obs_space = obs_space
        self.action_space = action_space
        self.num_skills = num_skills
        self.ac_models = nn.ModuleList()
        self.timer = 0
        self.ask_cooldown = ask_cooldown
        self.num_envs = num_procs

        self.current_skills : list[int] = [0] * self.num_envs
        self.current_goals : list[int] = [None] * self.num_envs
        self.skill_vocabs : list[Vocabulary] = [None] * self.num_skills
        self.vocab : Vocabulary = vocab.vocab
        self.invert_vocab : dict = {v: k for k, v in self.vocab.items()}
        
        self.llm_variant = llm_variant
        # load skill mmodel 
        for i in range(num_skills):
            self.ac_models.append(self.load_model(i))

        # self.lock = threading.Lock()

    @property
    def memory_size(self):
        return 2 * self.semi_memory_size

    @property
    def semi_memory_size(self):
        return self.image_embedding_size

    def load_model(self, index):
        mdl = ACModel(self.obs_space, self.action_space, self.use_memory, self.use_text)
        p = Path(SKILL_MDL_PATH[index], "status.pt")
        with open(p, "rb") as f:
            status = torch.load(f)
            model_state = status['model_state']
        mdl.load_state_dict(model_state)
        vocab = Vocabulary(100)
        vocab.load_vocab(status['vocab'])
        self.skill_vocabs[index] = vocab
        for p in mdl.parameters():
            p.requires_grad = True
        return mdl

    def get_skills_and_goals(self, obs):
        '''
            Get the skill numbers and goals for an observation. Must ensure observation batch size is the same as the number of parallel environments
        '''
        # Here, we enforce that the batch size of this obs is the same as the number of parallel environments
        assert (obs.image.shape[0] == self.num_envs)
        assert (obs.text.shape[0] == self.num_envs)

        if self.timer == 0:

            # Iterate over batches
            for idx in range(obs.image.shape[0]):

                # Extract the individual image and mission texts
                obs_img : torch.Tensor = obs.image[idx]
                mission_txt = " ".join([self.invert_vocab[s.item()] for s in obs.text[idx]])
                print(f"Mission text sent is {mission_txt}")

                # Ask the LLM planner
                try:
                    if self.llm_variant == "gpt":
                        skill_num = gpt_skill_planning(obs_img.cpu().numpy(), mission_txt)
                    elif self.llm_variant == "llama":
                        skill_num = llama_skill_planning(obs_img.cpu().numpy(), mission_txt)
                    elif self.llm_variant == "human":
                        skill_num, goal_text = human_skill_planning()
                    print(f"Skill planning outcome: {skill_num}. Goal: {goal_text}")
                except Exception as e:
                    print(f"Planning failed with error {e}, using the old goal and current skill.")
                    return self.current_skills, self.current_goals

                # Store the skill numbers and goal tokens returned by the planner
                self.current_skills[idx] = skill_num

                goal_tokens = []
                for s in goal_text.split():
                    if s not in self.skill_vocabs[skill_num].vocab:
                        print(f"Warning: unknown word {s} in mission text {goal_text}")
                    goal_tokens.append(self.skill_vocabs[skill_num][s])
                goal_tokens = torch.IntTensor(goal_tokens).to(device)
                self.current_goals[idx] = goal_tokens
            self.timer = self.ask_cooldown
        else:
            self.timer -= 1
        return self.current_skills, self.current_goals

    def forward(self, obs : DictList, memory):
        # here, obs is a dictionary of batched images and batched text. The batch size is a integer multiple of the number of parallel environments.

        dist_logits, values, memories = [], [], []
        # In each iteration of this loop, we need to extract one step of observations from all parallel environments, and ask get_skill.
        for i in range(0, len(obs), self.num_envs):
            obs_one_step = obs[i:i + self.num_envs]
            current_skills, current_goals = self.get_skills_and_goals(obs_one_step)

            # Iterate over skill and goal token pairs
            # Need to gather the dist, value, and memory
            for j in range(self.num_envs):
                skill_num, goal = current_skills[j], current_goals[j]
                obs_one_step = obs_one_step[j:j + 1]
                memory_one_step = memory[i + j:i + j + 1]

                # Use the same image observation but change the goal
                new_obs = DictList({"image" : obs_one_step.image, "text" : goal.unsqueeze(0)})
                d, v, m = self.ac_models[skill_num](new_obs, memory_one_step)

                dist_logits.append(d.logits)
                values.append(v)
                memories.append(m)
            
        dist_logits = torch.cat(dist_logits)
        values = torch.cat(values)
        memories = torch.cat(memories)

        return Categorical(logits=dist_logits), values, memories


    
