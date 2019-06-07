import json
import loger
import apiai
import list_control
import telebot as tb
import proxy_changer
from time import sleep


# Читаем айпи и порт прокси из файла
ip_port = proxy_changer.read_proxy()

# Соединяемся с прокси чтобы обойти блокировку
tb.apihelper.proxy = {'https': 'https://{}'.format(ip_port)}

# Соединяемся с ботом и убираем многопоточность
bot = tb.TeleBot('Токен бота', threaded=False)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    about_me = '''Привет. Я помогу со списком покупок.
Попроси меня сделать список или пойти в магазин'''
    bot.send_message(message.chat.id, about_me)


@bot.message_handler(content_types=['text'])
def response_to_user(message):
    chat_id = message.chat.id

    # Токен API к Dialogflow
    request = apiai.ApiAI('Пользовательский токен с ДФ').text_request()

    # На каком языке будет послан запрос
    request.lang = 'ru'

    # ID Сессии диалога чтобы потом учить бота
    request.session_id = 'Любое текстовое значение'

    # Посылаем запрос к серверу с сообщением от юзера
    request.query = message.text

    # Получаем ответ от сервера и декодируем в utf-8
    response_json = json.loads(request.getresponse().read().decode('utf-8'))

    # Достаём ответ ИИ
    response_from_ai = response_json['result']['fulfillment']['speech']
    # Достаём текущее намерение
    action = response_json['result']['action']
    # Достаём список покупок от пользователя
    parameters = response_json['result']['parameters']

    # Создаем список покупок
    if action == 'create_list.shop_list':
        # Парсим список
        shop_list = list_control.parse_list(parameters)
        # Записываем его в файл
        list_control.list_to_file(shop_list)
        shop_list = list_control.list_from_file()
        markup = list_control.create_buttons(shop_list)
        # Отправляем его
        bot.send_message(chat_id, 'Записал. Вот список', reply_markup=markup)

    # Создаем напоминание
    elif action == 'create_list.shop_list.notify':
        # Если бот не смог распарсить время
        if not parameters['time']:
            bot.send_message(chat_id, 'Не могу прочитать время')

        # Если напоминание поставлено без даты
        if not parameters['date']:
            bot.send_message(chat_id, 'Напомню в {}'.format(parameters['time']))
            time_delta = list_control.get_time_delta(parameters['time'])
            list_control.set_notify(time_delta, bot, chat_id)

        # Если напоминание поставлено с датой и временем
        else:
            bot.send_message(chat_id, 'Напомню {} в {}'.format(parameters['date'],
                                                               parameters['time']))
            time_delta = list_control.get_time_delta(parameters['time'], parameters['date'])
            list_control.set_notify(time_delta, bot, chat_id)

    # Ответ бота на любые другие вопросы
    else:
        bot.send_message(chat_id, response_from_ai)


@bot.callback_query_handler(lambda query: True)
def delete_button_from_list(query):
    # Получаем список из файла
    file_shop_list = list_control.list_from_file()
    # Создаём список из кнопок
    shop_list = list_control.create_buttons(file_shop_list)

    # Удаляем кнопку
    for button in shop_list.keyboard:
        if button[0]['callback_data'] == query.data:
            index_for_remove = shop_list.keyboard.index(button)
            del shop_list.keyboard[index_for_remove]
            file_shop_list.remove(button[0]['text'])
            list_control.list_to_file(file_shop_list)

    # Если список пустой – удаляем сообщение с ним
    if not shop_list.keyboard:
        bot.delete_message(query.message.chat.id, query.message.message_id)
    # Если не пустой, обновляем сообщение с ним
    else:
        bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id,
                                      reply_markup=shop_list)


try:
    # Запускаем бота
    bot.polling()

# Если прокси отваливается
except OSError as e:
    # Тормозим бота
    bot.stop_polling()

    # Записываем в лог имя ошибки прокси
    loger.write_error(type(e).__name__)

    # Ждём пять секунд, чтобы не словить бан за слишком частые запросы
    sleep(5)

    # Получаем данные о прокси
    proxy = proxy_changer.get_proxy()

    # Обновляем адрес прокси, чтобы бот выводил текущий адрес
    ip_port = proxy['ip_port']

    # Ставим прокси
    tb.apihelper.proxy = {'https': 'https://{}'.format(proxy['ip_port'])}

    # Перезаписываем в файл
    proxy_changer.write_proxy(proxy)

    # Записываем данные нового прокси
    loger.write_info(proxy)

    # Запускаем бота
    bot.polling()
