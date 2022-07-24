from datetime import datetime
from typing import List

from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']

SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '1G-MFMLZh4SPuFKPBK31YLahFoklKVCMgy0aAqUiuwDI'
RANGE = 'A2:Z1000'


def credentials() -> Credentials:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds


def service_drive(creds: Credentials) -> datetime:
    date = None
    service_drive = build('drive', 'v3', credentials=creds)
    response = service_drive.files().list(
        pageSize=5,
        fields="nextPageToken, files(*)").execute()

    for file in response.get('files', {}):
        sheet_id = file.get("id",None)
        if sheet_id ==SPREADSHEET_ID:
            date = datetime.fromisoformat(file.get("modifiedTime")[:-1])
            break

    if not date:
        raise ValueError("Не удалось получить дату изменения файла")
    else:
        return date


def service_sheets(creds: Credentials) -> List[List]:
    service_sheet = build('sheets', 'v4', credentials=creds)
    sheet = service_sheet.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE).execute()

    values = result.get('values', [])

    if not values:
        raise ValueError("Не удалось получить данные в Google Sheets")
    else:
        return values
