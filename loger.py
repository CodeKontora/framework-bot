import logging
import datetime
from subprocess import run
from os.path import getsize


logging.basicConfig(filename="history_work.log", level=logging.INFO)


def write_info(data_proxy):
    logging.info('''
    Работаю на ip {ip}
    Порт {port}
    Страна {country}
    Последняя проверка {last_check}
    '''.format(ip=data_proxy['ip'], port=data_proxy['port'],
               country=data_proxy['country'], last_check=data_proxy['last_check']))


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

        # Получаем сегодняшнуюю дату и настраиваем её формат вывода
        # %d.%m.%Y в %H:%M означает формат день.месяц.год в час:минута
        last_cleaning_log = datetime.datetime.today().strftime("%d.%m.%Y в %H:%M")

        # Записываем в файл
        file = open('last_cleaning_log.txt', 'w')
        file.write(str(last_cleaning_log))
        file.close()


# Проверяем файл при каждой загрузке модуля
check_log_size()
