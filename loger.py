# encoding=utf8
import logging
import datetime
from subprocess import run
from os.path import getsize
import requests


logging.basicConfig(filename="history_work.log", level=logging.INFO)


def write_info(data_proxy):
    # Проверяем, что прокси пришёл в полном формате
    try:
        logging.info('''
        Работаю на ip {ip}
        Порт {port}
        Страна {country}
        Последняя проверка {last_check}
        '''.format(ip=data_proxy['ip'], port=data_proxy['port'],
                   country=data_proxy['country'], last_check=data_proxy['last_check']))

    # Если прокси не в полном формате
    # значит бот попал в бан и использует резервный прокси из файла
    except KeyError:
        # Узнаём причину бана от сайта
        response = requests.get('http://pubproxy.com/api/proxy?type=https')

        # Записываем её в лог
        logging.error('''Прокси не пришел, бот попал в бан.
        Ответ сайта: {}'''.format(response.text))


def write_error(description_error):
    logging.error('''
    Прокси отвалился с ошибкой {error}
    Подбираю новый
    '''.format(error=description_error))


def check_log_size():
    # Проверяем размер файла
    # Если он больше или равен 1 Мб или же 1 048 576 байт, то удаляем лог
    if (getsize('history_work.log') >= 1048576):
        # Запускаем процесс для удаления файла
        run(['rm', 'history_work.log'])


# Проверяем файл при каждой загрузке модуля
check_log_size()
