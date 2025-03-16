from telegram import Update
from telegram.ext import ContextTypes
from src.features.crafting import craft_item, check_hidden_recipe
from src.models.item import Item
from src.features.inventory import add_to_inventory
from config import CRAFTING_OPTIONS

async def crafting_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /craft command.

    Usage:
      1. /craft 
         -> Lists available categories and materials.
      2. /craft <category> <material>
         -> Crafts an item with the given material.
      3. /craft <category> <material1> <material2>
         -> Checks for a hidden recipe using two materials.
            - If found, grants legendary item.
            - Else, falls back to normal crafting with material1.
    """
    try:
        parts = update.message.text.strip().split()

        if len(parts) == 1:
            intro_message = (
                "✨ **Welcome to the Crafting System!** ✨\n\n"
                "To craft an item, use:\n"
                "`/craft <category> <material>`\n"
                "or for hidden recipes:\n"
                "`/craft <category> <material1> <material2>`\n\n"
                "Example:\n"
                "`/craft weapon Mithril`\n"
                "`/craft weapon Mithril Obsidian`\n\n"
                "**Available Categories & Materials:**\n"
            )
            for category, data in CRAFTING_OPTIONS.items():
                materials = ", ".join(data["materials"].keys())
                intro_message += f"\n*{category.title()}*:\n  Materials: {materials}\n"
            await update.message.reply_text(intro_message, parse_mode="Markdown")
            return

        category = parts[1].lower()

        if len(parts) >= 4:
            material1 = parts[2].title()
            material2 = " ".join(parts[3:]).title()

            hidden_item = check_hidden_recipe(material1, material2)
            if hidden_item:
                item = Item(name=hidden_item, rarity="legendary")
                add_to_inventory(context, item)
                await update.message.reply_text(
                    f"🎉 Hidden Recipe Unlocked! You crafted: {item.name} (Rarity: {item.rarity})"
                )
                return

            # Hidden recipe not found, fall back to normal crafting
            result = craft_item(category, material1)
            await process_crafting_result(update, context, result, category, material1, f"No hidden recipe found for '{material1}' + '{material2}'. ")
            return

        # Normal crafting
        material = " ".join(parts[2:]).title()
        result = craft_item(category, material)
        await process_crafting_result(update, context, result, category, material)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


async def process_crafting_result(update, context, result, category, material, prefix=""):
    """
    Helper function to process crafting result and update inventory.
    """
    if result.startswith("Success!"):
        crafted_item_name = result.split("crafted a ")[1].rstrip(".")
        rarity = CRAFTING_OPTIONS.get(category, {}).get("materials", {}).get(material, {}).get("rarity", "common")
        item = Item(name=crafted_item_name, rarity=rarity)
        add_to_inventory(context, item)
        await update.message.reply_text(f"{prefix}{result} (Rarity: {item.rarity})")
    else:
        await update.message.reply_text(f"{prefix}{result}")