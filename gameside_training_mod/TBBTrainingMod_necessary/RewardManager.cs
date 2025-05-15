using Terraria;
using Terraria.ID;
using Terraria.ModLoader;
using System;
using System.IO;
using SettingsAccesser;
using Terraria.DataStructures;

namespace RewardManager{
    public class DealDamageIncentive : ModPlayer{
        public override void OnHitNPC(NPC target, NPC.HitInfo hit, int damageDone){
            if (target.type == NPCID.EyeofCthulhu){
                RewardAccumulantManager.addReward(hit.Damage*SettingsOperations.get_int_value("attack_reward_factor"));
                bool finish=true;
                foreach(NPC npc in Main.npc){
                    if(npc.active && npc.type==NPCID.EyeofCthulhu){
                        finish=false;
                        break;
                    }
                }
                if(finish){
                    File.WriteAllText(SettingsOperations.get_string_value("reward_accumulant_path"), "Inactive. Boss defeated.");
                }
                //Main.NewText($"Damage given: {hit.Damage}");
            }
        }
    }
    public class TakeDamageDisincentive : ModPlayer{
        public override void OnHurt(Player.HurtInfo info){
            RewardAccumulantManager.addReward(-info.Damage*SettingsOperations.get_int_value("hurt_punishment_factor"));
            if(Player.dead){
                Main.NewText("player died");
                File.WriteAllText(SettingsOperations.get_string_value("reward_accumulant_path"), "Inactive. Player died.");
            }
            //Main.NewText($"Damage taken: {info.Damage}");
        }
        public override void Kill(double damage, int hitDirection, bool pvp, PlayerDeathReason damageSource){
            File.WriteAllText(SettingsOperations.get_string_value("reward_accumulant_path"), "Inactive. Player died.");
            //Main.NewText("Player died");
        }
    }
    // NTS: txt file over socket for simplicity
    public class RewardAccumulantManager{
        public static string readRewardAccumulant(){
            try{
                string content = File.ReadAllText(SettingsOperations.get_string_value("reward_accumulant_path"));
                //Console.WriteLine($"Current reward accumulant is {content}");
                return content;
            }
            catch(Exception e){
                Console.WriteLine($"txt reading error. {e.Message}");
            }
            return "Error";
        }
        public static void addReward(double reward){
            try{
                double current_reward_accumulant=double.Parse(readRewardAccumulant());
                string changeTo=(reward+current_reward_accumulant).ToString();
                File.WriteAllText(SettingsOperations.get_string_value("reward_accumulant_path"), changeTo);
                //Console.WriteLine($"Current reward accumulant after adding is {changeTo}");
            }
            catch(Exception e){
                Console.WriteLine($"txt writing error. {e.Message}");
            }
        }
        public static void resetRewardAccumulant(){
            File.WriteAllText(SettingsOperations.get_string_value("reward_accumulant_path"), "0");
        }
    }
}