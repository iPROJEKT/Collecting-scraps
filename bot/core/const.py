LOG_FORM = '%(asctime)s, %(levelname)s, %(message)s'
LOG_FILEMOD = 'w'
LOG_FILENAME = 'logger.log'
TOKEN_EXECT = 'Token is invalid!'
A1 = 'Отчет от'
A2 = 'Номер установк'
B2 = 'Что случились (наименование дефекта)'
C2 = 'Кто зафиксировал'
D2 = 'Развернутое пояснение'
E2 = 'Имя программа'
F2 = 'Координаты'
G2 = 'Во сколько зарегистрировали'
FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_TITLE = 'Отчет от {}'
LOCALE = 'ru_RU'
SHEET_TITLE = 'Регистация дефектов'
ROW_COUNT = 50
COLUMN_COUNT = 9
RANGE = r'A1:G50'
SHEERTYPE = 'GRID'
TYPE = 'user'
ROLE = 'writer'
TABLE_UPDATA = 'ROWS'
FILDS_FOR_SERVIS_ACCOUNT = 'id'
SHEERTID = 0
ROW_COUNT_ERROR = 'Слишком много дефектов'
COLUMN_COUNT_ERROR = 'В таблице всего 7 столбцов'
TABLE_VALUES = [
    [A1],
    [A2, B2, C2, D2, E2, F2, G2]
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