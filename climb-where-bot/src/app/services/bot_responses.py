from telegram import Update
from telegram.constants import ParseMode
import traceback
import json
import html

class BotResponses:
    def __init__(self, bot_username, dev_chat_id, logger):
        self.bot_username = bot_username
        self.dev_chat_id = dev_chat_id
        self.logger = logger
    
    # Responses
    def handle_response(self, text):
        """
        If/Else responses to messages with keywords
        """
        processed_text = text.lower()

        if 'alvin' and 'cholesterol' in processed_text:
            return 'Alvin, please take note of your cholesterol level...'
        
        if 'alvin' and 'good job' in processed_text:
            return 'Great job keeping your cholesterol level in check Alvin!'

        if 'elin' and 'cool' in processed_text:
            return '...'
        
        return 'I do not understand what you are saying...'

    # Handle messages from group | supergroup | private
    async def handle_message(self, update, context):
        # handle photos (? for LLM)
        message_type = update.effective_chat.type
        text = update.effective_message.text
        self.logger.info(f'User ({update.effective_user.username}) in {message_type} ({update.effective_chat.id}): "{text}"')
        if message_type == 'group' or message_type == 'supergroup':
            if self.bot_username in text:
                new_text = text.replace(self.bot_username,'').strip()
                response = self.handle_response(new_text)
            else:
                return
        else:
            response = self.handle_response(text)
        self.logger.info(f"Bot sent: {response}")
        await update.effective_message.reply_text(response)

    # Errors
    async def error(self, update, context):
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        self.logger.error("Exception while handling an update:", exc_info=context.error)

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
        await context.bot.send_message(chat_id=self.dev_chat_id, text=message, parse_mode=ParseMode.HTML)
        await update.message.reply_text(text=f"An exception was raised: {tb_list[-1]}")