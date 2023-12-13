import logging

from telegram.ext import Application

from config import bot_token
from handlers import wallet


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    bot = Application.builder().token(bot_token).build()
    logger.info('Бот успешно запущен.')
    wallet.wallet_handlers(bot)
    bot.run_polling()


if __name__ == '__main__':
    main()
