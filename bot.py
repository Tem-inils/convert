import telebot
from telebot import types
import requests

bot = telebot.TeleBot('6449422166:AAGCbP8xQUa9ZNrxYPanrSAojupX8dZifHw')
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет введите сумму')
    bot.register_next_step_handler(message, summa)
def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Пишите сумму')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 1:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/UZS', callback_data='usd/usz')
        btn2 = types.InlineKeyboardButton('UZS/USD', callback_data='uzs/usd')
        btn3 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть > 1')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        url = f'https://api.exchangerate.host/convert?from={values[0]}&to={values[1]}'
        response = requests.get(url)
        data = response.json()
        rate = data['info']['rate']
        res = amount * rate
        bot.send_message(call.message.chat.id, f'Полуается:{round(res, 2)}')
        bot.register_next_step_handler(call.message.chat.id, summa)

    else:
        bot.send_message(call.message.chat.id, f'Введите пару значение через / ')
        bot.register_next_step_handler(call.message, my_cur)

def my_cur(message):
    values = message.text.upper().split('/')
    url = f'https://api.exchangerate.host/convert?from={values[0]}&to={values[1]}'
    response = requests.get(url)
    data = response.json()
    rate = data['info']['rate']
    res = amount * rate
    bot.send_message(message, f'Полуается:{round(res, 2)} ')
    bot.register_next_step_handler(message, summa)
bot.polling(none_stop=True)