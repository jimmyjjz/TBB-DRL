using Terraria;
using Terraria.ModLoader;
using System;
using System.IO;
using SettingsAccesser;
using Terraria.DataStructures;

namespace RewardManager{
    public class DealDamageIncentive : ModPlayer{
        public override void OnHitNPC(NPC target, NPC.HitInfo hit, int damageDone){
            int boss_id = SettingsOperations.get_int_value("boss_id");
            if (target.type == boss_id){
                RewardDenoterManager.addReward(hit.Damage * SettingsOperations.get_int_value("attack_reward_factor"));
                bool finish = true;
                foreach (NPC npc in Main.npc){
                    if (npc.active && npc.type == boss_id){
                        finish = false;
                        break;
                    }
                }
                if (finish){
                    File.WriteAllText(SettingsOperations.get_string_value("reward_denoter_path"), "EInactive. Boss defeated.");
                }
                //Main.NewText($"Damage given: {hit.Damage}");
            }
        }
    }
    public class TakeDamageDisincentive : ModPlayer{
        public override void OnHurt(Player.HurtInfo info){
            if(!RewardDenoterManager.readRewardDenoter().Substring(1).Equals("Inactive. Boss defeated.")){
                RewardDenoterManager.addReward(-info.Damage * SettingsOperations.get_int_value("hurt_punishment_factor"));
                //Main.NewText($"Damage taken: {info.Damage}");
            }
        }
        public override void Kill(double damage, int hitDirection, bool pvp, PlayerDeathReason damageSource){
            File.WriteAllText(SettingsOperations.get_string_value("reward_denoter_path"), "EInactive. Player died.");
            //Main.NewText("Player died");
        }
    }
    public class RunAwayDisincentive : ModPlayer{
        public static bool punishing = false;
        public static void resetPunishing(){
            punishing = false;
        }
        public override void PostUpdate(){
            double px = Player.position.X;
            double py = Player.position.Y;
            bool punish = true, boss_exist = false;
            foreach (NPC npc in Main.npc){
                if (npc.active && npc.type == SettingsOperations.get_int_value("boss_id")){
                    boss_exist = true;
                    //Main.NewText(Math.Sqrt(Math.Pow(px - npc.position.X, 2) + Math.Pow(py - npc.position.Y, 2)));
                    if (Math.Sqrt(Math.Pow(px - npc.position.X, 2) + Math.Pow(py - npc.position.Y, 2)) < SettingsOperations.get_double_value("run_away_distance_threshold")){
                        punish = false;
                    }
                }
            }
            if (!punishing && boss_exist && punish && !Player.dead){
                punishing = true;
                //Main.NewText("rwp on");
                RewardDenoterManager.toggleDistancePunish();
            }
            else if(punishing && boss_exist && !punish && !Player.dead){
                punishing = false;
                //Main.NewText("rwp off");
                RewardDenoterManager.toggleDistancePunish();
            }
        }
    }
    // NTS: txt file over socket for simplicity
    public class RewardDenoterManager{
        public static string readRewardDenoter(){
            try{
                string content = File.ReadAllText(SettingsOperations.get_string_value("reward_denoter_path"));
                //Console.WriteLine($"Current reward denoter is {content}");
                return content;
            }
            catch (Exception e){
                Console.WriteLine($"txt reading error. {e.Message}");
            }
            return "Error";
        }
        public static void addReward(double reward){
            try{
                string rewardDenoter = readRewardDenoter();
                double current_reward_denoter = double.Parse(rewardDenoter.Substring(1));
                string changeTo = (reward + current_reward_denoter).ToString();
                File.WriteAllText(SettingsOperations.get_string_value("reward_denoter_path"), rewardDenoter[0] + changeTo);
                Console.WriteLine($"Current reward denoter after adding is {rewardDenoter[0]+changeTo}");
            }
            catch (Exception e){
                Console.WriteLine($"txt writing error. If because player respawned without reset, ignore this. {e.Message}");
            }
        }
        public static void resetRewardDenoter(){
            File.WriteAllText(SettingsOperations.get_string_value("reward_denoter_path"), "N0");
        }
        public static void toggleDistancePunish(){
            try{
                string rewardDenoter = readRewardDenoter();
                double current_reward_denoter = double.Parse(rewardDenoter.Substring(1));
                File.WriteAllText(SettingsOperations.get_string_value("reward_denoter_path"), (rewardDenoter[0] == 'N' ? 'P' : 'N') + current_reward_denoter.ToString());
                Console.WriteLine($"Current reward denoter is {(rewardDenoter[0] == 'N' ? 'P' : 'N') + current_reward_denoter.ToString()}");
            }
            catch (Exception e){
                Console.WriteLine($"txt writing error. {e.Message}");
            }
        }
    }
}