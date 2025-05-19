
using System.Collections.Generic;
using Terraria;
using Terraria.ModLoader;
using Terraria.UI;
public class SettingsButtonRemover : ModSystem{//Note: only removes settings button that exists in the bottom right on death screen
    public override void ModifyInterfaceLayers(List<GameInterfaceLayer> layers){
        var player = Main.LocalPlayer.GetModPlayer<MP>();
        if (player.isDead){
            layers.RemoveAll(layer => layer.Name.Contains("Settings Button"));
        }
    }
}
public class MP : ModPlayer{
    public bool isDead => Player.dead;
}