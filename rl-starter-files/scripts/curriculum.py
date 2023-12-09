from envs.goto import goto_dict
from envs.open import open_dict
from envs.pickup import pickup_dict
from envs.putnext import putnext_dict

def get_curriculum(args):
    if args.skill == 'goto':
        return Curriculum(goto_dict, args.upgrade_threshold, args.downgrade_threshold, args.repeat_threshold)
    elif args.skill == 'open':
        return Curriculum(open_dict, args.upgrade_threshold, args.downgrade_threshold, args.repeat_threshold)
    elif args.skill == 'pickup':
        return Curriculum(pickup_dict, args.upgrade_threshold, args.downgrade_threshold, args.repeat_threshold)
    elif args.skill == 'putnext':
        return Curriculum(putnext_dict, args.upgrade_threshold, args.downgrade_threshold, args.repeat_threshold)
    else:
        raise NotImplementedError

class Curriculum:

    def __init__(self, env_dict, upgrade_threshold=0.6, downgrade_threshold=0.3, repeat_threshold=5):
        """Curriculum class for selecting environments and updating the difficulty.

        Args:
            env_dict (int->dict[name, envs]): Dictionary of levels and their environments.
            upgrade_threshold (float, optional): Defaults to 0.6.
            downgrade_threshold (float, optional): Defaults to 0.3.
        """
        self.env_dict = env_dict
        self.current_level = 0
        # thresholds
        self.upgrade_threshold = upgrade_threshold
        self.downgrade_threshold = downgrade_threshold
        self.repeated_threshold = repeat_threshold
        # env difficulty of current level
        self.env_idx = 0
        self.repeated = 0
        self.finished_levels = []
        self.if_new = False
        # highly not possible to flag this as finished
        self.if_finished = False

    def select_environment(self):
        """
        Selects an environment based on the current level.
        """
        self.if_new = False
        return self.env_dict[self.current_level]['envs'][self.env_idx]
    
    def if_new_env(self):
        return self.if_new

    def update_level(self, success_rate):
        """
        Updates the level and env difficulties based on the success rate.
        """
        # update difficulty
        if success_rate > self.upgrade_threshold and self.env_idx < len(self.env_dict[self.current_level]['envs']):
            self.env_idx += 1
            self.if_new = True
        elif success_rate < self.downgrade_threshold and self.env_idx > 0:
            self.env_idx -= 1
            self.if_new = True
        else:
            self.repeated += 1

        # update level
        if self.repeated > self.repeated_threshold:
            self.repeated = 0
            self.env_idx = 0
            self.current_level += 1
            self.current_level = self.current_level % len(self.env_dict.keys())
            self.if_new = True

        if self.env_idx >= len(self.env_dict[self.current_level]['envs']):
            self.finished_levels.append(self.current_level)
            self.repeated = 0
            self.env_idx = 0
            self.current_level += 1
            self.current_level = self.current_level % len(self.env_dict.keys())
            self.if_new = True

        # check if level is finished
        while self.current_level in self.finished_levels:
            self.current_level += 1
            self.current_level = self.current_level % len(self.env_dict.keys())
            self.if_new = True
        
        if len(self.finished_levels) == len(self.env_dict.keys()):
            self.if_finished = True


if __name__ == '__main__':
    from envs.goto import goto_dict
    curriculum = Curriculum(env_dict=goto_dict)
    for i in range(10):
        print(curriculum.select_environment())
        curriculum.update_level(0.5)
    print('-------------------')
    for i in range(10):
        print(curriculum.select_environment())
        curriculum.update_level(0.7)
    print('-------------------')
    for i in range(10):
        print(curriculum.select_environment())
        curriculum.update_level(0.1)