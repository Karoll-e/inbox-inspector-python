import os

import telebot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Hola! Yo estare encargado de que estes informado con todo lo que esta pasando en el market!")


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(
        message,
        "Puedes interactuar conmigo usando comandos. Por ahora, solo respondo a /start y /help /news",
    )

@bot.message_handler(commands=["news"])
def send_news(message):
    bot.reply_to(
        message,
        "here you got today news",
    )


if __name__ == "__main__":
    bot.polling()
