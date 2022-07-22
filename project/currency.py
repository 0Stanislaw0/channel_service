from typing import Union

import requests
import xml.etree.ElementTree as ET
from loguru import logger


@logger.catch
def get_currency() -> Union[float, tuple[None, str], None]:
    """Получение актуальной валюты с сайта ЦБ России"""

    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    if response.status_code == 200:
        tree = ET.fromstring(response.content)
        target = None
        for ind, child in enumerate(tree.iter("*")):
            if target == ind:
                return float(child.text.replace(",", "."))
            if child.text == "Доллар США":
                target = ind + 1
        raise ValueError("Не удалось получить актуальный курс")
    else:
        response.raise_for_status()
