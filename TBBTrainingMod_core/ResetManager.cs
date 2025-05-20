using Terraria.ModLoader;
using Terraria;
using Terraria.GameInput;
using Microsoft.Xna.Framework;
using TBBTrainingMod;
using RewardManager;
using SettingsAccesser;
using System.Collections.Generic;
using System;

namespace ResetManager{
    public class Trigger : ModPlayer{
        public override void OnRespawn(){
            //replenish health and mana
            Player.statLife = Player.statLifeMax2;
            Player.statMana = Player.statManaMax2;
        }
        public override void ProcessTriggers(TriggersSet triggersSet){
            if (Keybinds.resetKeybind.JustPressed){
                //reset runaway punishing toggle
                RunAwayDisincentive.resetPunishing();
                //reset reward denoter
                RewardDenoterManager.resetRewardDenoter();
                //reset velocity
                Player.velocity = Vector2.Zero;
                //reset fall start
                Player.fallStart = (int)(Player.position.Y / 16f);
                //teleport
                Player.Teleport(new Vector2(SettingsOperations.get_int_value("player_initial_point_x"), SettingsOperations.get_int_value("player_initial_point_y")), 1);
                //if player is dead then player will immediately spawn at defined location
                Main.spawnTileX = (int)Player.position.X / 16;
                Main.spawnTileY = (int)Player.position.Y / 16;
                Player.respawnTimer = 0;
                //replenish health and mana
                Player.statLife = Player.statLifeMax2;
                Player.statMana = Player.statManaMax2;
                //inventory clear
                for (int i = 0; i < Player.inventory.Length; i++){
                    Player.inventory[i].TurnToAir();
                }
                //clear all buffs
                for (int i = Player.MaxBuffs - 1; i >= 0; i--){
                    Player.DelBuff(i);
                }
                //clear potion delay
                Player.potionDelay = 0;
                //hotbar setup
                List<Tuple<int, int>> items = SettingsOperations.get_loadout();
                for (int i = 0; i < items.Count; i++){
                    Player.inventory[i].SetDefaults(items[i].Item1);
                    Player.inventory[i].stack = items[i].Item2;
                }
                //makes all hostile mobs disappear(not killing)
                foreach (NPC npc in Main.npc){
                    if (npc.active && !npc.friendly && !npc.townNPC && !npc.dontTakeDamage){
                        npc.active = false;
                    }
                }
                //clear all items
                foreach (Item item in Main.item){
                    if (item.active){
                        item.TurnToAir();
                    }
                }
                //clear chat
                for (int i = 0; i < 10; i++){
                    Main.NewText(" ");
                }
                //summon boss
                NPC.NewNPC(
                    Entity.GetSource_FromThis(),
                    SettingsOperations.get_int_value("boss_initial_point_x"),
                    SettingsOperations.get_int_value("boss_initial_point_y"),
                    SettingsOperations.get_int_value("boss_id"),
                    Target: Main.myPlayer
                );
            }
            if (Keybinds.debugKeybind.JustPressed){
                Vector2 position = Player.position;
                Main.NewText($"Player Position: Pixels = ({position.X}, {position.Y})", 255, 255, 0);
                foreach (Item item in Main.item){
                    if (item.active){
                        item.TurnToAir();
                    }
                }
            }
        }
    }
}