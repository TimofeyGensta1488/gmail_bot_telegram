# -*- coding: utf-8 -*-
# Модули
try:
	import telebot
	import smtplib,ssl 
	import time 
	import os
	from email.mime.text import MIMEText # Для отправки текста
	from email.mime.multipart import MIMEMultipart
	from telebot import types # Кнопки
	from random import randint,choice,randrange 
	from email.mime.application import MIMEApplication # Для отправки файлов
	import config3 # Токен бота
	import requests # Для получения данных с сайта
	import pyowm # Модуль для роботы с погодой
	from bs4 import BeautifulSoup as bs # Парсинг курса доллара
	from firebase import firebase # Подключаю базу данных, чтоб записать данные пользователя
	import firebase_admin
	from firebase_admin import credentials
	from firebase_admin import db
	import mimetypes
	import base64

except ImportError as e:
	print("Какой-то модуль не заработал !! ")

cred = credentials.Certificate("telergram_bot_key.json")
firebase_admin.initialize_app(cred,{
	"databaseURL":"https://bot--telegram-228.firebaseio.com/"
	})

images_formats = ".bmp",".jpg",".png",".gif",".jpeg",".tif"
files_formats = ".txt",".doc",".rtf",".docx"
tables_formats = ".csv",".xls",".xlsx",".xlsm",".ods"
archive_formats = ".rar",".zip",".tg"

# ref = db.reference('/')


ref = db.reference('my_data')
ref_data = ref.get()

# Токен
bot = telebot.TeleBot(config3.TOKEN)

HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'} # User-Agent, чтоб сайт распозновал меня как юзера
url_usa = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&rlz=1C1SQJL_enUA884UA884&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&aqs=chrome.0.69i59j0l7.4996j1j7&sourceid=chrome&ie=UTF-8' # Ссылка на сайт
page_usa = requests.get(url_usa,headers = HEADERS)
soup = bs(page_usa.content,'lxml')

owm = pyowm.OWM('ff46a20765614ebaf32f1ed12e89bb0e', language = "RU") # Создаём аккаунт на OpenWeatherMap и вставляем APi-ключ сюда

user_dict = {} # Словарь для хранения информации.После перезапуска всё удаляется
user_photo = {} # Словарь для хранения фото от пользователя.Тоже удаляется после перезапуска

teach = {'nem': 'pipoks@meta.ua','fiz':"anisimovakm@ukr.net",'geo':"zazymko69@ukr.net",'ukr':"lubovsan282@gmail.com",'my':"kupruhintimofej@gmail.com"} # Этот словарь хранит ключи с почтами

markup_types = types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True)
btn_1 = types.KeyboardButton('Документ')
btn_2 = types.KeyboardButton('Фото')
btn_3 = types.KeyboardButton('Аудио')
markup_types.add(btn_1,btn_2,btn_3)

# Клавиатуры
markup_exit = types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True)
button1 = types.KeyboardButton('Отменить отправку.')	
markup_exit.add(button1)

markup = types.ReplyKeyboardRemove(selective = False) # Для удаления клавиатуры 

markup_mess1 = types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True,row_width = 2)

button1 = types.KeyboardButton('Добавить.')
button2 = types.KeyboardButton('Отправить.')
button3 = types.KeyboardButton('Отменить отправку.')
markup_mess1.add(button1,button2,button3)

markup_mess2 = types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True,row_width = 1)

button4 = types.KeyboardButton('Оставить сообщение пустым.')
button2 = types.KeyboardButton('Отменить отправку.')
markup_mess2.add(button4,button2)

markup_gmails = types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True,row_width = 3)

button1 = types.KeyboardButton('Немецкий')
button2 = types.KeyboardButton('Отменить отправку.')
button3 = types.KeyboardButton('Физ-ра')
button4 = types.KeyboardButton('География')
button5 = types.KeyboardButton('Украинский')
button6 = types.KeyboardButton('Моя почта вторая')
markup_gmails.add(button1,button6,button3,button4,button5,button2)

markup_gdz = types.InlineKeyboardMarkup(row_width = 2)

btn = types.InlineKeyboardButton('Геометрия', url = 'https://vshkole.com/8-klass/reshebniki/geometriya/ag-merzlyak-vb-polonskij-ms-yakir-2016')
btn2 = types.InlineKeyboardButton('Алгебра', url = 'https://vshkole.com/8-klass/reshebniki/algebra/ag-merzlyak-vb-polonskij-ms-yakir-2016')
btn3 = types.InlineKeyboardButton('Знания.com', url = 'https://znanija.com/')
markup_gdz.add(btn,btn2,btn3)

# Классы
class User:
	def __init__(self,login):

		self.login = login
		keys = ['password','tema','message2','message3','message4','message5','tosomeone'] # Значения для регистрации

		for key in keys:
			self.key = None # Каждое из них равняется None

class User2:
	def __init__(self,photo1):
		self.photo1 = photo1
		keys = ['photo2','photo3','photo4','photo5'] # Фото

		for key in keys:
			self.key = None

@bot.message_handler(commands=["course"])
def dollar(message):

	us = soup.findAll('div',class_ = 'dDoNo vk_bk gsrt gzfeS') # Получаем блок div
	for dollar in us:
		curs_us = dollar.find('span',{'class':"DFlfde SwHCTb"}).get("data-value")
	bot.send_message(message.chat.id,"Курс доллара в гривны: {0}".format(curs_us)) # Выводим значение курса
	
@bot.message_handler(commands=["GDZ"])
def gdz(message):

	bot.send_message(message.chat.id,'ГДЗ 8 класс: геометрия, алгебра и сайт "Знания":',reply_markup = markup_gdz)

@bot.message_handler(commands=["weather"])

def weather(message):
	
	msg = bot.send_message(message.chat.id,'Напишите свой город.')
	bot.register_next_step_handler(msg,weather2) # Записываем город 

def weather2(message):
	try:
		obs = owm.weather_at_place(message.text)
		w = obs.get_weather() # Получаем статус погоды

		fc = owm.three_hours_forecast(message.text) # Для прогноза на завтра
		f = fc.get_forecast()

		bot.send_message(message.chat.id,"Температура в городе {0}  {1} °C. ".format(message.text,w.get_temperature('celsius')['temp'])) # Отображаем температуру
		bot.send_message(message.chat.id,"Статус погоды: {}.".format(w.get_detailed_status()),reply_markup = markup) #  Отображаем статус погоды

		for weather in f:
			pass
		bot.send_message(message.chat.id,'Завтра будет {0} °C.'.format(weather.get_temperature('celsius')['temp'])) # Прогноз на завтра  

	except pyowm.exceptions.api_response_error.NotFoundError as e:
		bot.reply_to(message,"Такого города не существует!!!") # Ловим ошибку, если pyowm не нашел города

@bot.message_handler(commands=["rand"])

def random(message):

	markup_rand = types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True)  # Ещё одна клавиатура
	button1 = types.KeyboardButton('Генерация рандомного числа')
	markup_rand.add(button1)

	try:
		msg = bot.send_message(message.chat.id,"Сгенерировать случайное число?",reply_markup = markup_rand)
		bot.register_next_step_handler(msg,random2)

	except Exception as e:
		bot.reply_to(message,"Что-то неправильно.")

def random2(message):
	mess = message.text

	markup_chrom = types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True) # CREATING SECOND KEYBOARD
	button1 = types.KeyboardButton('Да')
	button2 = types.KeyboardButton('Нет')
	markup_chrom.add(button1,button2)

	if mess == "Генерация рандомного числа":
		bot.send_message(message.chat.id,"Рандомное число:")
		bot.send_message(message.chat.id,(str(randint(1,500)))) # GENERATION NUMBER

	else:
		bot.send_message(message.text.id,"Такого я не понимаю.")

	try:
		msg = bot.send_message(message.chat.id,'Хотите узнать количество ваших хромосом?',reply_markup = markup_chrom) 
		bot.register_next_step_handler(msg,random3)

	except Exception as e:
		bot.reply_to(message,"Что-то неправильно.")	

def random3(message):
	mess = message.text
	gif = "https://s4.gifyu.com/images/giphye1d7533ba6e2ff97.gif" # Ссылка на Gif
	ans = 'Да','Нет','нет','НЕТ','да','ДА' # Возможные ответы 

	if mess.startswith(ans): # Если сообщение начинается с таких слов то:
		bot.send_message(message.chat.id,"Поздравляю! {0} {1}, у вас 47 хромосом !!!".format(message.chat.first_name,message.chat.last_name)) 
		bot.send_video(message.chat.id,gif) # Отправляем гифку

	else:
		bot.send_message(message.text.id,"Такого я не понимаю.")

# THE NEXT COMMAND 'SEND'
@bot.message_handler(commands=["send"])

def send_message(message):
	chat_id = message.chat.id
	user_id = message.from_user.id
	try:
		if user_id == 1074201738:
			msg = bot.send_message(message.chat.id,'Можешь ввести свою почту:',reply_markup = markup_exit)
		
		else:
			bot.send_message(chat_id,"Команда недоступна.")

	except Exception as e:
		bot.send_message(chat_id,"Возникла ошибка с регистрацией")

	
	bot.register_next_step_handler(msg,ret) # Переход в другую функцию
		
def ret(message):
	gmails = "@gmail.com","@ukr.net","@meta.ua"
	mess = message.text
	message.text.split()
	
	if mess.startswith('Отменить отправку.'): # Если пользователь нажал на кнопку, то цикл останавливается
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup) # Убираем клавиатуру когда цикл закончился
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id) # Останавливаем цикл

	else:

		# try:
		chat_id = message.chat.id
		user_dict[chat_id] = User(ref_data["my_email"]) # Передаем значение в класс, а потом в словарь 

		msg = bot.send_message(message.chat.id,'Можешь ввести свой пароль:',reply_markup = markup_exit) # Спрашиваем пароль
		bot.register_next_step_handler(msg,ret4)

		# except Exception as e:
		# 	bot.reply_to(message,'Что-то неправильно!!!',reply_markup = markup)
		

def ret4(message):
	user_id = message.from_user.id
	mess = message.text
	chat_id = message.chat.id
	user = user_dict[chat_id]

	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)

	else:	

		# try:
		if user_id == 1074201738:
			user.password = ref_data["pass_"]
				
		else:
			user.password = message.text
			bot.delete_message(message.chat.id, message.message_id) #  Удаляем сообщение, чтобы пароль нельзя было увидеть
		
		msg = bot.send_message(message.chat.id,'<strong>Введите получателя:</strong>', parse_mode = 'html',reply_markup = markup_gmails) # Спрашиваем получателя
		bot.register_next_step_handler(msg,ret2)

		# except Exception as e:
		# 	bot.reply_to(message,'Что-то неправильно!!!',reply_markup = markup)
		

def ret2(message):

	chat_id = message.chat.id
	user = user_dict[chat_id]
	mess = message.text

	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
		

	else:
		# Берём значения из словаря "teach"
		if message.text == "Немецкий":
			user.tosomeone = teach["nem"]

		elif message.text == "Физ-ра":
			user.tosomeone = teach["fiz"]

		elif message.text == "География":
			user.tosomeone = teach["geo"]

		elif message.text == "Украинский":
			user.tosomeone = teach["ukr"]

		elif message.text == "Моя почта вторая":
			user.tosomeone = teach["my"]

		else:
			user.tosomeone = message.text

		# Новая клавиатура для темы сообщения
		markup_tema = types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True,row_width = 1)
		button = types.KeyboardButton('Продолжить без темы.')
		button2 = types.KeyboardButton('Отменить отправку.')
		markup_tema.add(button,button2)

		try:
			
			msg = bot.send_message(message.chat.id,"<b>Введите тему сообщения:</b>",parse_mode = 'html',reply_markup = markup_tema) # Спрашиваем тему сообщения
			bot.register_next_step_handler(msg,ret3)	

		except Exception as e:
			bot.reply_to(message,'Что-то неправильно!!!',reply_markup = markup)
		

def ret3(message):

	mess = message.text
	chat_id = message.chat.id
	user = user_dict[chat_id]

	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
		

	else:

		if message.text == 'Продолжить без темы.':
			user.tema = None

		else:
			user.tema = message.text

		try:		
			msg = bot.send_message(message.chat.id,"<b>Введите сообщение:</b>",parse_mode = 'html',reply_markup = markup_mess2) # Спрашиваем текст сообщения
			bot.register_next_step_handler(msg,nefinal)

		except Exception as e:
			bot.reply_to(message,'Что-то неправильно!!!',reply_markup = markup)	

def nefinal(message):

	mess = message.text
	chat_id = message.chat.id
	user = user_dict[chat_id]

	user.message2 = message.text

	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
		
	else:
		if message.text == "Оставить сообщение пустым.":
			user.message2 = ' ' 

		else:
			user.message2 = message.text

		msg = bot.send_message(message.chat.id,'Добавить что-то ещё?',reply_markup = markup_mess1) # Прикрепляем файлы
		bot.register_next_step_handler(msg,nefinal2)

def nefinal2(message):

	mess = message.text
	chat_id = message.chat.id
	user = user_dict[chat_id]
	
	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
		
	else:
		
		if message.text != "Добавить.":

			try:
				try:
					msg = MIMEMultipart()
					msg['Subject'] = user.tema	#  Тема
					msg["To"] = user.tosomeone # Кому
					msg['From'] = "Сool->" # От кого
					body = user.message2

					msg.attach(MIMEText(body)) # Отправляем сообщение

					context = ssl.create_default_context() # Для болеей надёжной защиты
					server = smtplib.SMTP('smtp.googlemail.com',587) # Порт
					server.starttls(context = context)
					server.ehlo()
					server.login(user.login,user.password) # Логинимся
					server.sendmail(user.login,user.tosomeone,msg.as_string()) # Отправляем
					bot.send_message(message.chat.id,'Сообщение успешно отправлено.',reply_markup = markup)
					server.quit() # Закрываем сервер

				except smtplib.SMTPAuthenticationError as e:
					bot.send_message(message.chat.id,"Вы ввели недействительный адрес или пароль!!!",reply_markup = markup)# Ловим ошибку, если пользователь ввёл неправильные данные
			except smtplib.SMTPRecipientsRefused as e:
				bot.send_message(message.chat.id,'Вы ввели недействительного получателя!!!')
		else:
			msg = bot.send_message(message.chat.id,"Прикрепите файл.",reply_markup = markup) 
			bot.register_next_step_handler(msg,nefinal_2)

def nefinal_2(message):
	chat_id = message.chat.id
	mess = message.text
	
	try:
		chat_id = message.chat.id
		file_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_info.file_path) # Бот загружает файл

		global file_type1
		file_type1 = file_info.file_path
		file_type1 = file_type1.split("/")
		file_type1 = file_type1[-1]

		user_photo[chat_id] = User2(downloaded_file) # Делаем так же как и с регистрацией
		user2 = user_photo[chat_id]

	except Exception as e:
		bot.send_message(message.chat.id,'Возникла ошибка с файлом',reply_markup = markup) 

	msg = bot.send_message(message.chat.id,'Добавить что-то ещё?',reply_markup = markup_mess1)
	bot.register_next_step_handler(msg,nefinal3)

	
def nefinal3(message):

	mess = message.text
	chat_id = message.chat.id
	
	user = user_dict[chat_id]
	user2 = user_photo[chat_id]
	
	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
		
	else:
		
		if message.text != "Добавить.":
			try:
				try:
					msg = MIMEMultipart()
					msg['Subject'] = user.tema	
					msg["To"] = user.tosomeone
					msg['From'] = "Сool->"

					body = user.message2

					part = MIMEApplication(user2.photo1) # Добавляем само фото
					
					part.add_header('Content-Disposition', 'attachment', filename=file_type1) # Здесь записываем название файла
					
					msg.attach(MIMEText(body))
					msg.attach(part) # Добаляем файл в сообщение
					

					context = ssl.create_default_context()
					server = smtplib.SMTP('smtp.googlemail.com',587)
					server.starttls(context = context)
					server.login(user.login,user.password)
					server.sendmail(user.login,user.tosomeone,msg.as_string())
					bot.send_message(message.chat.id,'Сообщение успешно отправлено.',reply_markup = markup)	
					server.quit()

				except smtplib.SMTPAuthenticationError as e:
					bot.send_message(message.chat.id,"Вы ввели недействительный адрес или пароль!!!",reply_markup = markup)
			except smtplib.SMTPRecipientsRefused as e:
				bot.send_message(message.chat.id,'Вы ввели недействительного получателя!!!')	
		else:
			msg = bot.send_message(message.chat.id,"Прикрепите файл:",reply_markup = markup)
			bot.register_next_step_handler(msg,nefinal_3)

def nefinal_3(message):
	
	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path) # Бот загружает файл
	
	global file_type2
	file_type2 = file_info.file_path
	file_type2 = file_type2.split("/")
	file_type2 = file_type2[-1]

	chat_id = message.chat.id
	user2 = user_photo[chat_id]
	user2.photo2 = downloaded_file

	msg = bot.send_message(message.chat.id,'Добавить что-то ещё?',reply_markup = markup_mess1)
	bot.register_next_step_handler(msg,nefinal4)

def nefinal4(message):

	mess = message.text
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user2 = user_photo[chat_id]
	
	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
		
	else:
		
		if message.text != "Добавить." :
			try:
				try:
					msg = MIMEMultipart()
					msg['Subject'] = user.tema	
					msg["To"] = user.tosomeone
					msg['From'] = "Сool->"

					body = user.message2

					part = MIMEApplication(user2.photo1)
					part2 = MIMEApplication(user2.photo2)

					part.add_header('Content-Disposition', 'attachment', filename=file_type1)
					part2.add_header('Content-Disposition', 'attachment', filename=file_type2)

					msg.attach(MIMEText(body))
					msg.attach(part)
					msg.attach(part2)

					context = ssl.create_default_context()
					server = smtplib.SMTP('smtp.googlemail.com',587)
					server.starttls(context = context)
					server.login(user.login,user.password)
					server.sendmail(user.login,user.tosomeone,msg.as_string())
					bot.send_message(message.chat.id,'Сообщение успешно отправлено.',reply_markup = markup)	
					server.quit()

				except smtplib.SMTPAuthenticationError as e:
					bot.send_message(message.chat.id,"Вы ввели недействительный адрес или пароль!!!",reply_markup = markup)
			except smtplib.SMTPRecipientsRefused as e:
				bot.send_message(message.chat.id,'Вы ввели недействительного получателя')	
		else:
			msg = bot.send_message(message.chat.id,"Прикрепите файл:",reply_markup = markup)
			bot.register_next_step_handler(msg,nefinal_4)

def nefinal_4(message):

	mess = message.text

	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path) # Бот загружает файл
	try:
		global file_type3
		file_type3 = file_info.file_path
		file_type3 = file_type3.split("/")
		file_type3 = file_type3[-1]

	except Exception as e:
		bot.send_message(message.chat.id,'Возникла ошибка с файлом',reply_markup = markup) 

	chat_id = message.chat.id
	user2 = user_photo[chat_id]
	user2.photo3 = downloaded_file

	msg = bot.send_message(message.chat.id,'Добавить что-то ещё?',reply_markup = markup_mess1)
	bot.register_next_step_handler(msg,nefinal5)

def nefinal5(message):

	mess = message.text
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user2 = user_photo[chat_id]
	
	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
		
	else:
		
		if message.text != "Добавить." :
			try:
				try:
					msg = MIMEMultipart()
					msg['Subject'] = user.tema	
					msg["To"] = user.tosomeone
					msg['From'] = "Сool->"

					body = user.message2

					part = MIMEApplication(user2.photo1)
					part2 = MIMEApplication(user2.photo2)
					part3 = MIMEApplication(user2.photo3)
					

					part.add_header('Content-Disposition', 'attachment', filename=file_type1)
					part2.add_header('Content-Disposition', 'attachment', filename=file_type2)
					part3.add_header('Content-Disposition', 'attachment', filename=file_type3)
				

					msg.attach(MIMEText(body))
					msg.attach(part)
					msg.attach(part2)
					msg.attach(part3)
					

					context = ssl.create_default_context()
					server = smtplib.SMTP('smtp.googlemail.com',587)
					server.starttls(context = context)
					server.login(user.login,user.password)
					server.sendmail(user.login,user.tosomeone,msg.as_string())
					bot.send_message(message.chat.id,'Сообщение успешно отправлено.',reply_markup = markup)	
					server.quit()

				except smtplib.SMTPAuthenticationError as e:
					bot.send_message(message.chat.id,"Вы ввели недействительный адрес или пароль!!!",reply_markup = markup)
			except smtplib.SMTPRecipientsRefused as e:
				bot.send_message(message.chat.id,'Вы ввели недействительного получателя')	
		else:
			msg = bot.send_message(message.chat.id,"Прикрепите файл:",reply_markup = markup)
			bot.register_next_step_handler(msg,nefinal_5)

def nefinal_5(message):

	mess = message.text

	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path) # Бот загружает файл
	try:
		global file_type4
		file_type4 = file_info.file_path
		file_type4 = file_type4.split("/")
		file_type4 = file_type4[-1]

	except Exception as e:
		bot.send_message(message.chat.id,'Возникла ошибка с файлом',reply_markup = markup) 
			

	chat_id = message.chat.id
	user2 = user_photo[chat_id]
	user2.photo4 = downloaded_file

	msg = bot.send_message(message.chat.id,'Добавить что-то ещё?',reply_markup = markup_mess1)
	bot.register_next_step_handler(msg,nefinal6)

def nefinal6(message):

	mess = message.text
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user2 = user_photo[chat_id]
	
	if mess.startswith('Отменить отправку.'):
		bot.send_message(message.chat.id,'Отправка отменена.',reply_markup = markup)
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
		
	else:
		
		if message.text != "Добавить." :
			try:
				try:
					msg = MIMEMultipart()
					msg['Subject'] = user.tema	
					msg["To"] = user.tosomeone
					msg['From'] = "Сool->"

					body = user.message2

					part = MIMEApplication(user2.photo1)
					part2 = MIMEApplication(user2.photo2)
					part3 = MIMEApplication(user2.photo3)
					part4 = MIMEApplication(user2.photo4)

					part.add_header('Content-Disposition', 'attachment', filename=file_type1)
					part2.add_header('Content-Disposition', 'attachment', filename=file_type2)
					part3.add_header('Content-Disposition', 'attachment', filename=file_type3)
					part4.add_header('Content-Disposition', 'attachment', filename=file_type4)	

					msg.attach(MIMEText(body))
					msg.attach(part)
					msg.attach(part2)
					msg.attach(part3)
					msg.attach(part4)	

					context = ssl.create_default_context()
					server = smtplib.SMTP('smtp.googlemail.com',587)
					server.starttls(context = context)
					server.login(user.login,user.password)
					server.sendmail(user.login,user.tosomeone,msg.as_string())
					bot.send_message(message.chat.id,'Сообщение успешно отправлено.',reply_markup = markup)	
					server.quit()

				except smtplib.SMTPAuthenticationError as e:
					bot.send_message(message.chat.id,"Вы ввели недействительный адрес или пароль!!!",reply_markup = markup)
			except smtplib.SMTPRecipientsRefused as e:
				bot.send_message(message.chat.id,'Вы ввели недействительного получателя')	
		else:
			msg = bot.send_message(message.chat.id,"Прикрепите последний файл:",reply_markup = markup) # Лимит фото-5
			bot.register_next_step_handler(msg,final2)

def final2(message):

	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path) # Бот загружает файл
	try:
		global file_type5
		file_type5 = file_info.file_path
		file_type5 = file_type5.split("/")
		file_type5 = file_type5[-1]

	except Exception as e:
		bot.send_message(message.chat.id,'Возникла ошибка с файлом',reply_markup = markup) 
			
	mess = message.text
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user2 = user_photo[chat_id]
	user2.photo5 = downloaded_file

	if message.text == 'Отменить отправку.':
		bot.send_message(message.chat.id,'Отправка отменена.')
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)

	else:
		try:
			try:
				msg = MIMEMultipart()
				msg['Subject'] = user.tema	
				msg["To"] = user.tosomeone
				msg['From'] = "Сool->"

				body = user.message2

				part = MIMEApplication(user2.photo1)
				part2 = MIMEApplication(user2.photo2)
				part3 = MIMEApplication(user2.photo3)
				part4 = MIMEApplication(user2.photo4)
				part5 = MIMEApplication(user2.photo5)

				part.add_header('Content-Disposition', 'attachment', filename=file_type1)
				part2.add_header('Content-Disposition', 'attachment', filename=file_type2)
				part3.add_header('Content-Disposition', 'attachment', filename=file_type3)
				part4.add_header('Content-Disposition', 'attachment', filename=file_type4)
				part5.add_header('Content-Disposition', 'attachment', filename=file_type5)

				msg.attach(MIMEText(body))
				msg.attach(part)
				msg.attach(part2)
				msg.attach(part3)
				msg.attach(part4)
				msg.attach(part5)	

				context = ssl.create_default_context()
				server = smtplib.SMTP('smtp.googlemail.com',587)
				server.starttls(context = context)
				server.login(user.login,user.password)
				server.sendmail(user.login,user.tosomeone,msg.as_string())
				bot.send_message(message.chat.id,'Сообщение успешно отправлено.',reply_markup = markup)	
				server.quit()

			except smtplib.SMTPAuthenticationError as e:
				bot.send_message(message.chat.id,"Вы ввели недействительный адрес или пароль!!!",reply_markup = markup)
		except smtplib.SMTPRecipientsRefused as e:
				bot.send_message(message.chat.id,'Вы ввели недействительного получателя')

# Бот отсылает свои команды при написании текста в чат
@bot.message_handler(content_types=["text"])
def first_message(message):	
	bot.send_message(message.chat.id,"МОИ КОМАНДЫ:\n/send - отправка сообщений и файлов.\n/rand - прекол.\n/GDZ - можно нажать на кнопку и перейти на сайт с ГДЗ.\n/course - команда,которая показует курс доллара.\n/weather - узнает погоду в вашем городе.") # IF USER WRITING SOMETHING IN CHAT BOT SEND THE LIST OF COMMANDS

# Если пользователь скидывает файлы в чат
@bot.message_handler(content_types=["photo",'video','audio'])
def wer(message):
	bot.send_message(message.chat.id,'Если хотите отправить какой-то файл воспользуйтесь командой /send')

if __name__ == '__main__':
	bot.polling(none_stop = True)