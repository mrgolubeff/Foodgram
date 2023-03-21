# Foodgram project
# Проект "Продуктовый помощник"
### Описание
"Продуктовый помощник" позволяет создавать и выкладывать свои рецепты, подписываться на авторов рецептов, добавлять рецепты в избранное и формировать список покупок.

### Автор
Владимир Голубев

### Наполнение env-файла (/infra)
+ DB_ENGINE=[path to postgresql backend] # указываем, что работаем с postgresql
+ DB_NAME=[datebase name] # имя базы данных
+ POSTGRES_USER=[login] # логин для подключения к базе данных
+ POSTGRES_PASSWORD=[password] # пароль для подключения к БД
+ DB_HOST=[container name] # название сервиса (контейнера)
+ DB_PORT=[bd port] # порт для подключения к БД
+ SECRET_KEY=[Django secret key] # Секретный ключ из файла settings.py

### Команды для запуска приложения в контейнерах
1. Перейти в директорию foodgram_project_react/infra (в которой хранится файл docker-compose.yaml)
2. Из этой директории выполнить команду ```docker-compose up -d --build``` (это пересоберет контейнеры и запустит их в фоновом режиме)
3. Сделать миграции командой ```docker-compose exec infra_backend_1 python manage.py migrate```
4. Остановить исполнение проекта можно командой ```docker-compose down```
