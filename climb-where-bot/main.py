from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PollHandler
from dotenv import load_dotenv
import os
from src.bot_responses import handle_response
from src.bot_commands import help_command, generate_poll_command, close_poll_command, repoll_command, get_poll_results

# TODO
# - Weighted poll options
# -- lightweight DB to store weights (SQLite) - currently json
# - Pin and unpin most recent generated poll
# - LLM chatbot
# -- lightweight LLM or chatbot API
# - runtime -> whether schedule or run indefinitely

load_dotenv()

TOKEN = os.environ.get("TOKEN")
BOT_USERNAME = os.environ.get("BOT_USERNAME")

# Handle messages from group | supergroup | private
async def handle_message(update, context):
    message_type = update.message.chat.type
    text = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group' or message_type == 'supergroup':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME,'').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)
    print('Bot:',response)
    await update.message.reply_text(response)

# Errors
async def error(update, context):
    print(f'Update {update} casued error: {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
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
    print('Run polling...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)