import telebot
from telebot import types
import time
import os

''' Воскресенская солянка '''
from bs4 import BeautifulSoup
import requests

url = 'http://salavatmk.ru/raspisanie.php'
post = []

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")


def pars(message_user):
    if page.status_code == 200: #проверка соединения с сайтом
        for a in soup.find_all('a', href=True):
            if '.pdf' in a['href'] and message_user == 'проверить':
                post.append(f"http://salavatmk.ru{a['href']}")
        
        if len(post) == 0:# если нет расписания
            return f"На сайте еще нет расписания"
        else:
            return post[-1]
    else:#ошибка если дисконнект
        return f"Ошибка соединения с сайтом"


token = os.environ.get('TOKEN')
bot = telebot.TeleBot(str(token))

owner = 741541899


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	btn1 = types.KeyboardButton('Проверить')
	markup.add(btn1)
	send_message = f"<b>Привет {message.from_user.first_name}!</b>\nЭтот бот создан для получения расписания с сайта колледжа. " \
		f"Для того, чтобы получить расписание напиши 'Проверить' или нажми соответсвующую кнопку.\nДля обратной связи со мной /Helpme(Пример: /Helpme Описание проблемы)"
	bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['Helpme'])
def messages(message):
	if int(message.chat.id) == owner:
		try:
			bot.send_message(message.chat.id, 'Сообщение от администратора было получено')
		except:
			bot.send_message(owner, 'Что-то пошло не так! Бот продолжил свою работу.' + ' Ошибка произошла в блоке кода:\n\n <code>@bot.message_handler(content_types=["callback"])</code>', parse_mode='HTML')
	else:
		pass
		try:
			bot.forward_message(owner, message.chat.id, message.message_id)
			bot.send_message(message.chat.id, str(message.from_user.first_name) + ',' +' я получил сообщение и очень скоро на него отвечу :)')
		except:
			bot.send_message(owner, 'Что-то пошло не так! Бот продолжил свою работу.')


@bot.message_handler(commands=['send'])
def process_start(message):
	if int(message.chat.id) == owner:
		try:
			bot.send_message(message.chat.id, 'Для отправки сообщения сделай /send')
			bot.forward_message(owner, message.chat.id, message.message_id)
			bot.register_next_step_handler(message, process_mind)
		except:
			bot.send_message(message.chat.id, "Что-то пошло не так! Ошибка возникла в блоке кода:\n<code>@bot.message_handler(commands=['send_message'])</code>", parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, 'Вы не являетесь администратором для выполнения этой команды!')
def process_mind(message):
	if int(message.chat.id) == owner:
		try:
			text = 'Сообщение было отправлено пользователю ' + str(message.reply_to_message.forward_from.first_name)
			bot.forward_message(message.reply_to_message.forward_from.id, owner, message.message_id)
			bot.send_message(owner, text)
		except:
			bot.send_message(message.chat.id, 'Что-то пошло не так! Бот продолжил свою работу.' + ' Ошибка произошла в блоке кода:\n\n <code>def process_mind(message)</code>', parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, 'Вы не являетесь администратором для выполнения этой команды!')

@bot.message_handler(content_types=['text'])
def mess(message):
	final_message = ""
	get_message_bot = message.text.strip().lower()
	if get_message_bot == "проверить":
		final_message =f"<u>Вот акктуальное расписание на неделю:</u>\n<a>{pars(get_message_bot)}</a>"		
	else:
		final_message = "<a>Некорректный запрос</a>"
	bot.send_message(message.chat.id, final_message, parse_mode='html')
while True:
    try:
        bot.polling(none_stop=True)#Это нужно чтобы бот работал всё время

    except:
        time.sleep(5)#если ошибка бот уходит в спящий режим на 5 секунд
