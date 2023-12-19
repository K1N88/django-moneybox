import asyncio
import logging
from random import randint

from telebot import TeleBot, types
from telebot.util import quick_markup

from config import bot_token


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_wallets(user):
    wallets = [
        {
            'name': 'RUB',
            'currency': 'RUB',
            'balance': 100.1,
            'id': 1
        },
        {
            'name': 'USD',
            'currency': 'USD',
            'balance': 200.1,
            'id': 2
        },
        {
            'name': 'EUR',
            'currency': 'EUR',
            'balance': 300.1,
            'id': 3
        },
        {
            'name': 'UAH',
            'currency': 'UAH',
            'balance': 400.1,
            'id': 4
        },
    ]
    return wallets


bot = TeleBot(bot_token)
logger.info('Бот успешно запущен.')


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = quick_markup({
        'Кошельки': {'callback_data': 'wallets'},
        'Переводы': {'callback_data': 'transfers'},
    }, row_width=2)
    text = 'Привет! Выбери действие:'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'wallets')
def wallets(call):
    wllts = get_wallets(call.message.chat.id)
    markup = 
    for item in wllts:

    text = 'Выбери кошелек:'
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


def process_name_step(message):
    try:

        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception()
        bot.send_message(message.chat.id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')


bot.infinity_polling()
