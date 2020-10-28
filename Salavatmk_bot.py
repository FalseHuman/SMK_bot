import telebot
from telebot import types
import time
import pars



bot = telebot.TeleBot('Ваш API-ключ')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Проверить')
    btn2 = types.KeyboardButton('Обратная связь')
    markup.add(btn1, btn2)
    send_message = f"<b>Привет {message.from_user.first_name}!</b>\nЭтот бот создан для получения расписания с сайта колледжа. " \
        f"Для того, чтобы получить расписание напиши 'Проверить' или нажми соответсвующую кнопку.\n"
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "проверить":
        final_message =f"<u>Вот акктуальное расписание на неделю:</u>\n<a>{pars.pars(get_message_bot)}</a>"
    elif get_message_bot == 'обратная связь':
        final_message = f"Тест"

    else:
        final_message = "<a>Некорректный запрос</a>"
    
    bot.send_message(message.chat.id, final_message, parse_mode='html')

while True:
    try:
        bot.polling(none_stop=True)#Это нужно чтобы бот работал всё время

    except:
        time.sleep(5)#если ошибка бот уходит в спящий режим на 5 секунд