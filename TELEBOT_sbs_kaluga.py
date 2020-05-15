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

correct_word = 0

def start(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(1)
    custom_keyboard = [['Заказ оборудования'], ['Отчет в свободной форме']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
    bot.send_message(chat_id=update.message.chat_id, text="What do you want to do?", reply_markup=reply_markup)
    return ACTION

def action(bot, update):
    if(update.message.text == 'Заказ оборудования'):
        learn(bot, update)
    elif(update.message.text == 'Отчет в свободной форме'):
        num = generate_correct_answer()
        global correct_word 
        correct_word = num
        correct_num = random.randint(1, 4)
        first_incorrect = words[random.randint(1, len(words) - 1)]
        second_incorrect = words[random.randint(1, len(words) - 1)]
        third_incorrect = words[random.randint(1, len(words) - 1)]
        if(correct_num == 1):
            custom_keyboard=[[words[correct_word]], [first_incorrect], 
            [second_incorrect], [third_incorrect]]
        elif(correct_num == 2):
            custom_keyboard=[[first_incorrect], [words[correct_word]], 
            [second_incorrect], [third_incorrect]]
        elif(correct_num == 3):
            custom_keyboard=[[first_incorrect], [second_incorrect], 
            [words[correct_word]], [third_incorrect]]
        elif(correct_num == 4):
            custom_keyboard=[[first_incorrect], [second_incorrect], 
            [third_incorrect], [words[correct_word]]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
        bot.send_message(chat_id=update.message.chat_id, text=description[correct_word], reply_markup=reply_markup)
        return ANSWER

def generate_correct_answer(): #генерация рандомного слова из словааря
    num = random.randint(1, len(words) - 1)
    return num

def get_correct_word(): #подтверждение корректности
    return correct_word

def answer_check(bot, update):
    correct_word = get_correct_word()
    custom_keyboard = [['Заказ оборудования'], ['Отчет в свободной форме']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=False)
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

def learn(bot, update):
    num = random.randint(1, len(words) - 1)
    bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
    time.sleep(1)
    bot.send_message(chat_id=update.message.chat_id, text="*"+ words[num]+"* - "+description[num]+"\n"+"\n_"+type[num]+"_", parse_mode=telegram.ParseMode.MARKDOWN)
    bot.send_message(chat_id=update.message.chat_id, text="What is next?")

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
            ACTION: [RegexHandler('^(Заказ оборудования|Отчет в свободной форме)$', action)],
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