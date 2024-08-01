# Используем официальный образ Python в качестве базового
FROM python:3.12-alpine
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию контейнера
COPY . .

# Настраиваем переменные окружения
ENV PYTHONUNBUFFERED=1

# Прогоняем миграции перед запуском бота
RUN alembic upgrade head

# Указываем команду для запуска бота
CMD ["python", "main.py"]