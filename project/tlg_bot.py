from database import get_delivery_times
import telebot

bot = telebot.TeleBot("5460284921:AAF8U97n3y5Qe31qQgUtN3tBbgo_Mw3oo0g")


@bot.message_handler(content_types=['text'])
def start(message):
    with open('subscribed_users.txt', mode='a+') as f:
        f.write(str(message.from_user.id) + "\n")

    bot.send_message(message.from_user.id,
                     f'Привет {message.from_user.first_name}. '
                     'Добавлю тебя в список тех, кто следит '
                     'за сроками поставки')


def send():
    with open('subscribed_users.txt', mode='r') as f:
        users = f.read()
    delivery_time = get_delivery_times()
    for user in set(users.strip().split("\n")):
        bot.send_message(user, "\n".join(delivery_time))

if __name__=="__main__":
    bot.polling(none_stop=True, interval=0)
