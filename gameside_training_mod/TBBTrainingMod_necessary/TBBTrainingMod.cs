using Terraria.ModLoader;

namespace TBBTrainingMod{
    public class Keybinds : Mod{
        public static ModKeybind resetKeybind, debugKeybind;
        public override void Load(){
            resetKeybind = KeybindLoader.RegisterKeybind(this, "Reset", "R");
            debugKeybind = KeybindLoader.RegisterKeybind(this, "Debug", "G");
        }
        public override void Unload(){
            resetKeybind = null;
            debugKeybind = null;
        }
    }
}
