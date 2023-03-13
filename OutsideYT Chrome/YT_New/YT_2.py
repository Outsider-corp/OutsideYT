import requests

# Адрес страницы входа Google
login_url = "https://accounts.google.com/signin/v2/identifier"

# Логин и пароль от аккаунта Google
email = "example@gmail.com"
password = "examplepassword"

# Создание сессии и запрос страницы входа Google
session = requests.Session()
response = session.get(login_url)

# Извлечение значения "GALX" из HTML-кода страницы входа
galx_value = response.text.split('name="GALX"')[1].split('value="')[1].split('"')[0]

# Формирование параметров запроса и отправка запроса на вход с логином
login_params = {"continue": "https://www.google.com/", "GALX": galx_value}
login_data = {"Email": email, "Passwd": password, "GALX": galx_value}
login_response = session.post(login_url, params=login_params, data=login_data, allow_redirects=False)

# Проверка успешности авторизации
if "Location" in login_response.headers:
    location = login_response.headers["Location"]
    if "https://accounts.google.com/signin/challenge/" in location:
        print("Двухэтапная аутентификация включена, необходимо ввести код")
    elif "https://accounts.google.com/signin/rejected" in location:
        print("Неправильный логин или пароль")
    elif "https://accounts.google.com/signin/select" in location:
        print("Выберите аккаунт Google для входа")
else:
    print("Успешная авторизация")

# Извлечение cookie из сессии и использование ее для доступа к защищенным ресурсам
cookie_dict = session.cookies.get_dict()
print("Cookie:", cookie_dict)
