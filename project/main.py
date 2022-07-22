from googleapiclient.errors import HttpError
from loguru import logger
from requests import HTTPError
import ischedule

from auth import service_drive, service_sheets, credentials
from currency import get_currency
from database import get_last_modified_db, write_to_db
from proccesing_data import processing_data
from tlg_bot import bot, send

logger.add("main.log", format="{time} {level} {message}", level="DEBUG",
           rotation="100 Mb", compression="zip")


def main():
    creds, date, values, actual_currency = None, None, None, None

    try:
        creds = credentials()
    except FileNotFoundError as fnf:
        logger.error(f" {fnf}")

    try:
        date = service_drive(creds)
    except HttpError as he:
        logger.error(f"{he}")
    except ValueError as ve:
        logger.error(f"{ve}")

    try:
        values = service_sheets(creds)
    except HttpError as he:
        logger.error(f"{he}")
    except ValueError as ve:
        logger.error(f"{ve}")

    date = date.replace(microsecond=0)

    try:
        actual_currency = get_currency()
    except HTTPError:
        logger.error("Не удалось получить ответ от ЦБ: "
                     "{e.response.status_code}")

    valid_data = processing_data(values, actual_currency)
    last_modified_db = get_last_modified_db()
    if last_modified_db <= date:
        write_to_db(valid_data, date.strftime('%d-%m-%Y %H:%M:%S'))
        send()


ischedule.schedule(main, interval=2 * 60)
ischedule.schedule(send, interval=86400)

# TODO: завернуть в докер


if __name__ == '__main__':
    logger.debug("start")
    ischedule.run_loop()
