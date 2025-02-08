import os
import random
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ====================
# Conversation States
# ====================
STORY_IN_PROGRESS = 1
QUEST_IN_PROGRESS = 2
CRAFTING_ITEM, CRAFTING_MATERIAL = range(2)
QUIZ_IN_PROGRESS = 3

# ====================
# Crafting System Configuration
# ====================
CRAFTING_OPTIONS = {
    "weapon": {
        "items": ["Dragonbone Sword", "Phoenix Bow", "Ice Dagger"],
        "materials": {
            "Dragon Scales": {"success_rate": 0.8, "rarity": "rare"},
            "Obsidian": {"success_rate": 0.6, "rarity": "common"},
            "Mithril": {"success_rate": 0.7, "rarity": "uncommon"}
        }
    },
    "potion": {
        "items": ["Elixir of Life", "Potion of Invisibility", "Liquid Lightning"],
        "materials": {
            "Phoenix Feather": {"success_rate": 0.9, "rarity": "legendary"},
            "Stardust": {"success_rate": 0.5, "rarity": "common"},
            "Moonstone": {"success_rate": 0.7, "rarity": "uncommon"}
        }
    },
    "artifact": {
        "items": ["Crown of Stars", "Amulet of Shadows", "Orb of Prophecy"],
        "materials": {
            "Ethereal Essence": {"success_rate": 0.85, "rarity": "rare"},
            "Ancient Relic": {"success_rate": 0.75, "rarity": "uncommon"},
            "Crystal Shard": {"success_rate": 0.6, "rarity": "common"}
        }
    }
}

# Hidden recipes (material combinations that unlock special items)
HIDDEN_RECIPES = {
    ("Phoenix Feather", "Ethereal Essence"): "Phoenix Amulet",
    ("Dragon Scales", "Ancient Relic"): "Dragonheart Gauntlet",
    ("Stardust", "Moonstone"): "Starlight Pendant"
}

# ====================
# Quest System Configuration
# ====================
QUESTS = {
    "find_the_lost_relic": {
        "stages": [
            {
                "prompt": "You find yourself in a dark forest. Do you go 'left' or 'right'?",
                "valid_inputs": ["left", "right"],
                "response": {
                    "left": "You stumble upon a hidden path. It leads to a clearing.",
                    "right": "You encounter a pack of wolves. They chase you back!"
                }
            },
            {
                "prompt": "In the clearing, you see a cave. Do you 'enter' or 'leave'?",
                "valid_inputs": ["enter", "leave"],
                "response": {
                    "enter": "Inside the cave, you find the lost relic!",
                    "leave": "You return home empty-handed."
                }
            }
        ],
        "reward": "Ancient Relic"
    }
}

# ====================
# Quiz Configuration
# ====================
QUIZ_QUESTIONS = [
    {
        "question": "What is the name of the sacred artifact Chuzo protects?",
        "options": ["Orb of Eternity", "Crown of Stars", "Amulet of Shadows"],
        "correct_answer": "Orb of Eternity"
    },
    {
        "question": "What role did Chuzo play in the Great War?",
        "options": ["Healer", "Strategist", "Blacksmith"],
        "correct_answer": "Strategist"
    },
    {
        "question": "Which mythical creature is NOT found in the kingdom?",
        "options": ["Dragon", "Phoenix", "Kraken"],
        "correct_answer": "Kraken"
    },
    {
        "question": "What is the name of the dark sorcerer who threatened the kingdom?",
        "options": ["Malakar", "Zorath", "Necron"],
        "correct_answer": "Malakar"
    },
    {
        "question": "Where did Chuzo grow up?",
        "options": ["Ruins of Brynthe", "Forest of Eldar", "Mountains of Kael"],
        "correct_answer": "Ruins of Brynthe"
    }
]

# ====================
# Backstory Updates
# ====================
BACKSTORY = (
    "📜 **Chuzo's Backstory** 📜\n\n"
    "Chuzo grew up in the **Ruins of Brynthe**, a once-great city now in decay. "
    "As a child, he survived by scavenging and begging until the **Alpha Empress** discovered him. "
    "Impressed by his resilience, she took him under her wing and trained him in the arcane arts.\n\n"
    "During the **Great War**, Chuzo served as a **strategist**, using his cunning to outmaneuver enemy forces. "
    "His mastery of magic turned the tide of battle, earning him the title of **Master Artificer**.\n\n"
    "Today, Chuzo protects the **Orb of Eternity**, a sacred artifact said to hold the power of creation itself. "
    "The kingdom is also home to mythical creatures like **dragons**, **phoenixes**, and **shadow wraiths**.\n\n"
    "Chuzo's greatest challenge came when the dark sorcerer **Malakar** threatened the kingdom. "
    "With his wisdom and magic, Chuzo defeated Malakar and saved the realm."
)

# ====================
# Story One: The Lost Relic
# ====================
STORY_ONE = {
    "title": "The Lost Relic",
    "stages": [
        {
            "prompt": "You are tasked with finding the lost relic of Brynthe. Do you 'search the forest' or 'ask the villagers'?",
            "valid_inputs": ["search the forest", "ask the villagers"],
            "response": {
                "search the forest": "You venture into the dark forest, where you hear strange whispers.",
                "ask the villagers": "The villagers tell you of a cave where the relic might be hidden."
            }
        },
        {
            "prompt": "You find a mysterious door. Do you 'open it' or 'look for another way'?",
            "valid_inputs": ["open it", "look for another way"],
            "response": {
                "open it": "The door creaks open, revealing the lost relic!",
                "look for another way": "You find a hidden passage, but it leads to a dead end."
            }
        }
    ],
    "reward": "Relic of Brynthe"
}

# ====================
# Story Two: The Sorcerer's Curse
# ====================
STORY_TWO = {
    "title": "The Sorcerer's Curse",
    "stages": [
        {
            "prompt": "A curse has befallen the kingdom. Do you 'seek the wise elder' or 'investigate the ruins'?",
            "valid_inputs": ["seek the wise elder", "investigate the ruins"],
            "response": {
                "seek the wise elder": "The elder tells you the curse can be broken with the Phoenix Amulet.",
                "investigate the ruins": "You find ancient texts hinting at the curse's origin."
            }
        },
        {
            "prompt": "You must choose: 'craft the Phoenix Amulet' or 'confront the sorcerer'.",
            "valid_inputs": ["craft the Phoenix Amulet", "confront the sorcerer"],
            "response": {
                "craft the Phoenix Amulet": "You gather materials and craft the amulet, breaking the curse!",
                "confront the sorcerer": "You face the sorcerer but are overwhelmed by his dark magic."
            }
        }
    ],
    "reward": "Phoenix Amulet"
}

# ====================
# Inventory System
# ====================
def get_inventory(context):
    """Retrieve the user's inventory"""
    return context.user_data.get('inventory', [])

def add_to_inventory(context, item):
    """Add an item to the user's inventory"""
    if 'inventory' not in context.user_data:
        context.user_data['inventory'] = []
    context.user_data['inventory'].append(item)

# ====================
# Core Command Handlers
# ====================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    context.user_data['mood'] = "neutral"  # Default mood
    context.user_data['inventory'] = []  # Initialize inventory
    await update.message.reply_text(
        "Greetings, traveler! I am Chuzo, the Master Artificer. How may I assist you today?"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
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
    """Handle /backstory command"""
    await update.message.reply_text(BACKSTORY, parse_mode="Markdown")

async def inventory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /inventory command"""
    inventory = get_inventory(context)
    if not inventory:
        await update.message.reply_text("Your inventory is empty.")
    else:
        await update.message.reply_text(
            "📦 **Your Inventory** 📦\n\n" + "\n".join(inventory)
        )

# ====================
# Story Handlers
# ====================
async def story1_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /story1 command (The Lost Relic)"""
    context.user_data['current_story'] = STORY_ONE
    context.user_data['story_stage'] = 0
    await update.message.reply_text(STORY_ONE['stages'][0]['prompt'])
    return STORY_IN_PROGRESS

async def story2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /story2 command (The Sorcerer's Curse)"""
    context.user_data['current_story'] = STORY_TWO
    context.user_data['story_stage'] = 0
    await update.message.reply_text(STORY_TWO['stages'][0]['prompt'])
    return STORY_IN_PROGRESS

async def handle_story_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user input during a story"""
    story = context.user_data['current_story']
    stage = context.user_data['story_stage']
    stage_data = story['stages'][stage]

    user_input = update.message.text.strip().lower()
    if user_input not in stage_data['valid_inputs']:
        await update.message.reply_text("Invalid input. Please try again.")
        return STORY_IN_PROGRESS

    await update.message.reply_text(stage_data['response'][user_input])

    if stage < len(story['stages']) - 1:
        context.user_data['story_stage'] += 1
        await update.message.reply_text(story['stages'][stage + 1]['prompt'])
        return STORY_IN_PROGRESS
    else:
        reward = story['reward']
        add_to_inventory(context, reward)
        await update.message.reply_text(f"Story complete! You received: {reward}")
        return ConversationHandler.END

# ====================
# Cancel Conversation Handler
# ====================
async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current conversation."""
    await update.message.reply_text("🚫 Conversation canceled.")
    return ConversationHandler.END

# ====================
# Error Handler
# ====================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors gracefully."""
    print(f"Error: {context.error}")
    await update.message.reply_text("⚠️ An error occurred. Please try again.")

# ====================
# Application Setup
# ====================
if __name__ == "__main__":
    print("Summoning Chuzo...")
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("backstory", backstory_command))
    app.add_handler(CommandHandler("inventory", inventory_command))
    app.add_handler(CommandHandler("story1", story1_command))
    app.add_handler(CommandHandler("story2", story2_command))

    # Story conversation handler
    story_handler = ConversationHandler(
        entry_points=[CommandHandler("story1", story1_command), CommandHandler("story2", story2_command)],
        states={STORY_IN_PROGRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_story_input)]},
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
        allow_reentry=True
    )
    app.add_handler(story_handler)

    # Add error handler
    app.add_error_handler(error_handler)

    print("Chuzo awakened! Polling for messages...")
    app.run_polling()