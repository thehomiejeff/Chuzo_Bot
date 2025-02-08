from telegram import Update
from telegram.ext import ContextTypes
from src.data.lore import BACKSTORY
from src.features.inventory import get_inventory

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    context.user_data['mood'] = "neutral"  # Default mood
    context.user_data['inventory'] = []    # Initialize inventory
    await update.message.reply_text(
        "Greetings, traveler! I am Chuzo, the Master Artificer. How may I assist you today?"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        "**Chuzo's Arcane Services** 🔮\n\n"
        "/start - Begin our conversation\n"
        "/help - Reveal command secrets\n"
        "/backstory - My humble origins\n"
        "/story1 - Begin the 'Lost Relic' story\n"
        "/story2 - Begin the 'Sorcerer's Curse' story\n"
        "/quest - Start a new quest\n"
        "/craft - Forge magical items\n"
        "/quizzes - Test your knowledge of the kingdom\n"
        "/inventory - View your inventory\n\n"
        "**Try these incantations:**\n"
        "- 'Tell me a story'\n- 'What can you craft?'\n- 'What time is it?'"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def backstory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backstory command."""
    await update.message.reply_text(BACKSTORY, parse_mode="Markdown")

async def inventory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /inventory command."""
    inventory = get_inventory(context)
    if not inventory:
        await update.message.reply_text("Your inventory is empty.")
    else:
        await update.message.reply_text(
            "📦 **Your Inventory** 📦\n\n" + "\n".join(inventory)
        )
