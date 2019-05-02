import loger
import telebot as tb
import proxy_changer
from time import sleep


# Читаем айпи и порт прокси из файла
ip_port = proxy_changer.read_proxy()

# Соединяемся с прокси чтобы обойти блокировку
tb.apihelper.proxy = {'https': 'https://{}'.format(ip_port)}

# Соединяемся с ботом и убираем многопоточность
bot = tb.TeleBot('720900961:AAHH-XKpDWthRv-w9NSiAPwPkmDqZfqEl9g', threaded=False)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '''
    Я пока что умею только здороваться. Напишите что-нибудь''')


@bot.message_handler(commands=['proxy'])
def proxy_message(message):
    bot.send_message(message.chat.id, '''
    Сейчас я на ip {}'''.format(ip_port))


@bot.message_handler(commands=['log'])
def send_log(message):
    log = open('history_work.log', 'r')
    bot.send_document(message.chat.id, log)

    # Проверяем есть ли файл
    try:
        file = open('last_cleaning_log.txt', 'r')

    # Если нету, считаем, что чистки ещё не было
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Чистки ещё не было')

    # Если есть, читаем из файла дату последней чистки лога и отправляем её
    else:
        date_last_cleaning_log = file.read()
        file.close()

        bot.send_message(message.chat.id, '''
        Последняя чистка была {}'''.format(date_last_cleaning_log))


@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    bot.reply_to(message, 'Привет, чтобы там не было написано')


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
