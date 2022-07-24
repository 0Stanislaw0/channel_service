from typing import List

from database import get_delivery_times, write_user, get_users
from loguru import logger
import telebot

bot = telebot.TeleBot("5460284921:AAF8U97n3y5Qe31qQgUtN3tBbgo_Mw3oo0g")


@bot.message_handler(content_types=['text'])
def subscription(message):
    """Добавляет пользователя в список рассылки"""

    logger.debug(f"Пользователь {message.from_user.first_name} подписался")

    write_user(message.from_user.id)
    bot.send_message(message.from_user.id,
                     f'Привет {message.from_user.first_name}. '
                     'Добавлю тебя в список тех, кто следит '
                     'за сроками поставки')


def send():
    """Отправка уведомлений пользователям о сроках поставок"""

    logger.debug("Уведомляем пользователей о поставках")

    delivery_time: List[str] = get_delivery_times()
    users = get_users()
    for user in users:
        bot.send_message(user, "\n".join(delivery_time))

if __name__=="__main__":
    bot.polling(none_stop=True, interval=0)
