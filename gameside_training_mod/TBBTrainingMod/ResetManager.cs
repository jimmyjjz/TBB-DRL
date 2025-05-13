using Terraria.ModLoader;
using Terraria;
using Terraria.ID;
using Terraria.GameInput;
using Microsoft.Xna.Framework;
using TBBTrainingMod.Content.Items;
using ModNS;

namespace RMNS{ // reset manager namespace
    public class ResetManager : ModPlayer{
        public override void ProcessTriggers(TriggersSet triggersSet){
            if(ModNS.TBBTrainingMod.resetKeybind.JustPressed){
                Player.Teleport(new Vector2(35000, 8166), 1);
                NPC.NewNPC(
                    Entity.GetSource_FromThis(),
                    35050,
                    8100,
                    NPCID.EyeofCthulhu,
                    Target: Main.myPlayer       
                );
                Player.statLife = Player.statLifeMax2;
                Player.statMana = Player.statManaMax2;
                for (int i = 0; i < Player.inventory.Length; i++){
                    Player.inventory[i].TurnToAir();
                }
                Player.inventory[0].SetDefaults(ItemID.FlintlockPistol);
                for(int i = 1; i<=8; i++){
                    Player.inventory[i].SetDefaults(ItemID.HighVelocityBullet);
                    Player.inventory[i].stack = 9999;
                }
                Player.inventory[9].SetDefaults(ModContent.ItemType<OneTapper>());
            }
            if(ModNS.TBBTrainingMod.debugKeybind.JustPressed){
                Vector2 position = Player.position;
                Main.NewText($"Player Position: Pixels = ({position.X}, {position.Y})", 255, 255, 0);
            }
        }
    }
}
