# Используем базовый образ для нашего
FROM python:3.7.3-alpine3.9

# Создаём директорию бота
RUN mkdir /shoper_bot

# Копируем все файлы из текущей директории в директорию бота
COPY . /shoper_bot

# Устанавливаем рабочую директорию
WORKDIR /shoper_bot

# Устанавливаем pytelegrambotapi и requests
RUN pip3 install --no-cache-dir pytelegrambotapi
RUN pip3 install --no-cache-dir requests

# Указываем команды для выполнения после запуска контейнера
CMD ["python3", "bot.py"]
