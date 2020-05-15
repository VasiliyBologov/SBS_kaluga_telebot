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
import logging
from functools import wraps
import random
import dictionaries

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

ACTION, ANSWER = range(2)

words = dictionaries.words
type = dictionaries.type
description = dictionaries.description

flag_zakaz = 0 # 1- нажата кнопка заказ оборудования; 11 - выбрано осб 
flag_otchet = 0 # 1- нажата кнопка отчет

def start(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    custom_keyboard = [['Заказ оборудования'], ['Отчет в свободной форме'], ['Выгрузка логов'], ['Помощь']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
    bot.send_message(chat_id=update.message.chat_id, text="Чаво надо?", reply_markup=reply_markup)
    return ACTION

def action(bot, update):  # обработка событий по нажатию кнопки
    if(update.message.text == 'Заказ оборудования'):
		# флаг заказ оборудования
        
        global flag_zakaz
		flag_zakaz = 1
		custom_keyboard = [['Обнинское'], ['Дзержинское'], ['Козельское'], ['Кировское']]
		
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
		
        bot.send_message(chat_id=update.message.chat_id, text="Выбери ОСБ:", reply_markup=reply_markup)
		
        return ANSWER
		
    elif(update.message.text == 'Отчет в свободной форме'):
        learn(bot, update)
		
	elif(update.message.text == 'Выгрузка логов'):
		reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
        bot.send_message(chat_id=update.message.chat_id, text="Выгрузка логов доступна Админу!", reply_markup=reply_markup)
		#сделать выгрузку логов		
		
	elif(update.message.text == 'Помощь'):
		reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
        bot.send_message(chat_id=update.message.chat_id, text="Для заказа оборудования нажмите кнопку Заказ оборудования. Кнопка отчет необходима для кладовщика при отчете о заказе оборудования. Выгрузка логов доступна Сигуткину Д.Е. По прочим вопросам к Бологову В.А.", reply_markup=reply_markup)
		'''
def generate_correct_answer(): #генерация рандомного слова из словааря
    num = random.randint(1, len(words) - 1)
    return num

def get_correct_word(): #подтверждение корректности
    return correct_word
'''
def answer_check(bot, update): #обработка событий по ответу текстом по флагу
    
    custom_keyboard = [['Заказ оборудования'], ['Отчет в свободной форме'], ['Выгрузка логов'], ['Помощь']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
	global flag_zakaz
	global flag_otchet
    """
	if(update.message.text == words[correct_word]):
        bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id, text="*Correct!*", parse_mode=telegram.ParseMode.MARKDOWN)
        bot.send_message(chat_id=update.message.chat_id, text="What do you want to do?", reply_markup=reply_markup)
        return ACTION
    else:
        bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id, text="*Incorrect!*" + " Correct answer is: " + words[correct_word], parse_mode=telegram.ParseMode.MARKDOWN)
        bot.send_message(chat_id=update.message.chat_id, text="What do you want to do?", reply_markup=reply_markup)
        return ACTION
	"""
	if(flag_zakaz == 1):# выбрана кнопка заказ оборудования-> выбор осб
		osb = update.message.text
		bot.send_message(chat_id=update.message.chat_id, text="Выбрано ОСБ: "+osb+"  Напиши список необходимового оборудования и материалов.", reply_markup=reply_markup)
		global flag_zakaz
		flag_zakaz = 11
		#return ANSWER
		#запись осб на заказ оборудования в логи
	if(flag_zakaz == 11): #выбрано осб -> пиши список
		list_obor = update.message.text
		bot.send_message(chat_id=update.message.chat_id, text="Заказано оборудование: "+list_obor+ "Список отправлен кладовщику.ЗЫ: не отправлен еще тест.", reply_markup=reply_markup)
		
		global flag_zakaz
		flag_zakaz = 0
		return ACTION
		# запись списка оборудования в логи и отправка кладовщику и сигуткину
	if(flag_otchet == 1):
		othcet_klad = update.message.text
		bot.send_message(chat_id=update.message.chat_id, text="Отчет: "+list_obor+ "записан .ЗЫ: не записан еще тест.", reply_markup=reply_markup)
		# записать отчет в логи
		global flag_otchet
		flag_otchet = 0
		return ACTION
	
	
def learn(bot, update): #отработка нажатия кнопки Отчет в свободной форме
    # флаг отчет
        
    global flag_otchet
	flag_otchet = 1
    bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
    time.sleep(1)
    bot.send_message(chat_id=update.message.chat_id, text="Напиши отчет в свободной форме")
	return ANSWER
	#записать отчет в логи!!!

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