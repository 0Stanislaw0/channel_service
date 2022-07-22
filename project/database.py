from typing import List
from datetime import datetime, timedelta
from sqlalchemy import create_engine, insert, select, func
from sqlalchemy import Column, Integer, DateTime, DECIMAL, Date
from sqlalchemy.orm import declarative_base
from loguru import logger

#engine = create_engine('postgresql+psycopg2:'
           #           '//postgres:uorm9074@localhost:5432/postgres')

engine = create_engine('postgresql+psycopg2:'
                      '//postgres:qwerty19ytrewq@db:5432/postgres')


engine.connect().execute("SET DateStyle TO European;")

Base = declarative_base()


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    dollar_value = Column(DECIMAL)
    rubles_value = Column(DECIMAL)
    date = Column(Date)
    datetime = Column(DateTime)  # Поле для хранения версии Sheets


@logger.catch
def get_delivery_times() -> List[str]:
    """Получение даты последней модификации"""

    query = select([
        Order.date, Order.order, func.max(Order.datetime)
    ]).group_by(Order.date, Order.order)

    result = engine.execute(query).fetchall()
    delivery_times = []
    now = datetime.now().date()
    for record in result:
        if record[0] is not None:
            if now + timedelta(days=5) >= record[0] >= now:
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

    for record in result:
        if record[0]:
            return record[0]
        else:
            return datetime(2020, 1, 1)


@logger.catch
def write_to_db(data: List[List[object]], date: str) -> None:
    """Запись в бд"""

    conn = engine.connect()
    for row in data:
        ins = insert(Order).values(order=row[1], dollar_value=row[2],
                                   date=row[3], rubles_value=row[4],
                                   datetime=date)
        conn.execute(ins)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
