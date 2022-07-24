from typing import List
from datetime import datetime
from sqlalchemy import create_engine, insert, select, func, distinct
from sqlalchemy import Column, Integer, DateTime, DECIMAL, Date
from sqlalchemy.orm import declarative_base
from loguru import logger

from sqlalchemy.sql import text


engine = create_engine('postgresql+psycopg2:'
                      '//postgres:qwerty19ytrewq@db:5432/postgres')


Base = declarative_base()


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    dollar_value = Column(DECIMAL)
    rubles_value = Column(DECIMAL)
    date = Column(Date)
    datetime = Column(DateTime)  # Поле для хранения версии Sheets


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)


@logger.catch
def write_user(id: str) -> None:
    """Запись пользователя который подписался на рассылку уведoмлений"""

    conn = engine.connect()
    insert_user = insert(User).values(chat_id=id)
    conn.execute(insert_user)

    return None


@logger.catch
def get_users() -> List[int]:
    """Получение списка пользователей"""

    query = select(distinct(User.chat_id))

    result = engine.execute(query).fetchall()
    users = [] 

    for record in result:
        if record[0] is not None:
            users.append(record[0])
    return users

# TODO add func del from user



@logger.catch
def get_delivery_times() -> List[str]:
    """Получение cроков поставки"""

    query = select([
        Order.date, Order.order, func.max(Order.datetime)
    ]).group_by(Order.date, Order.order)

    result = engine.execute(query).fetchall()
    delivery_times = []
    now = datetime.now().date()
    for record in result:
        if record[0] is not None:
            if now > record[0]:
                d = record[0].strftime('%d-%m-%Y')
                delivery_times.append(f"номер заказа {record[1]}"
                                      f",cрок поставки {d}")
    return delivery_times


@logger.catch
def get_last_modified_db() -> datetime:
    """Получение даты последней модификации"""

    query = select([
        func.max(Order.datetime)
    ])
    result = engine.execute(query).fetchall()

    print
    for record in result:
        if record[0]:
            return record[0]
        else:
            return datetime(2020, 1, 1)

@logger.catch
def write_sheet(data: List[List[object]], date: str) -> None:
    """обновление таблицы"""

    for row in data:
        ins = insert(Order).values(order=row[1], dollar_value=row[2],
                                   date=func.to_date(row[3], 'DD-MM-YYYY'), rubles_value=row[4],
                                   datetime=func.to_date(date, 'DD-MM-YYYY HH24:MI:SS'))
                                   
        engine.execute(ins)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    

