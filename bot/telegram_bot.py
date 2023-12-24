import logging
from pprint import pprint

import requests
from telebot import TeleBot, types
from telebot.util import quick_markup
from openapi_client import WalletsApi, ApiClient, Wallet

from config import bot_token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BASE_URL = 'http://localhost/api/v1/'


def get_wallets(user):
    '''
    wallets_url = BASE_URL + 'wallet'
    headers = {'Authorization': 'token'}
    try:
        wallets = requests.get(wallets_url, headers=headers)
    except Exception as e:
        logger.error(e, exc_info=True)
    '''
    api_client = ApiClient()
    '''
    wallets_api = WalletsApi(api_client)
    wallets = wallets_api.wallet_list().get()
    '''
    pprint(api_client.__dict__)

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


def get_id(call):
    return call.data.split(':')[-1]


bot = TeleBot(bot_token)
logger.info('Бот успешно запущен.')


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
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    row = []
    for item in wllts:
        row.append(types.InlineKeyboardButton(
            f"{item['currency']} {item['balance']}",
            callback_data=f'wallet edit:{item["id"]}',
        ))
        if len(row) == markup.row_width:
            markup.add(*row)
            row = []
    markup.add(*row)

    text = 'Выбери кошелек:'
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('wallet edit'))  # noqa
def wallet_edit(call):
    id = get_id(call)
    markup = quick_markup({
        'изменить': {'callback_data': f'wallet update:{id}'},
        'удалить': {'callback_data': f'wallet delete:{id}'},
        'назад': {'callback_data': 'wallets'},
    }, row_width=2)
    text = 'Выбери действие:'
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('wallet delete'))  # noqa
def wallet_delete(call):
    id = get_id(call)
    markup = quick_markup({
        'удалить': {'callback_data': f'wallet delete yes:{id}'},
        'отмена': {'callback_data': f'wallet edit:{id}'},
    }, row_width=2)
    text = 'Восстановить кошелек будет невозможно. Подтвердите действие:'
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('wallet delete yes'))  # noqa
def wallet_delete_yes(call):
    id = get_id(call)
    url = BASE_URL + 'wallet/' + id
    headers = {'Authorization': 'token'}
    try:
        requests.delete(url, headers=headers)
    except Exception as e:
        logger.error(e, exc_info=True)

    text = 'Кошелек удален'
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data.startswith('wallet update'))  # noqa
def wallet_update(call):
    id = get_id(call)
    call.wallet = id
    pprint(call.__dict__)
    text = 'Введите новое имя кошелька:'
    message = bot.send_message(call.message.chat.id, text)
    bot.register_next_step_handler(message, wallet_update_yes)


def wallet_update_yes(message):
    id = message.wallet
    url = BASE_URL + 'wallet/' + id
    headers = {'Authorization': 'token'}
    data = {'name': message.text}
    '''
    try:
        requests.patch(url, headers=headers, data=data)
    except Exception as e:
        logger.error(e, exc_info=True)
    '''
    text = 'Кошелек изменен'
    pprint(message.__dict__)
    bot.send_message(message.message.chat.id, text)


'''
# функция-обработчик первого шага
def first_step_handler(message: Message):
    # сохраняем ответ пользователя в атрибуте message.user_answer
    message.user_answer = message.text
    # отправляем сообщение с запросом на следующий шаг
    bot.send_message(message.chat.id, "Введите следующий шаг:")
    # регистрируем обработчик следующего шага
    bot.register_next_step_handler(message, second_step_handler)

# функция-обработчик второго шага
def second_step_handler(message: Message):
    # получаем ответ пользователя из атрибута message.user_answer
    user_answer = message.user_answer
    # сохраняем ответ пользователя в переменную
    user_answer2 = message.text
    # отправляем сообщение с подтверждением
    bot.send_message(message.chat.id, f"Вы ввели: {user_answer} и {user_answer2}")

# регистрируем обработчик первого шага
bot.register_next_step_handler(message, first_step_handler)
'''


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
    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}! Я - <b>{1.first_name}</b>, бот созданный для того чтобы помочь тебе.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

# Обработка команды "Рандомное число"
@bot.message_handler(content_types=['text'])
def random_number(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            # Генерация случайного числа от 0 до 100
            bot.send_message(message.chat.id, str(random.randint(0, 100)))

        elif message.text == '😊 Как дела?':
            # Создание инлайн-клавиатуры
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, как у тебя?', reply_markup=markup)

        elif message.text == '🎁 Получить подарок':
            # Создание клавиатуры с возможностью отправки локации
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Отправить локацию", request_location=True)

            markup.add(item1)

            bot.send_message(message.chat.id, "Отправь мне свою локацию и я найду для тебя ближайший подарок!",
                             reply_markup=markup)

# Обработка нажатий на кнопки инлайн-клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Я рад, что у тебя все хорошо! 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Не переживай, все наладится! 😊')

            # Удаление сообщения с инлайн-клавиатурой
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отлично, как у тебя?",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))

# Запуск бота
bot.polling(none_stop=True)
