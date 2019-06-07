from telebot import types
from datetime import datetime, date, time
from threading import Timer


def parse_list(shop_list):
    shop_list = shop_list['list'][0].split(', ')
    for item in range(len(shop_list)):
        shop_list[item] = shop_list[item].capitalize()

    return shop_list


def create_buttons(parsed_list):
    shop_list = types.InlineKeyboardMarkup()
    for item in parsed_list:
        button = types.InlineKeyboardButton(item, callback_data=item)
        shop_list.add(button)

    return shop_list


def list_to_file(parsed_list):
    file = open('shop_list.txt', 'w')

    for item in parsed_list:
        file.write(item + '\n')
    file.close()


def list_from_file():
    file = open('shop_list.txt', 'r')

    shop_list = [line.strip() for line in file]
    file.close()

    return shop_list


def get_time_delta(time_notify, date_notify=None):
    def calculating_date():
        if date_notify is None:
            return date.today()
        return date.fromisoformat(date_notify)

    # Переводим время в формат времени
    parsed_time_notify = time.fromisoformat(time_notify)
    # Переводим дату в формат даты
    parsed_date_notify = calculating_date()
    # Собираем дату и время в формат даты и времени
    parsed_datetime = datetime.combine(parsed_date_notify, parsed_time_notify)
    datetime_now = datetime.now()
    delta = parsed_datetime - datetime_now
    # Получаем разницу во времени в секундах
    delta_seconds = delta.seconds

    return delta_seconds


def set_notify(time_delta, bot, chat_id):
    def notify():
        shop_list = list_from_file()
        markup = create_buttons(shop_list)
        bot.send_message(chat_id, 'Ты просил напомнить про покупки.\rВот список',
                         reply_markup=markup)
        # Удаляем таймер
        timer.cancel()

    # Создаем таймер
    timer = Timer(time_delta, notify)
    timer.start()
