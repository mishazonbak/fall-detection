import telebot
import qrcode


bot = telebot.TeleBot("6539441771:AAGigJ7cDkKrIUGq8WpHMVvtWOAB5tGbU20")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, ваш ID: {message.from_user.id}, он нужен для рассылки")
    user_id = message.from_user.id
bot.polling()