import re
from typing import List
from loguru import logger

pattern_date: str = "(0[0-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}"


def processing_data(data: List[List], currency: float) -> List[List]:
    """ Обработка данных """
    new_data = []
    for row in data:
        error = 0
        try:
            row[1] = int(row[1])
            row[2] = float(row[2])
            if re.findall(pattern_date, row[3]):
                row[3] = row[3].replace(".", "-")
            else:
                raise ValueError

        except ValueError:
            logger.error(f"Неверный формат данных в строке: {row}")
            error += 1

        if error > 0:
            logger.error(f"Найдено  ошибок {error}."
                         f"Строка {row} записана в бд не будет")
        else:
            ruble: float = currency * float(row[2])
            row.append(ruble)
            new_data.extend([row])
    return new_data