from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from src.data.quests import PHOENIX_CALL_QUEST
from src.features.inventory import add_to_inventory

# Define a unique state for the quest conversation
QUEST_IN_PROGRESS = 10  # This is an arbitrary state constant for the quest conversation

async def quest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starts the quest by sending the first prompt and saving the quest state.
    """
    context.user_data['current_quest'] = PHOENIX_CALL_QUEST
    context.user_data['quest_stage'] = 0
    stage = PHOENIX_CALL_QUEST['stages'][0]
    prompt = stage['prompt']
    # Append available choices to the prompt
    if stage.get('choices'):
        choice_text = "\n\n"
        for key, choice in stage['choices'].items():
            choice_text += f"{key.upper()}: {choice['text']}\n"
        prompt += choice_text
    await update.message.reply_text(prompt)
    return QUEST_IN_PROGRESS

async def handle_quest_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processes the user's input for the quest and branches the narrative accordingly.
    """
    quest = context.user_data.get('current_quest')
    stage_index = context.user_data.get('quest_stage', 0)
    stage = quest['stages'][stage_index]
    
    user_input = update.message.text.strip().lower()
    choices = stage.get('choices', {})

    # Validate the input
    if not choices or user_input not in choices:
        await update.message.reply_text("Please choose one of the available options (e.g., A or B).")
        return QUEST_IN_PROGRESS

    # Process the valid choice
    outcome_text = choices[user_input]['text']
    next_stage = choices[user_input]['next']
    
    # Display the outcome text
    await update.message.reply_text(outcome_text)
    
    # Determine the next stage
    if isinstance(next_stage, int):
        context.user_data['quest_stage'] = next_stage
        next_stage_data = quest['stages'][next_stage]
    elif isinstance(next_stage, str) and next_stage.startswith("end_"):
        if next_stage == "end_a":
            next_stage_data = quest['stages'][6]
        elif next_stage == "end_b":
            next_stage_data = quest['stages'][7]
        else:
            await update.message.reply_text("Quest error: unknown ending.")
            return ConversationHandler.END
        
        # Award the quest reward if defined
        reward_item = next_stage_data.get("reward_item")
        if reward_item:
            reward_text = f"You have earned: {reward_item['item']} (Rarity: {reward_item['rarity']})"
            add_to_inventory(context, f"{reward_item['item']} (Rarity: {reward_item['rarity']})")
        else:
            reward_text = "No reward defined."
            
        # End the quest after showing the final prompt and reward
        await update.message.reply_text(next_stage_data['prompt'] + "\n\n" + reward_text)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Quest error: invalid next stage.")
        return ConversationHandler.END

    # Show the prompt for the next stage along with its choices
    prompt = next_stage_data['prompt']
    if next_stage_data.get('choices'):
        choice_text = "\n\n"
        for key, choice in next_stage_data['choices'].items():
            choice_text += f"{key.upper()}: {choice['text']}\n"
        prompt += choice_text
    await update.message.reply_text(prompt)
    return QUEST_IN_PROGRESS

async def cancel_quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the quest conversation."""
    await update.message.reply_text("🚫 Quest canceled.")
    return ConversationHandler.END
