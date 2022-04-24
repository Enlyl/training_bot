import telebot
from telebot import types
from config import TOKEN, API_KEY
from pyowm import OWM
from pyowm.utils import config


bot = telebot.TeleBot(token=TOKEN)


def get_weather_at_city(city):
    conf = config.get_default_config()
    conf['language'] = 'ru'

    owm = OWM(API_KEY, config=conf)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather

    detailed_status = w.detailed_status
    wind = w.wind()['speed']
    temp = w.temperature('celsius')['temp']

    output = f'В городе {city} сейчас {detailed_status}\n Скорость ветра: {wind} м/с\nТемпература {temp} ℃'

    return output


def get_city(message: types.Message):
    chat_id = message.chat.id
    city = message.text
    output = get_weather_at_city(city)

    bot.send_message(chat_id=chat_id, text=output)


@bot.message_handler(commands=['weather'])
def weather(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Введите название название города')
    bot.register_next_step_handler(message, get_city)


if __name__ == '__main__':
    bot.infinity_polling()