from google.oauth2.service_account import Credentials
from googleapiclient import discovery


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

