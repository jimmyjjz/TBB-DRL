# Deep Reinforcement Learning Applied to Terraria Boss Battles
Introduction
This project utilizes PPO(proximal policy optimization) to train an agent to defeat Terraria bosses.

Installation

Note: must have access to tModloader and Terraria

First things first, Clone the repo.

Setup Gameside Training Mod
1. Make a tModloader mod skeleton
2. Navigate to the folder of the mod skeleton you have created in the previous step and copy the contents of TBBTrainingMod_core into that folder(just copy paste and select replace files)
3. Replace "...\\settings.json" in line 8 of SettingsAccesser with the path of settings.json(found in DRL_component folder)

Setup Deep Reinforcement Learning
1. Replace "...\\reward_accumulant.txt" of settings.json with the path of reward_accumulant.txt(found in DRL_component folder)
2. Install python 3.11
3. Install dependencies
##
<tab><tab>pip install numpy==1.26.4 pillow==11.2.1 gymnasium==1.0.0 dxcam==0.0.5 pydirectinput==1.0.4 stable-baselines3==2.6.0

How to Train and Run

Run train_model.py to train

Run run_model.py to run
Make sure when running an existing checkpoint is attempted to be used via settings.json