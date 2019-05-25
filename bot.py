import json
import loger
import apiai
import telebot as tb
import proxy_changer
from time import sleep


# Читаем айпи и порт прокси из файла
ip_port = proxy_changer.read_proxy()

# Соединяемся с прокси чтобы обойти блокировку
tb.apihelper.proxy = {'https': 'https://{}'.format(ip_port)}

# Соединяемся с ботом и убираем многопоточность
bot = tb.TeleBot('866043065:AAFiQShKR9takR3DE2FHoFjEM4bwRvnf5KE', threaded=False)


@bot.message_handler(content_types=['text'])
def response_to_user(message):
    chat_id = message.chat.id

    # Токен API к Dialogflow
    request = apiai.ApiAI('Пользовательский токен с диалог флоу').text_request()

    # На каком языке будет послан запрос
    request.lang = 'ru'

    # ID Сессии диалога чтобы потом учить бота
    # Напишите любое название
    request.session_id = 'Test'

    # Посылаем запрос к серверу с сообщением от юзера
    request.query = message.text

    # Получаем ответ от сервера и декодируем в utf-8
    response_json = json.loads(request.getresponse().read().decode('utf-8'))

    # Достаём ответ ИИ
    response_from_ai = response_json['result']['fulfillment']['speech']

    bot.send_message(chat_id, response_from_ai)


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
