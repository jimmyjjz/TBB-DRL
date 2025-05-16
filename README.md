# Deep Reinforcement Learning Applied to Terraria Boss Battles
### Introduction
This project utilizes PPO(proximal policy optimization) to train an agent to defeat Terraria bosses. The agent learns via screencapture inputs and rewards off of ingame damage(taken and dealt accordingly), therefore possesses supreme adaptivity. This allows training on any Terraria boss no matter if it is worm-type(eater of worlds), segmented(skeletron), or singular(eye of cthulu) without any code changes. Thus, can be used with ease to explore possible play styles with different ingame equipment or for playtesting with different levels of competency against different bosses.

### Setup
**Note: must have access to tModloader and Terraria**

First things first, Clone the repo.

Setup Gameside Training Mod:
1. Make a tModloader mod skeleton
2. Navigate to the folder of the mod skeleton you have created in the previous step and copy the contents of TBBTrainingMod_core into that folder(just copy paste and click replace files)
3. Replace "...\\settings.json" in line 8 of [SettingsAccesser](https://github.com/jimmyjjz/TBB-DRL/blob/main/TBBTrainingMod_core/SettingsAccesser.cs) with the path of [settings.json](https://github.com/jimmyjjz/TBB-DRL/blob/main/DRL_component/settings.json)

Setup Deep Reinforcement Learning:
1. Replace "...\\reward_accumulant.txt" of [settings.json](https://github.com/jimmyjjz/TBB-DRL/blob/main/DRL_component/settings.json) with the path of [reward_accumulant](https://github.com/jimmyjjz/TBB-DRL/blob/main/DRL_component/reward_accumulant.txt).txt
2. [Install python 3.11](https://www.python.org/downloads/release/python-3110/)
3. Install dependencies
```
pip install numpy==1.26.4 pillow==11.2.1 gymnasium==1.0.0 dxcam==0.0.5 pydirectinput==1.0.4 stable-baselines3==2.6.0
```

### How to Train and Run a Model
Run [train_model.py](https://github.com/jimmyjjz/TBB-DRL/blob/main/DRL_component/run_model.py) to train. Run [run_model.py](https://github.com/jimmyjjz/TBB-DRL/blob/main/DRL_component/run_model.py) to run. Make sure when running, an existing checkpoint is attempted to be used via [settings.json](https://github.com/jimmyjjz/TBB-DRL/blob/main/DRL_component/settings.json).

### Misc
While training and running works in whatever Terraria terrain, just in case you want a good orthrodox boss battle arena, one is provided [TBB-Environment World.wld](https://github.com/jimmyjjz/TBB-DRL/blob/main/TBB-Environment%20World.wld).

To play on this world just put [TBB-Environment World.wld](https://github.com/jimmyjjz/TBB-DRL/blob/main/TBB-Environment%20World.wld) into ...\\Terraria\\tModLoader\\Worlds