import telebot
import os

bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))

    
@bot.message_handler(commands=['start'])
def start_handler(message):
    predicted_orders =  predict_orders(model)
    bot.send_message(chat_id = message.chat.id, text=f"The predicted number of orders is {predicted_orders}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

