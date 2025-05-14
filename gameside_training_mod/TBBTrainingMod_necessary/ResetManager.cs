using Terraria.ModLoader;
using Terraria;
using Terraria.ID;
using Terraria.GameInput;
using Microsoft.Xna.Framework;
using TBBTrainingMod.Content.Items;
using TBBTrainingMod;

namespace ResetManager{
    public class Trigger : ModPlayer{
        public override void ProcessTriggers(TriggersSet triggersSet){
            if(Keybinds.resetKeybind.JustPressed){
                //teleport
                Player.Teleport(new Vector2(35000, 8166), 1);
                //replenish health and mana
                Player.statLife = Player.statLifeMax2;
                Player.statMana = Player.statManaMax2;
                //inventory clear
                for (int i = 0; i < Player.inventory.Length; i++){
                    Player.inventory[i].TurnToAir();
                }
                //hotbar setup
                Player.inventory[0].SetDefaults(ItemID.FlintlockPistol);
                for(int i = 1; i<=8; i++){
                    Player.inventory[i].SetDefaults(ItemID.HighVelocityBullet);
                    Player.inventory[i].stack = 9999;
                }
                Player.inventory[9].SetDefaults(ModContent.ItemType<OneTapper>());
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
                    35050,
                    8100,
                    NPCID.EyeofCthulhu,
                    Target: Main.myPlayer       
                );
            }
            if(Keybinds.debugKeybind.JustPressed){
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