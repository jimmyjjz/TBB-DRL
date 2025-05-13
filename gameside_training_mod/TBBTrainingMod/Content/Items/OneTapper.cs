using Terraria;
using Terraria.ID;
using Terraria.ModLoader;

namespace TBBTrainingMod.Content.Items{ 
	public class OneTapper : ModItem{
		public override void SetDefaults(){
			Item.damage = 999999;
			Item.DamageType = DamageClass.Melee;
			Item.width = 40;
			Item.height = 80;
			Item.useTime = 10;
			Item.useAnimation = 10;
			Item.useStyle = ItemUseStyleID.Swing;
			Item.knockBack = 6;
			Item.value = Item.buyPrice(silver: 1);
			Item.rare = ItemRarityID.Blue;
			Item.UseSound = SoundID.Item1;
			Item.autoReuse = true;
		}
		public override void AddRecipes(){
			Recipe recipe = CreateRecipe();
			recipe.AddIngredient(ItemID.DirtBlock, 1);
			recipe.AddTile(TileID.WorkBenches);
			recipe.Register();
		}
	}
}
