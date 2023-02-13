import telebot
import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load the data
df = pd.read_csv("taxi_orders.csv")

# Preprocessing the data
# convert time column to datetime type
df['datetime'] = pd.to_datetime(df['datetime'])
# set time as the index
df.set_index('datetime', inplace=True)
# resample the data to get the number of orders every hour
df_hourly = df.resample('1H').sum()

# Create new features
df_hourly['hour'] = df_hourly.index.hour
df_hourly['day_of_week'] = df_hourly.index.dayofweek
df_hourly['month'] = df_hourly.index.month
df_hourly['season'] = (df_hourly.index.month%12 + 3)//3

# Split the data into training and testing sets
train_data, test_data = train_test_split(df_hourly, test_size=0.2)

# Create the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
X_train = train_data[['hour', 'day_of_week', 'month', 'season']]
y_train = train_data['num_orders'].values
model.fit(X_train, y_train)

def predict_orders(model, df):
    now = datetime.datetime.now()
    hour = now.hour + 1
    day_of_week = now.weekday()
    month = now.month
    season = determine_season(month)
    
    features = [hour, day_of_week, month, season]
    prediction = model.predict([features])
    
    return prediction[0]


def determine_season(month):
    if month >= 3 and month <= 5:
        return 1
    elif month >= 6 and month <= 8:
        return 2
    elif month >= 9 and month <= 11:
        return 3
    else:
        return 4

TELEGRAM_TOKEN = '6191497935:AAGX3CjSNwEhWhLiyqgRT7a90iuSSA2Sptk'

bot = telebot.TeleBot(os.environ.get(TELEGRAM_TOKEN))

    
@bot.message_handler(commands=['start'])
def start_handler(message):
    predicted_orders =  predict_orders(model)
    bot.send_message(chat_id = message.chat.id, text=f"The predicted number of orders is {predicted_orders}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

