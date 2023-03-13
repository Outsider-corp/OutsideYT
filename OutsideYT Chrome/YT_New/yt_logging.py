from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

# Путь к файлу, в котором будут сохраняться данные авторизации
TOKEN_PATH = 'token.pickle'

# Права доступа, которые требуются для приложения
SCOPES = ['https://www.googleapis.com/auth/drive']

# Файл, в котором находятся учетные данные для приложения
CREDENTIALS_FILE = 'credentials.json'

# Создание объекта Flow для авторизации
flow = InstalledAppFlow.from_client_secrets_file(
    CREDENTIALS_FILE, scopes=SCOPES)

# Получение кода авторизации
auth_url, _ = flow.authorization_url(prompt='consent')
print('Перейдите по ссылке для получения кода авторизации:\n{}'.format(auth_url))
code = input('Введите полученный код: ')

# Обмен кода авторизации на токен доступа и обновления
flow.fetch_token(code=code)

# Сохранение токена в файл
with open(TOKEN_PATH, 'wb') as token:
    pickle.dump(flow.credentials, token)

# Создание сессии для запросов к API Google
session = Request().authorize(flow.credentials)

# Получение cookie из сессии
cookies = session.get('https://www.google.com/').cookies.get_dict()
print(cookies)
