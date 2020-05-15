# -*- coding: utf-8 -*-
import telebot

''' Обработка сообщений.
bot = telebot.TeleBot("893542959:AAET1KMGZdZBnIKWxBMy7n3MnOmEH3Apx-Q")

@bot.message_handler(content_types=["text"])
def handle_text(message):
	if message.text == "Hi":
		bot.send_message(message.from_user.id, "Hello! I am HabrahabrExampleBot. How can i help you?")
	
	elif message.text == "How are you?" or message.text == "How are u?":
		bot.send_message(message.from_user.id, "I'm fine, thanks. And you?")
	
	else:
		bot.send_message(message.from_user.id, "Sorry, i dont understand you.")

bot.polling(none_stop=True, interval=0)

# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	pass

 # Обработчик для документов и аудиофайлов
@bot.message_handler(content_types=['document', 'audio'])
def handle_document_audio(message):
	pass

bot.polling(none_stop=True, interval=0)
'''
import telegram
import time
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ChatAction
from functools import wraps
import random
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

ACTION, ANSWER = range(2)

flag_zakaz = 0 # 1- нажата кнопка заказ оборудования; 
flag_otchet = 0 # 1- нажата кнопка отчет
osb = "null"

def start(bot, update):
	bot.send_chat_action(chat_id=update.message.chat_id, action = telegram.ChatAction.TYPING)
	time.sleep(1)
	custom_keyboard = [['Заказ оборудования'], ['Отчет в свободной форме'], ['Выгрузка логов'], ['Помощь']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
	bot.send_message(chat_id=update.message.chat_id, text="Что будем делать?", reply_markup=reply_markup)
	return ACTION

def action(bot, update):
	global flag_otchet
	global flag_zakaz
	if(update.message.text == 'Заказ оборудования'):
		global flag_zakaz
		flag_zakaz = 1
		
		
		custom_keyboard = [['Обнинское'], ['Дзержинское'], ['Козельское'], ['Кировское']]
		reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
		bot.send_message(chat_id=update.message.chat_id, text="Выбери ОСБ:", reply_markup=reply_markup)
		#bot.send_message(chat_id=update.message.chat_id, text="Флаг отчета: "+str(flag_otchet)+"\n"+"\n"+"Флаг заказа: "+str(flag_zakaz))
		return ANSWER
	  
	elif(update.message.text == 'Отчет в свободной форме'):
		
		flag_otchet = 1
		send_text(bot, update, "Введи отчет:")
		
		return ANSWER
		
	elif(update.message.text == 'Выгрузка логов'):
		send_text(bot, update, "Выгрузка логов временно невозможна.")
		
		
	elif(update.message.text == 'Помощь'):
		send_text(bot, update, "Для заказа оборудования нажмите кнопку Заказ оборудования. Кнопка отчет необходима для кладовщика при отчете о заказе оборудования. Выгрузка логов доступна Сигуткину Д.Е. По прочим вопросам к Бологову В.А..")
	
	else:
		send_text(bot, update, "Выбери действие.")
	

def send_text(bot, update, tex_send):
	
	bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
	time.sleep(1)
	#reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
	bot.send_message(chat_id=update.message.chat_id, text=tex_send, parse_mode=telegram.ParseMode.MARKDOWN)
	#bot.send_message(chat_id=update.message.chat_id, text="Флаг отчета: "+str(flag_otchet)+"\n"+"\n"+"Флаг заказа: "+str(flag_zakaz))



def get_flag_zakaz(): #возвращает флаг заказ
	return flag_zakaz
def get_flag_otchet(): #возвращает флаг отчет
	return flag_otchet
def get_osb():			#возвращает осб
	return osb
	
def sbros_flagov():
	global flag_zakaz
	global flag_otchet
	global osb
	flag_zakaz = 0
	flag_otchet = 0	
	osb = "null"
	#bot.send_message(chat_id=update.message.chat_id, text="Флаги сброшены! ", reply_markup=reply_markup)

def answer_check(bot, update):

	global osb
	flag_otchet = get_flag_otchet()
	flag_zakaz = get_flag_zakaz()
	osb = get_osb()
	
	
	#bot.send_message(chat_id=update.message.chat_id, text="Флаг отчета: "+flag_otchet+"\n"+"\n_"+"Флаг заказа: "+flag_zakaz, reply_markup=reply_markup)
	
	custom_keyboard = [['Заказ оборудования'], ['Отчет в свободной форме'], ['Выгрузка логов'], ['Помощь']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)

	if(update.message.text == "Обнинское"):
	
		bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
		bot.send_message(chat_id=update.message.chat_id, text="Выбрано осб: Обнинское", parse_mode=telegram.ParseMode.MARKDOWN)
		bot.send_message(chat_id=update.message.chat_id, text="Какое оборудование необходимо?", reply_markup=reply_markup)
		osb = "Обнинское"
		#return ACTION
		
	elif(update.message.text == "Дзержинское"):
	
		bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
		bot.send_message(chat_id=update.message.chat_id, text="Выбрано осб: Дзержинское", parse_mode=telegram.ParseMode.MARKDOWN)
		bot.send_message(chat_id=update.message.chat_id, text="Какое оборудование необходимо?", reply_markup=reply_markup)
		osb = "Дзержинское"
		#return ACTION

	elif(update.message.text == "Козельское"):
	
		bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
		bot.send_message(chat_id=update.message.chat_id, text="Выбрано осб: Козельское", parse_mode=telegram.ParseMode.MARKDOWN)
		bot.send_message(chat_id=update.message.chat_id, text="Какое оборудование необходимо?", reply_markup=reply_markup)
		osb = "Козельское"
		#return ACTION
	
	elif(update.message.text == "Кировское"):
	
		bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
		bot.send_message(chat_id=update.message.chat_id, text="Выбрано осб: Кировское", parse_mode=telegram.ParseMode.MARKDOWN)
		bot.send_message(chat_id=update.message.chat_id, text="Какое оборудование необходимо?", reply_markup=reply_markup)
		osb = "Кировское"
		#return ACTION
	
	else:
		
		up_text = update.message.text
		up_chat_id = update.message.chat_id
		#bot.send_message(chat_id=update.message.chat_id, text="Записано сообщение:", parse_mode=telegram.ParseMode.MARKDOWN)
		
		
		#bot.send_message(chat_id=update.message.chat_id, text="От пользователя:  \n"+str(up_chat_id)+"\n"+"Текст"+"\n"+up_text, reply_markup=reply_markup)
		
		# id Оля 351441795
		#  Бологов 474921250
		# Сигуткин 477574186
		# Гусаков 79728426
		name1_chat = update.message.from_user.first_name
		name2_chat = update.message.from_user.last_name
		#bot.send_message(chat_id=474921250, text="Записано сообщение:  \n"+"От пользователя:  \n"+str(name1_chat)+"  "+str(name2_chat))
		#bot.send_message(chat_id=474921250, text=" \n"+str(up_chat_id)+"\n  Текст"+"\n"+up_text)
		#bot.send_message(chat_id=477574186, text="Записано сообщение:  \n"+"От пользователя:  \n"+str(name1_chat)+"  "+str(name2_chat))
		#bot.send_message(chat_id=477574186, text=" \n"+str(up_chat_id)+"\n  Текст"+"\n"+up_text)
		
		#bot.send_message(chat_id=update.message.chat_id, text="Флаг отчета: "+str(flag_otchet)+"\n"+"\n"+"Флаг заказа: "+str(flag_zakaz))
		#return ACTION
		
		if (flag_zakaz == 1):
			#ответ пользователю
			reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
			bot.send_message(chat_id=update.message.chat_id, text="Введён заказ."+"\n"+"ОСБ: "+osb+"\n_"+up_text, reply_markup=reply_markup)
			#отправка кладовщику
			
			#отправка ответственному
			bot.send_message(chat_id=474921250, text="Записано сообщение:  \n"+"От пользователя:  \n"+str(name1_chat)+"  "+str(name2_chat))
			bot.send_message(chat_id=474921250, text="ID чата с пользователем "+str(up_chat_id)+"\nЗаказ оборудования: \n ОСБ: "+osb+"\n"+up_text)
			#Запись логов
			
			
			sbros_flagov()
			return ACTION
		elif(flag_otchet == 1):
			#ответ пользователю
			reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
			bot.send_message(chat_id=update.message.chat_id, text="Введён отчет."+"\n"+"\n_"+up_text, reply_markup=reply_markup)
			#отправка ответственному
			
			#Запись логов
			
			sbros_flagov()
			return ACTION
		else:
			#ответ пользователю
			reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
			bot.send_message(chat_id=update.message.chat_id, text="Что-то не то. надо заново.", reply_markup=reply_markup)
			sbros_flagov()
			return ACTION
		
	
		


def cancel(bot, update):
	return ConversationHandler.END

def send_action(action):
	def decorator(func):
		@wraps(func)
		def command_func(*args, **kwargs):
			bot, update = args
			bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
			return func(bot, update, **kwargs)
		return command_func
	
	return decorator

def error(bot, update, error):
	logger.warning('Update "%s" caused error "%s"', update, error)

def main():
	updater = Updater(token='893542959:AAET1KMGZdZBnIKWxBMy7n3MnOmEH3Apx-Q')

	dispatcher = updater.dispatcher

	conv_handler = ConversationHandler(
		entry_points = [CommandHandler('start', start)],

		states = {
			ACTION: [RegexHandler('^(Заказ оборудования|Отчет в свободной форме|Выгрузка логов|Помощь)$', action)],
			ANSWER: [MessageHandler(Filters.text, answer_check)]
		},

		fallbacks=[CommandHandler('cancel', cancel)]
	)

	dispatcher.add_handler(conv_handler)

	dispatcher.add_error_handler(error)
	
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()