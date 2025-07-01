# RGS


> Веб-приложение для управления заказами в продуктовых магазинах. Позволяет сотрудникам создавать заявки, 
> а директору — просматривать и анализировать данные по
> магазинам.

---

## 🚀 Возможности

- Создание и редактирование заявок
-  Просмотр статистики по каждому магазину
-  Авторизация и роли пользователей
-  Экспорт данных
- Телеграмм бот

---

## Установka и запуск

1. Клонируй репозиторий:

`bash
git clone https://github.com/твой-ник/project-name.git
cd project-name
2. Установи виртуальное окружение и активируй:



python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3. Установи зависимости:



pip install -r requirements.txt

4. Создай .env файл и добавь туда:



SECRET_KEY=твой_секретный_ключ
DEBUG=True
DB_NAME=имя_бд
DB_USER=пользователь
DB_PASSWORD=пароль
DB_HOST=localhost
DB_PORT=5432

5. Примени миграции и запусти сервер:



python manage.py migrate
python manage.py runserver


---

🗂️ Структура проекта

project/
├── app1/
│   ├── models.py
│   ├── views.py
│   └── ...
├── project/
│   ├── settings.py
│   └── urls.py
├── templates/
├── static/
├── manage.py
└── .env


---
