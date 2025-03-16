from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.data.quests import PHOENIX_CALL_QUEST
from src.features.inventory import add_to_inventory

# Unique state for quest conversation
QUEST_IN_PROGRESS = 10

def format_stage_prompt(stage):
    """Helper to format the stage prompt with available choices."""
    prompt = stage['prompt']
    if stage.get('choices'):
        choice_text = "\n\n"
        for key, choice in stage['choices'].items():
            choice_text += f"{key.upper()}: {choice['text']}\n"
        prompt += choice_text
    return prompt

async def quest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Initiates the quest and sends the first prompt.
    """
    context.user_data['current_quest'] = PHOENIX_CALL_QUEST
    context.user_data['quest_stage'] = 0
    first_stage = PHOENIX_CALL_QUEST['stages'][0]
    
    prompt = format_stage_prompt(first_stage)
    await update.message.reply_text(prompt)
    return QUEST_IN_PROGRESS

async def handle_quest_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processes user's input and advances the quest.
    """
    quest = context.user_data.get('current_quest')
    stage_index = context.user_data.get('quest_stage', 0)
    stage = quest['stages'][stage_index]
    user_input = update.message.text.strip().lower()
    choices = stage.get('choices', {})

    # Validate input
    if not choices or user_input not in choices:
        await update.message.reply_text("Please choose one of the available options (e.g., A or B).")
        return QUEST_IN_PROGRESS

    choice = choices[user_input]
    next_stage = choice['next']

    # Display outcome text
    await update.message.reply_text(choice['text'])

    # Determine next stage
    if isinstance(next_stage, int):
        context.user_data['quest_stage'] = next_stage
        next_stage_data = quest['stages'][next_stage]
        prompt = format_stage_prompt(next_stage_data)
        await update.message.reply_text(prompt)
        return QUEST_IN_PROGRESS

    elif isinstance(next_stage, str) and next_stage.startswith("end_"):
        ending_stage_index = 6 if next_stage == "end_a" else 7 if next_stage == "end_b" else None
        if ending_stage_index is None:
            await update.message.reply_text("Quest error: unknown ending.")
            return ConversationHandler.END
        
        ending_stage = quest['stages'][ending_stage_index]
        reward_item = ending_stage.get("reward_item")
        reward_text = ""

        if reward_item:
            reward_text = f"\n\n🎁 You have earned: {reward_item['item']} (Rarity: {reward_item['rarity']})"
            add_to_inventory(context, f"{reward_item['item']} (Rarity: {reward_item['rarity']})")

        await update.message.reply_text(ending_stage['prompt'] + reward_text)
        return ConversationHandler.END

    else:
        await update.message.reply_text("Quest error: invalid next stage.")
        return ConversationHandler.END

async def cancel_quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the quest conversation."""
    await update.message.reply_text("🚫 Quest canceled.")
    return ConversationHandler.END