# w. llm
# a2c
python3 -m scripts.train --algo a2c --env BabyAI-GoToImpUnlock-v0 --text --save-interval 10 --frames 250000 --use-trajectory --frames-per-proc 5 --gpt

# ppo
python3 -m scripts.train --algo ppo --env BabyAI-GoToImpUnlock-v0 --text --save-interval 10 --frames 250000 --use-trajectory --gpt


# w/o. llm
# a2c
python3 -m scripts.train --algo a2c --env BabyAI-GoToImpUnlock-v0 --text --save-interval 10 --frames 250000 --frames-per-proc 5

# ppo
python3 -m scripts.train --algo ppo --env BabyAI-GoToImpUnlock-v0 --text --save-interval 10 --frames 250000

MiniGrid-BlockedUnlockPickup-v0
MiniGrid-LavaCrossingS9N1-v0
MiniGrid-LavaCrossingS9N2-v0
MiniGrid-LavaCrossingS9N3-v0
MiniGrid-LavaCrossingS11N5-v0
MiniGrid-SimpleCrossingS9N1-v0
MiniGrid-DistShift1-v0
MiniGrid-DistShift2-v0
MiniGrid-DoorKey-5x5-v0
MiniGrid-DoorKey-6x6-v0
MiniGrid-DoorKey-8x8-v0
MiniGrid-DoorKey-16x16-v0
MiniGrid-Dynamic-Obstacles-5x5-v0
MiniGrid-Dynamic-Obstacles-Random-5x5-v0
MiniGrid-Dynamic-Obstacles-6x6-v0
MiniGrid-Dynamic-Obstacles-Random-6x6-v0
MiniGrid-Dynamic-Obstacles-8x8-v0
MiniGrid-Dynamic-Obstacles-16x16-v0
MiniGrid-Empty-5x5-v0
MiniGrid-Empty-Random-5x5-v0
MiniGrid-Empty-6x6-v0
MiniGrid-Empty-Random-6x6-v0
MiniGrid-Empty-8x8-v0
MiniGrid-Empty-16x16-v0
MiniGrid-Fetch-5x5-N2-v0
MiniGrid-Fetch-6x6-N2-v0
MiniGrid-Fetch-8x8-N3-v0
MiniGrid-FourRooms-v0
MiniGrid-GoToDoor-5x5-v0
MiniGrid-GoToDoor-6x6-v0
MiniGrid-GoToDoor-8x8-v0
MiniGrid-GoToObject-6x6-N2-v0
MiniGrid-GoToObject-8x8-N2-v0
MiniGrid-KeyCorridorS3R1-v0
MiniGrid-KeyCorridorS3R2-v0
MiniGrid-KeyCorridorS3R3-v0
MiniGrid-KeyCorridorS4R3-v0
MiniGrid-KeyCorridorS5R3-v0
MiniGrid-KeyCorridorS6R3-v0
MiniGrid-LavaGapS5-v0
MiniGrid-LavaGapS6-v0
MiniGrid-LavaGapS7-v0
MiniGrid-LockedRoom-v0
MiniGrid-MemoryS17Random-v0
MiniGrid-MemoryS13Random-v0
MiniGrid-MemoryS13-v0
MiniGrid-MemoryS11-v0
MiniGrid-MultiRoom-N2-S4-v0
MiniGrid-MultiRoom-N4-S5-v0
MiniGrid-MultiRoom-N6-v0
MiniGrid-ObstructedMaze-1Dlhb-v0
MiniGrid-ObstructedMaze-Full-v0
MiniGrid-Playground-v0
MiniGrid-PutNear-6x6-N2-v0
MiniGrid-PutNear-8x8-N3-v0
MiniGrid-RedBlueDoors-6x6-v0
MiniGrid-RedBlueDoors-8x8-v0
MiniGrid-Unlock-v0
MiniGrid-UnlockPickup-v0


# BabyAI
BabyAI-GoToRedBallGrey-v0
BabyAI-GoToRedBall-v0
BabyAI-GoToObj-v0
BabyAI-GoToObjS4-v0
BabyAI-GoToObjS6-v0
BabyAI-GoToLocal-v0
BabyAI-GoToLocalS5N2-v0
BabyAI-GoToLocalS6N2-v0
BabyAI-GoToLocalS6N3-v0
BabyAI-GoToLocalS6N4-v0
BabyAI-GoToLocalS7N4-v0
BabyAI-GoToLocalS7N5-v0
BabyAI-GoToLocalS8N2-v0
BabyAI-GoToLocalS8N3-v0
BabyAI-GoToLocalS8N4-v0
BabyAI-GoToLocalS8N5-v0
BabyAI-GoToLocalS8N6-v0
BabyAI-GoToLocalS8N7-v0
BabyAI-GoTo-v0
BabyAI-GoToOpen-v0
BabyAI-GoToObjMaze-v0
BabyAI-GoToObjMazeOpen-v0
BabyAI-GoToObjMazeS4R2-v0
BabyAI-GoToObjMazeS4-v0
BabyAI-GoToObjMazeS5-v0
BabyAI-GoToObjMazeS6-v0
BabyAI-GoToObjMazeS7-v0
BabyAI-GoToImpUnlock-v0
BabyAI-GoToSeq-v0
BabyAI-GoToSeqS5R2-v0
BabyAI-GoToRedBlueBall-v0
BabyAI-GoToDoor-v0
BabyAI-GoToObjDoor-v0
BabyAI-Open-v0
BabyAI-OpenRedDoor-v0
BabyAI-OpenDoor-v0
BabyAI-OpenDoorDebug-v0
BabyAI-OpenDoorColor-v0
BabyAI-OpenDoorLoc-v0
BabyAI-OpenTwoDoors-v0
BabyAI-OpenRedBlueDoors-v0
BabyAI-OpenRedBlueDoorsDebug-v0
BabyAI-OpenDoorsOrderN2-v0
BabyAI-OpenDoorsOrderN4-v0
BabyAI-OpenDoorsOrderN2Debug-v0
BabyAI-OpenDoorsOrderN4Debug-v0
BabyAI-Pickup-v0
BabyAI-UnblockPickup-v0
BabyAI-PickupLoc-v0
BabyAI-PickupDist-v0
BabyAI-PickupDistDebug-v0
BabyAI-PickupAbove-v0
BabyAI-PutNextLocal-v0
BabyAI-PutNextLocalS5N3-v0
BabyAI-PutNextLocalS6N4-v0
BabyAI-PutNextS4N1-v0
BabyAI-PutNextS5N2-v0
BabyAI-PutNextS5N1-v0
BabyAI-PutNextS6N3-v0
BabyAI-PutNextS7N4-v0
BabyAI-PutNextS5N2Carrying-v0
BabyAI-PutNextS6N3Carrying-v0
BabyAI-PutNextS7N4Carrying-v0
BabyAI-Unlock-v0
BabyAI-UnlockLocal-v0
BabyAI-UnlockLocalDist-v0
BabyAI-KeyInBox-v0
BabyAI-UnlockPickup-v0
BabyAI-UnlockPickupDist-v0
BabyAI-BlockedUnlockPickup-v0
BabyAI-UnlockToUnlock-v0
BabyAI-ActionObjDoor-v0
BabyAI-FindObjS5-v0
BabyAI-FindObjS6-v0
BabyAI-FindObjS7-v0
BabyAI-KeyCorridor-v0
BabyAI-KeyCorridorS3R1-v0
BabyAI-KeyCorridorS3R2-v0
BabyAI-KeyCorridorS3R3-v0
BabyAI-KeyCorridorS4R3-v0
BabyAI-KeyCorridorS5R3-v0
BabyAI-KeyCorridorS6R3-v0
BabyAI-OneRoomS8-v0
BabyAI-OneRoomS12-v0
BabyAI-OneRoomS16-v0
BabyAI-OneRoomS20-v0
BabyAI-MoveTwoAcrossS5N2-v0
BabyAI-MoveTwoAcrossS8N9-v0
BabyAI-Synth-v0
BabyAI-SynthS5R2-v0
BabyAI-SynthLoc-v0
BabyAI-SynthSeq-v0
BabyAI-MiniBossLevel-v0
BabyAI-BossLevel-v0
BabyAI-BossLevelNoUnlock-v0