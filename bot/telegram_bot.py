import asyncio
import logging
from random import randint

from telebot.async_telebot import AsyncTeleBot, types
from telebot.util import quick_markup

from config import bot_token


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


bot = AsyncTeleBot(bot_token)
logger.info('Бот успешно запущен.')


@bot.message_handler(commands=['start'])
async def welcome(message):
    # Создание клавиатуры
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("wallets")

    markup.add(item1)

    # Отправка приветственного сообщения и клавиатуры
    await bot.send_message(
        message.chat.id,
        "Привет, {0.first_name}! Я - <b>{1.first_name}</b>, бот созданный для того чтобы помочь тебе.".format(  # noqa
            message.from_user, await bot.get_me()
        ), parse_mode='html', reply_markup=markup
    )


# Обработка команды "Рандомное число"
@bot.message_handler(content_types=['text'])
async def random_number(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            # Генерация случайного числа от 0 до 100
            await bot.send_message(message.chat.id, str(randint(0, 100)))

        elif message.text == '😊 Как дела?':
            # Создание инлайн-клавиатуры
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            await bot.send_message(message.chat.id, 'Отлично, как у тебя?',
                                   reply_markup=markup)

        elif message.text == '🎁 Получить подарок':
            # Создание клавиатуры с возможностью отправки локации
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Отправить локацию",
                                         request_location=True)

            markup.add(item1)

            await bot.send_message(
                message.chat.id,
                "Отправь мне свою локацию и я найду для тебя ближайший подарок!",  # noqa
                reply_markup=markup
            )


# Обработка нажатий на кнопки инлайн-клавиатуры
@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                await bot.send_message(call.message.chat.id,
                                       'Я рад, что у тебя все хорошо! 😊')
            elif call.data == 'bad':
                await bot.send_message(call.message.chat.id,
                                       'Не переживай, все наладится! 😊')

            # Удаление сообщения с инлайн-клавиатурой
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Отлично, как у тебя?",
                reply_markup=None
            )

    except Exception as e:
        print(repr(e))


# Обработка отправки локации
@bot.message_handler(content_types=['location'])
async def handle_location(message):
    # Создание клавиатуры с возможностью отправки контакта
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Отправить контакт", request_contact=True)

    markup.add(item1)

    await bot.send_message(
        message.chat.id,
        "Спасибо! Теперь отправь мне свой контакт, чтобы я мог связаться с тобой.",  # noqa
        reply_markup=markup
    )


# Обработка отправки контакта
@bot.message_handler(content_types=['contact'])
async def handle_contact(message):
    await bot.send_message(
        message.chat.id,
        "Спасибо за контакт! Я свяжусь с тобой в ближайшее время."
    )


# Запуск бота
async def main():
    await bot.polling(none_stop=True)


if __name__ == '__main__':
    asyncio.run(main())


import telebot
from telebot import types

# Создание бота
bot = telebot.TeleBot('TOKEN')


# Обработка команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    # Создание клавиатуры
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")
    item3 = types.KeyboardButton("🎁 Получить подарок")

    markup.add(item1, item2, item3)

    # Отправка приветственного сообщения и клавиатуры
    bot.send_message(
        message.chat.id,
        "Привет, {0.first_name}! Я - <b>{1.first_name}</b>, бот созданный для того чтобы помочь тебе.".format(  # noqa
            message.from_user, bot.get_me()
        ), parse_mode='html', reply_markup=markup
    )


# Обработка команды "Рандомное число"
@bot.message_handler(content_types=['text'])
def random_number(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            # Генерация случайного числа от 0 до 100
            bot.send_message(message.chat.id, str(randint(0, 100)))

        elif message.text == '😊 Как дела?':
            # Создание инлайн-клавиатуры
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, как у тебя?',
                             reply_markup=markup)

        elif message.text == '🎁 Получить подарок':
            # Создание клавиатуры с возможностью отправки локации
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Отправить локацию",
                                         request_location=True)

            markup.add(item1)

            bot.send_message(
                message.chat.id,
                "Отправь мне свою локацию и я найду для тебя ближайший подарок!",  # noqa
                reply_markup=markup
            )


# Обработка нажатий на кнопки инлайн-клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id,
                                 'Я рад, что у тебя все хорошо! 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id,
                                 'Не переживай, все наладится! 😊')

            # Удаление сообщения с инлайн-клавиатурой
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Отлично, как у тебя?",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))


# Запуск бота
bot.polling(none_stop=True)
