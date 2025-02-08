import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from src.commands.basic import start_command, help_command, backstory_command, inventory_command
from src.commands.story import story1_command, story2_command, handle_story_input, cancel_conversation
from config import TOKEN, STORY_IN_PROGRESS


# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Summoning Chuzo...")
    app = Application.builder().token(TOKEN).build()

    # Register basic command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("backstory", backstory_command))
    app.add_handler(CommandHandler("inventory", inventory_command))
    
    # Set up the conversation handler for story commands
    story_handler = ConversationHandler(
        entry_points=[
            CommandHandler("story1", story1_command),
            CommandHandler("story2", story2_command)
        ],
        states={
            STORY_IN_PROGRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_story_input)]
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
        allow_reentry=True
    )
    app.add_handler(story_handler)
    
    # Optional error handler
    app.add_error_handler(lambda update, context: logger.error(f"Error: {context.error}"))
    
    logger.info("Chuzo awakened! Polling for messages...")
    app.run_polling()

if __name__ == "__main__":
    main()
