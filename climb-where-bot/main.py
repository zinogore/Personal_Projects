from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PollHandler
from telegram.constants import ParseMode
from dotenv import load_dotenv
import os
import logging
import traceback
import json
import html
from src.bot_responses import handle_response
from src.bot_commands import help_command, generate_poll_command, close_poll_command, repoll_command, get_poll_results

# TODO
# Database:
# -> Record of different chats
    # -> Record of gyms (name, location, visits)
# - Weighted poll options
# -- lightweight DB to store weights (SQLite) - currently json
# - Pin and unpin most recent generated poll
# - LLM chatbot
# -- lightweight LLM or chatbot API
# - runtime -> whether schedule or run indefinitely
# check for empty repoll options
# map repoll options to chat id
# migrate thread data to db
# TODO DONE
# handle edited messages
# fix logging info not sending to dev chat
# optimize poll id tracking

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

# Handle messages from group | supergroup | private
async def handle_message(update, context):
    # handle photos (? for LLM)
    message_type = update.effective_chat.type
    text = update.effective_message.text
    logger.info(f'User ({update.effective_user.username}) in {message_type} ({update.effective_chat.id}): "{text}"')
    if message_type == 'group' or message_type == 'supergroup':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME,'').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)
    logger.info(f"Bot sent: {response}")
    await update.effective_message.reply_text(response)

# Errors
async def error(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    await context.bot.send_message(chat_id=DEV_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
    await update.message.reply_text(text=f"An exception was raised: {tb_list[-1]}")
        

if __name__ == '__main__':
    logger.info('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('generate_poll',generate_poll_command))
    app.add_handler(CommandHandler('close_poll',close_poll_command))
    app.add_handler(CommandHandler('re_poll',repoll_command))
    
    # Pollhandler
    app.add_handler(PollHandler(get_poll_results))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    logger.info('Run polling...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)