# Dog API Project

## Описание

Проект **Dog API** реализует REST API для работы с моделями **Dog** и **Breed** с использованием Django и Django REST Framework. API позволяет:
- Создавать, получать, обновлять и удалять записи о собаках (Dog) и породах собак (Breed)
- Получать список собак с аннотацией среднего возраста собак той же породы
- Получать детали о собаке с количеством собак той же породы
- Получать список пород с аннотацией количества собак для каждой породы

Проект также включает оптимизацию запросов с использованием подзапросов (OuterRef, Subquery), Docker-контейнеризацию для быстрой настройки окружения, а также полный набор тестов для проверки корректности работы API.

## Структура проекта

```plaintext
dog_api_project/
├── dog_project/
│   ├── __init__.py
│   ├── settings.py          # Основные настройки Django, в том числе настройки базы данных и переменные окружения
│   ├── urls.py              # Основная маршрутизация проекта
│   └── wsgi.py
├── dogs/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # Модели Dog и Breed с требуемыми полями
│   ├── serializers.py       # Сериализаторы для моделей Dog и Breed, включая дополнительные поля (average_age, same_breed_count, dog_count)
│   ├── views.py             # API ViewSet'ы (DogViewSet, BreedViewSet) с реализацией CRUD-операций и подзапросами
│   ├── urls.py              # Маршруты API, зарегистрированные с помощью DRF роутеров
│   └── tests.py             # Расширенный набор тестов для проверки всех эндпоинтов API
├── Dockerfile               # Файл для сборки Docker-образа приложения
├── docker-compose.yml       # Конфигурация Docker Compose для запуска Django и PostgreSQL в контейнерах
├── requirements.txt         # Список зависимостей проекта (Django, DRF, psycopg2-binary, python-dotenv и т.д.)
├── .env.example            # Пример файла переменных окружения (необходимо создать локальный .env файл)
└── README.md               # Документация по проекту (этот файл)
```

## Установка и запуск

### 1. Локальный запуск (без Docker)

1. Клонирование репозитория:
```bash
git clone <URL репозитория>
cd dog_api_project
```

2. Создание и активация виртуального окружения:
```bash
python -m venv venv
# Для Linux/MacOS:
source venv/bin/activate
# Для Windows:
venv\Scripts\activate
```

3. Установка зависимостей:
```bash
pip install -r requirements.txt
```

4. Настройка переменных окружения:
   - Создайте файл .env в корне проекта на основе файла .env.example:
   ```bash
   cp .env.example .env
   ```
   
   Пример содержимого .env для локальной разработки:
   ```ini
   DEBUG=1
   DATABASE_NAME=dog_api_db
   DATABASE_USER=dog_user
   DATABASE_PASSWORD=dog_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   SECRET_KEY=your_secret_key_here
   ```

5. Применение миграций:
```bash
python manage.py migrate
```

6. Запуск сервера разработки:
```bash
python manage.py runserver 0.0.0.0:8000
```

API будет доступно по адресу: http://localhost:8000/api/

### 2. Запуск через Docker

1. Убедитесь, что Docker и Docker Compose установлены.

2. Запуск контейнеров:
   В корневой директории проекта выполните:
   ```bash
   docker-compose up --build
   ```
   
   Эта команда:
   - Соберёт Docker-образ приложения
   - Запустит контейнер с Django и контейнер с PostgreSQL
   - При необходимости выполнит миграции

3. Доступ к API:
   После успешного запуска контейнеров API будет доступно по адресу: http://localhost:8000/api/

4. Выполнение команд внутри контейнера:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py test
```

## Использование API

### Эндпоинты модели Dog

- **GET /api/dogs/**
  Возвращает список собак с аннотацией average_age (средний возраст собак той же породы)

- **POST /api/dogs/**
  Создает новую запись о собаке. Пример JSON запроса:
  ```json
  {
    "name": "Bella",
    "age": 4,
    "breed": 1,
    "gender": "Female",
    "color": "Brown",
    "favorite_food": "Chicken",
    "favorite_toy": "Frisbee"
  }
  ```

- **GET /api/dogs/<id>/**
  Возвращает детали собаки с полем same_breed_count (количество собак той же породы)

- **PUT /api/dogs/<id>/**
  Обновляет запись о собаке

- **DELETE /api/dogs/<id>/**
  Удаляет запись о собаке

### Эндпоинты модели Breed

- **GET /api/breeds/**
  Возвращает список пород с аннотацией dog_count (количество собак для каждой породы)

- **POST /api/breeds/**
  Создает новую запись о породе. Пример JSON запроса:
  ```json
  {
    "name": "Golden Retriever",
    "size": "Large",
    "friendliness": 5,
    "trainability": 5,
    "shedding_amount": 4,
    "exercise_needs": 5
  }
  ```

- **GET /api/breeds/<id>/**
  Возвращает детали породы

- **PUT /api/breeds/<id>/**
  Обновляет запись о породе

- **DELETE /api/breeds/<id>/**
  Удаляет запись о породе

## Тестирование

Для запуска тестов выполните:
```bash
python manage.py test
```

Если вы используете Docker:
```bash
docker-compose exec web python manage.py test
```

Тесты покрывают создание, получение, обновление и удаление записей для моделей Dog и Breed, а также проверяют корректность вычисления агрегированных полей.

## Зависимости

Основные зависимости указаны в файле requirements.txt:
- Django
- djangorestframework
- psycopg2-binary
- python-dotenv

## Docker

Проект содержит файлы:
- Dockerfile – для сборки Docker-образа приложения
- docker-compose.yml – для одновременного запуска сервисов Django и PostgreSQL

## Переменные окружения

Настройки приложения (база данных, DEBUG, SECRET_KEY и т.д.) задаются через переменные окружения. Пример файла .env.example приведён в корне проекта. Для локального запуска измените DATABASE_HOST на localhost.
