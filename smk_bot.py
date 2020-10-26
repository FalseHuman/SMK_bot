import telebot
from telebot import types
import time
import pars



bot = telebot.TeleBot('Your token')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Проверить')
    markup.add(btn1)
    send_message = f"<b>Привет {message.from_user.first_name}!</b>\nЭтот бот создан для получения расписания с сайта колледжа. " \
        f"Для того, чтобы получить расписание напиши 'Проверить' или нажми соответсвующую кнопку.\n"
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "проверить":
        final_message =f"<u>Вот акктуальное расписание на неделю:</u>\n<a>{pars.pars(get_message_bot)}</a>"

    else:
        final_message = "<a>Некорректный запрос</a>"
    
    bot.send_message(message.chat.id, final_message, parse_mode='html')

while True:
    try:
        bot.polling(none_stop=True)#Это нужно чтобы бот работал всё время

    except:
        time.sleep(5)#если ошибка бот уходит в спящий режим на 5 секунд
