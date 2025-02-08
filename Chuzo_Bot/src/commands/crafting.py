from telegram import Update
from telegram.ext import ContextTypes
from src.features.crafting import craft_item, check_hidden_recipe
from config import CRAFTING_OPTIONS

async def crafting_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /craft command with improved user experience.
    
    Usage:
      1. /craft 
         -> Displays an introduction and lists available crafting categories and materials.
      
      2. /craft <category> <material>
         -> Attempts to craft an item normally using the given material.
      
      3. /craft <category> <material1> <material2>
         -> Checks for a hidden recipe with the two materials.
             - If found, returns the special item with 'legendary' rarity.
             - Otherwise, falls back to a normal crafting attempt using the first material.
    """
    try:
        parts = update.message.text.split()
        
        # If only the command itself is provided, display an introduction and available options.
        if len(parts) == 1:
            intro_message = (
                "✨ **Welcome to the Crafting System!** ✨\n\n"
                "To craft an item, use the command as follows:\n"
                "  `/craft <category> <material>`\n"
                "or for a hidden recipe:\n"
                "  `/craft <category> <material1> <material2>`\n\n"
                "For example:\n"
                "  `/craft weapon Mithril`\n"
                "  `/craft weapon Mithril Obsidian`\n\n"
                "**Available Crafting Categories and Materials** (hidden recipes are not listed):\n"
            )
            # List each category and its available materials.
            for category, data in CRAFTING_OPTIONS.items():
                materials = ", ".join(data["materials"].keys())
                intro_message += f"\n*{category.title()}*:\n  Materials: {materials}\n"
            
            await update.message.reply_text(intro_message, parse_mode="Markdown")
            return
        
        # Extract category (always the second word) and process further parameters.
        category = parts[1].lower()
        
        # If two or more materials are provided, treat as a dual-material (hidden recipe) attempt.
        if len(parts) >= 4:
            material1 = parts[2].title()
            # If exactly two materials are provided:
            if len(parts) == 4:
                material2 = parts[3].title()
            else:
                # If more than two words are provided after the category, join them for material2.
                material2 = " ".join(parts[3:]).title()
            
            # First check for a hidden recipe using the two materials.
            hidden_item = check_hidden_recipe(material1, material2)
            if hidden_item:
                # Award the hidden item with legendary rarity.
                from src.models.item import Item
                from src.features.inventory import add_to_inventory
                item = Item(name=hidden_item, rarity="legendary")
                add_to_inventory(context, item)
                await update.message.reply_text(
                    f"🎉 Hidden Recipe Unlocked! You crafted: {item.name} (Rarity: {item.rarity})"
                )
                return
            else:
                # Fall back to normal crafting using the first material.
                result = craft_item(category, material1)
                if result.startswith("Success!"):
                    # Extract the crafted item name.
                    crafted_item_name = result.split("crafted a ")[1].rstrip(".")
                    # Lookup rarity from the configuration.
                    rarity = CRAFTING_OPTIONS.get(category, {}).get("materials", {}).get(material1, {}).get("rarity", "common")
                    from src.models.item import Item
                    from src.features.inventory import add_to_inventory
                    item = Item(name=crafted_item_name, rarity=rarity)
                    add_to_inventory(context, item)
                    await update.message.reply_text(f"{result} (Rarity: {item.rarity})")
                else:
                    await update.message.reply_text(f"No hidden recipe found for '{material1}' + '{material2}'. {result}")
                return
        else:
            # Only one material provided: normal crafting attempt.
            material = " ".join(parts[2:]).title()
            result = craft_item(category, material)
            if result.startswith("Success!"):
                crafted_item_name = result.split("crafted a ")[1].rstrip(".")
                rarity = CRAFTING_OPTIONS.get(category, {}).get("materials", {}).get(material, {}).get("rarity", "common")
                from src.models.item import Item
                from src.features.inventory import add_to_inventory
                item = Item(name=crafted_item_name, rarity=rarity)
                add_to_inventory(context, item)
                await update.message.reply_text(f"{result} (Rarity: {item.rarity})")
            else:
                await update.message.reply_text(result)
            
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
