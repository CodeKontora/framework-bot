# Используем базовый образ для нашего
FROM python:stretch

# Создаём директорию бота
RUN mkdir /shoper_bot

# Копируем все файлы из текущей директории в директорию бота
COPY . /shoper_bot

# Устанавливаем рабочую директорию
WORKDIR /shoper_bot

# Устанавливаем pytelegrambotapi
RUN pip3 install --no-cache-dir pytelegrambotapi
RUN pip3 install --no-cache-dir apiai

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Указываем команды для выполнения после запуска контейнера
CMD ["python3", "bot.py"]