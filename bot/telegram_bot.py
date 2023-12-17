import asyncio
import logging

from telebot.async_telebot import AsyncTeleBot

from config import bot_token


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    bot = AsyncTeleBot(bot_token)
    logger.info('Бот успешно запущен.')

    @bot.message_handler(commands=['help', 'start'])
    async def send_welcome(message):
        await bot.reply_to(message, """\
    Hi there, I am EchoBot.
    I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
    """)

    @bot.message_handler(func=lambda message: True)
    async def echo_message(message):
        await bot.reply_to(message, message.text)

    asyncio.run(bot.polling())


if __name__ == '__main__':
    main()
