from telegram import Update
from telegram.ext import ContextTypes
from src.data.lore import BACKSTORY
from src.features.inventory import get_inventory

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with a polished, interactive greeting."""
    # Initialize user data
    context.user_data['mood'] = "neutral"  # Default mood
    context.user_data['inventory'] = []    # Initialize inventory
    
    # Enhanced greeting message with Markdown formatting
    greeting = (
        "✨ **Welcome, Adventurer!** ✨\n\n"
        "I am **Chuzo**, the Master Artificer—guardian of ancient secrets and mystical wonders.\n\n"
        "Embark on your journey with these powerful commands:\n"
        "• `/backstory` — Uncover my origins and the lore of our realm.\n"
        "• `/story1` — Begin the quest **'The Lost Relic'**.\n"
        "• `/story2` — Unravel the mystery of **'The Sorcerer's Curse'**.\n"
        "• `/quest` — Embark on a challenging quest.\n"
        "• `/craft` — Forge mighty items from magical materials.\n"
        "• `/quizzes` — Test your knowledge of the realm.\n"
        "• `/inventory` — View the treasures you've gathered.\n"
        "• `/help` — See all available commands and secrets.\n\n"
        "May the magic guide your path, brave traveler! 🔮"
    )
    
    await update.message.reply_text(greeting, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        "**Chuzo's Arcane Services** 🔮\n\n"
        "/start - Begin our conversation\n"
        "/help - Reveal command secrets\n"
        "/backstory - My humble origins\n"
        "/story1 - Begin the 'Lost Relic' story\n"
        "/story2 - Begin the 'Sorcerer's Curse' story\n"
        "/quest - Embark on a challenging quest\n"
        "/craft - Forge magical items\n"
        "/quizzes - Test your knowledge of the realm\n"
        "/inventory - View your inventory\n\n"
        "**Try these incantations:**\n"
        "- 'Tell me a story'\n"
        "- 'What can you craft?'\n"
        "- 'What time is it?'"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def backstory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backstory command."""
    await update.message.reply_text(BACKSTORY, parse_mode="Markdown")

async def inventory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /inventory command to display all items with rarity."""
    inventory = get_inventory(context)
    if not inventory:
        await update.message.reply_text("Your inventory is empty.")
    else:
        response = "📦 **Your Inventory** 📦\n\n"
        for item in inventory:
            # Check if the item has the attributes 'name' and 'rarity'
            try:
                response += f"- {item.name} (Rarity: {item.rarity})\n"
            except AttributeError:
                # Fallback if item is not an instance of Item
                response += f"- {str(item)}\n"
        await update.message.reply_text(response, parse_mode="Markdown")
