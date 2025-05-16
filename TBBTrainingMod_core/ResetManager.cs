using Terraria.ModLoader;
using Terraria;
using Terraria.ID;
using Terraria.GameInput;
using Microsoft.Xna.Framework;
using TBBTrainingMod.Content.Items;
using TBBTrainingMod;
using RewardManager;
using SettingsAccesser;

namespace ResetManager{
    public class Trigger : ModPlayer{
        public override void OnRespawn(){
            //replenish health and mana
            Player.statLife = Player.statLifeMax2;
            Player.statMana = Player.statManaMax2;
        }
        public override void ProcessTriggers(TriggersSet triggersSet)
        {
            if (Keybinds.resetKeybind.JustPressed)
            {
                //reset reward accumulant
                RewardAccumulantManager.resetRewardAccumulant();
                //reset velocity
                Player.velocity = Vector2.Zero;
                //reset fall start
                Player.fallStart = (int)(Player.position.Y / 16f);
                //teleport
                Player.Teleport(new Vector2(SettingsOperations.get_int_value("initial_point_x"), SettingsOperations.get_int_value("initial_point_y")), 1);
                //if player is dead then player will immediately spawn at defined location
                Main.spawnTileX = (int)Player.position.X / 16;
                Main.spawnTileY = (int)Player.position.Y / 16;
                Player.respawnTimer = 0;
                //replenish health and mana
                Player.statLife = Player.statLifeMax2;
                Player.statMana = Player.statManaMax2;
                //inventory clear
                for (int i = 0; i < Player.inventory.Length; i++)
                {
                    Player.inventory[i].TurnToAir();
                }
                //hotbar setup
                Player.inventory[0].SetDefaults(ItemID.SniperRifle);
                for (int i = 1; i <= 9; i++)
                {
                    Player.inventory[i].SetDefaults(ItemID.HighVelocityBullet);
                    Player.inventory[i].stack = 9999;
                }
                Player.inventory[19].SetDefaults(ModContent.ItemType<OneTapper>());
                //makes all hostile mobs disappear(not killing)
                foreach (NPC npc in Main.npc)
                {
                    if (npc.active && !npc.friendly && !npc.townNPC && !npc.dontTakeDamage)
                    {
                        npc.active = false;
                    }
                }
                //clear all items
                foreach (Item item in Main.item)
                {
                    if (item.active)
                    {
                        item.TurnToAir();
                    }
                }
                //clear chat
                for (int i = 0; i < 10; i++)
                {
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
            if (Keybinds.debugKeybind.JustPressed)
            {
                Vector2 position = Player.position;
                Main.NewText($"Player Position: Pixels = ({position.X}, {position.Y})", 255, 255, 0);
                foreach (Item item in Main.item)
                {
                    if (item.active)
                    {
                        item.TurnToAir();
                    }
                }
            }
        }
    }
}