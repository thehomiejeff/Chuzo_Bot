from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.data.stories import STORY_ONE, STORY_TWO
from src.features.inventory import add_to_inventory
from config import STORY_IN_PROGRESS
from src.models.item import Item  # Import the Item model

async def story1_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /story1 command (The Lost Relic) using 'next'/'stop' inputs."""
    context.user_data['current_story'] = STORY_ONE
    context.user_data['story_stage'] = 0
    # Append instructions to the first prompt.
    prompt = STORY_ONE['stages'][0]['prompt'] + "\n\nType 'next' to continue or 'stop' to cancel."
    await update.message.reply_text(prompt)
    return STORY_IN_PROGRESS

async def story2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /story2 command (The Sorcerer's Curse) using 'next'/'stop' inputs."""
    context.user_data['current_story'] = STORY_TWO
    context.user_data['story_stage'] = 0
    prompt = STORY_TWO['stages'][0]['prompt'] + "\n\nType 'next' to continue or 'stop' to cancel."
    await update.message.reply_text(prompt)
    return STORY_IN_PROGRESS

async def handle_story_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Process user input during a story conversation.
    Accepts only 'next' to proceed or 'stop' to cancel the story.
    """
    user_input = update.message.text.strip().lower()
    
    if user_input == "stop":
        await update.message.reply_text("🚫 Story canceled.")
        return ConversationHandler.END
    elif user_input == "next":
        story = context.user_data.get('current_story')
        stage = context.user_data.get('story_stage', 0)
        # If there is another stage, move to it.
        if stage < len(story['stages']) - 1:
            context.user_data['story_stage'] = stage + 1
            prompt = story['stages'][stage + 1]['prompt'] + "\n\nType 'next' to continue or 'stop' to cancel."
            await update.message.reply_text(prompt)
            return STORY_IN_PROGRESS
        else:
            # End of the story reached.
            reward_data = story['reward']  # Expected to be a dict: {"item": ..., "rarity": ...}
            reward_item = Item(name=reward_data["item"], rarity=reward_data["rarity"])
            add_to_inventory(context, reward_item)
            await update.message.reply_text(
                f"Story complete! You received: {reward_item.name} (Rarity: {reward_item.rarity})"
            )
            return ConversationHandler.END
    else:
        # Input was not recognized—remind the user.
        await update.message.reply_text("Please type 'next' to continue or 'stop' to cancel.")
        return STORY_IN_PROGRESS

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current conversation."""
    await update.message.reply_text("🚫 Story canceled.")
    return ConversationHandler.END
