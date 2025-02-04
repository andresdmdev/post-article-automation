import logging as log
from telegram import Bot
from utils.utils import get_bot_vars

class TelegramServices():
  def __init__(self):
    # Create the Updater and pass it your bot's token.
    bot_vars = get_bot_vars()
    BOT_TOKEN_TELEGRAM = bot_vars.get("BOT_TOKEN_TELEGRAM")
    self.chat_id = bot_vars.get("CHAT_ID_TELEGRAM")
    self.bot = Bot(token=BOT_TOKEN_TELEGRAM)

  def send_message(self, text_message: str):
    """
    Send message to specified Telegram chat
    """
    log.info(f"Send message: {text_message}")

    self.bot.send_message(chat_id=self.chat_id, text=text_message)
