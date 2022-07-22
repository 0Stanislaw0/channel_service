from datetime import datetime
from typing import List

from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']

SERVICE_ACCOUNT_FILE = 'credentials.json'
SAMPLE_SPREADSHEET_ID = '1G-MFMLZh4SPuFKPBK31YLahFoklKVCMgy0aAqUiuwDI'
SAMPLE_RANGE_NAME = 'A2:Z1000'


def credentials() -> Credentials:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds


def service_drive(creds: Credentials) -> datetime:
    date = None
    files = []
    service_drive = build('drive', 'v3', credentials=creds)
    response = service_drive.files().list(
        pageSize=5,
        fields="nextPageToken, files(*)").execute()
         # TODO: Нужно конректно с нашего sheets  тянуть время
    for file in response.get('files', []):
        date = datetime.fromisoformat(file.get("modifiedTime")[:-1])
    files.extend(response.get('files', []))
    if not date:
        raise ValueError("Не удалось получить дату изменения файла")
    else:
        return date


def service_sheets(creds: Credentials) -> List[List]:
    service_sheet = build('sheets', 'v4', credentials=creds)
    sheet = service_sheet.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()

    values = result.get('values', [])

    if not values:
        raise ValueError("Не удалось получить данные в Google Sheets")
    else:
        return values
