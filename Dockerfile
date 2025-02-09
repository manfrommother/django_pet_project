# Dockerfile
FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y gcc libpq-dev

# Задаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект
COPY . /app/

# Открываем порт
EXPOSE 8000

# Выполняем миграции и запускаем сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
