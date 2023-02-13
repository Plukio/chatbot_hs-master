import telebot
import openai
import os

bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))
openai.api_key = os.environ.get("OPENAI_TOKEN")


@bot.message_handler(commands=['start'])
def start(m, res=False):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="what is an elephant?",
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text
    bot.send_message(m.chat.id, response)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

