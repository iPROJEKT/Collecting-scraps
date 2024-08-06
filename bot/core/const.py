from bot.core.config import settings

LOG_FORM = '%(asctime)s, %(levelname)s, %(message)s'
LOG_FILEMOD = 'w'
LOG_FILENAME = 'logger.log'
TOKEN_EXECT = 'Token is invalid!'
A1 = 'Отчет от'
A2 = 'Номер установки'
B2 = 'Что случились (наименование дефекта)'
C2 = 'Кто зафиксировал'
D2 = 'Развернутое пояснение'
E2 = 'Имя программы'
F2 = 'Координаты'
G2 = 'Во сколько зарегистрировали'
FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_TITLE = 'Отчет от {}'
LOCALE = 'ru_RU'
SHEET_TITLE = 'Регистация дефектов от {}'
ROW_COUNT = 400
COLUMN_COUNT = 9
RANGE = r'A1:H400'
SHEERTYPE = 'GRID'
ID = None
TYPE = 'anyone'
ROLE = 'reader'
TABLE_UPDATA = 'ROWS'
FILDS_FOR_SERVIS_ACCOUNT = 'id'
SHEERTID = 0
ROW_COUNT_ERROR = 'Слишком много дефектов'
COLUMN_COUNT_ERROR = 'В таблице всего 7 столбцов'
TABLE_VALUES_FOR_DEF = [
    [A1],
    [A2, B2, C2, D2, E2, F2, G2]
]
TABLE_VALUES_FOR_OBS = [
    [A1],
    [A2, C2, D2]
]
TABLE_VALUES_FOR_MEH = [
    [A1],
    [G2, C2, 'Замена', 'Марка проволки', 'Диаметр', 'Газ', A2]
]
SPREADSHEET_BODY = {
    'properties': {
        'title': '',
        'locale': ''
    },
    'sheets': [
        {'properties': {
            'sheetType': '',
            'sheetId': '',
            'title': '',
            'gridProperties': {
                'rowCount': '',
                'columnCount': ''
            }
        }
        }
    ]
}
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key.replace('\\n', '\n'),
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}