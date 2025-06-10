import telegram
from config import Config
import logging

logger = logging.getLogger(__name__)

def send_telegram_alert(message: str):
    """Send an alert via Telegram.
    
    Args:
        message: Alert message to send.
    """
    try:
        bot = telegram.Bot(token=Config.TELEGRAM_TOKEN)
        bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text=message)
        logger.info("Sent Telegram alert: %s", message)
    except Exception as e:
        logger.error("Failed to send Telegram alert: %s", e)