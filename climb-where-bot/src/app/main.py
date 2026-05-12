from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PollHandler
from dotenv import load_dotenv
import os
import logging
from src.app.services.bot_responses import BotResponses
from src.app.services.bot_commands import BotCommands
from src.app.repositories.repository import get_list_of_gym_names

# TODO
# refactor: improve readability by using objects to define main app logic - DONE
# refactor: manage db models - DONE
# refactor: manage db session - DONE
# refactor: manage data access layer (repository) - FIX REQUIRED

# create store ids method - polls table
# create remove ids method - polls table
# creat store repoll options method - chats table

# fix: check for empty repoll options
# map repoll options to chat id
# migrate thread data to db

# Future works
# -- lightweight LLM or chatbot API
# - Pin and unpin most recent generated poll
# - Weighted poll options
# - runtime -> whether schedule or run indefinitely

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Get env variables
load_dotenv()

TOKEN = os.environ.get("TOKEN")
BOT_USERNAME = os.environ.get("BOT_USERNAME")
DEV_CHAT_ID = os.environ.get("DEV_CHAT_ID")

POLL_OPTIONS = get_list_of_gym_names()
NUM_OPTIONS = 7
NUM_SHUFFLE = 3
NON_RUDE = False
dict_chat_id = {}
dict_poll_id = {}
repoll_options = []

bot_responses = BotResponses(bot_username=BOT_USERNAME, dev_chat_id=DEV_CHAT_ID, logger=logger)
bot_commands = BotCommands(
    poll_options=POLL_OPTIONS,
    num_options=NUM_OPTIONS,
    num_shuffle=NUM_SHUFFLE,
    non_rude=NON_RUDE,
    dict_chat_id=dict_chat_id,
    dict_poll_id=dict_poll_id,
    repoll_options=repoll_options,
    logger=logger
    )

if __name__ == '__main__':
    logger.info('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('help',bot_commands.help_command))
    app.add_handler(CommandHandler('generate_poll',bot_commands.generate_poll_command))
    app.add_handler(CommandHandler('close_poll',bot_commands.close_poll_command))
    app.add_handler(CommandHandler('re_poll',bot_commands.repoll_command))
    
    # Pollhandler
    app.add_handler(PollHandler(bot_commands.get_poll_results))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, bot_responses.handle_message))

    # Errors
    app.add_error_handler(bot_responses.error)

    # Polls the bot
    logger.info('Run polling...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)