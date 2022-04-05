#TimeColonistBot
import time, threading, schedule
 
from telebot import TeleBot

API_TOKEN = 'API_TOKEN'
bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет колонист! Используй /set <минуты> для отсчета до начала ГНОБИ")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text=('ПОРА ГНОБИТЬ!'))


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        minutes = int(args[1])
        schedule.every(minutes).minutes.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
