using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Terraria.ModLoader;
using Terraria.GameInput;
using Microsoft.Xna.Framework.Input;

namespace ModNS{// mod namespace
    public class TBBTrainingMod : Mod{
        public static ModKeybind resetKeybind, debugKeybind;
        public override void Load(){
            resetKeybind = KeybindLoader.RegisterKeybind(this, "Reset", "R");
            debugKeybind = KeybindLoader.RegisterKeybind(this, "Debug", "G");
        }
    }
}
