import logging
import sys
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
from handlers import BotHandlers

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot"""
    try:
        # Check if token exists
        if not Config.BOT_TOKEN:
            logger.error("BOT_TOKEN not found! Please set it in environment variables.")
            return
        
        # Create application
        application = Application.builder().token(Config.BOT_TOKEN).build()
        
        # Initialize handlers
        handlers = BotHandlers()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", handlers.start_command))
        application.add_handler(CommandHandler("help", handlers.help_command))
        application.add_handler(CommandHandler("about", handlers.about_command))
        application.add_handler(CommandHandler("case", handlers.case_command))
        application.add_handler(CommandHandler("expand", handlers.expand_command))
        application.add_handler(CommandHandler("format", handlers.format_command))
        
        # Add message handler for regular text
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handlers.handle_message
        ))
        
        # Start the bot
        logger.info("🚀 Bot is starting...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        raise

if __name__ == '__main__':
    main()
