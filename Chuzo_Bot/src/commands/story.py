from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.data.stories import STORY_ONE, STORY_TWO
from src.features.inventory import add_to_inventory
from config import STORY_IN_PROGRESS


async def story1_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /story1 command (The Lost Relic)."""
    context.user_data['current_story'] = STORY_ONE
    context.user_data['story_stage'] = 0
    await update.message.reply_text(STORY_ONE['stages'][0]['prompt'])
    return STORY_IN_PROGRESS

async def story2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /story2 command (The Sorcerer's Curse)."""
    context.user_data['current_story'] = STORY_TWO
    context.user_data['story_stage'] = 0
    await update.message.reply_text(STORY_TWO['stages'][0]['prompt'])
    return STORY_IN_PROGRESS

async def handle_story_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process user input during a story conversation."""
    story = context.user_data.get('current_story')
    stage = context.user_data.get('story_stage', 0)
    stage_data = story['stages'][stage]
    
    user_input = update.message.text.strip().lower()
    if user_input not in stage_data['valid_inputs']:
        await update.message.reply_text("Invalid input. Please try again.")
        return STORY_IN_PROGRESS
    
    await update.message.reply_text(stage_data['response'][user_input])
    
    if stage < len(story['stages']) - 1:
        context.user_data['story_stage'] = stage + 1
        await update.message.reply_text(story['stages'][stage + 1]['prompt'])
        return STORY_IN_PROGRESS
    else:
        reward = story['reward']
        add_to_inventory(context, reward)
        await update.message.reply_text(f"Story complete! You received: {reward}")
        return ConversationHandler.END

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current conversation."""
    await update.message.reply_text("🚫 Conversation canceled.")
    return ConversationHandler.END
