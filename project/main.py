from datetime import datetime
from typing import List, Any

from httplib2 import FailedToDecompressContent

from googleapiclient.errors import HttpError
from loguru import logger
from requests import HTTPError
import ischedule

from auth import service_drive, service_sheets, credentials
from currency import get_currency
from database import get_last_modified_db, write_sheet
from proccesing_data import processing_data
from tlg_bot import bot, send

logger.add("main.log", format="{time} {level} {message}", level="DEBUG",
           rotation="100 Mb", compression="zip")


def main(first_start:bool = None):
    creds, date, values, actual_currency = None, None, None, None

    try:
        creds: Any = credentials()
    except FileNotFoundError as fnf:
        logger.error(f" {fnf}")

    try:
        date: datetime = service_drive(creds).replace(microsecond=0)
    except HttpError as he:
        logger.error(f"{he}")
    except ValueError as ve:
        logger.error(f"{ve}")

    try:
        values: List[List] = service_sheets(creds)
    except HttpError as he:
        logger.error(f"{he}")
    except ValueError as ve:
        logger.error(f"{ve}")

    try:
        actual_currency: float = get_currency()
    except HTTPError:
        logger.error("Не удалось получить ответ от ЦБ: "
                     "{e.response.status_code}")

    valid_data: List[List] = processing_data(values, actual_currency)
    last_modified_db: datetime = get_last_modified_db()
    if first_start:
        write_sheet(valid_data, date.strftime('%d-%m-%Y %H:%M:%S'))
        first_start = False
    elif not first_start and last_modified_db < date:
        write_sheet(valid_data, date.strftime('%d-%m-%Y %H:%M:%S'))
        send()


ischedule.schedule(main, interval=2 * 10)
ischedule.schedule(send, interval=86400)


if __name__ == '__main__':
    logger.debug("start")
    main(True)
    ischedule.run_loop()
