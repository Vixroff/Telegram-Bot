# импорт компонента, который будет фиксировать ошибки при работе бота
import logging
# импорт из библиотеки компонента, отвечающего за связь с сервером телеграм и обработчиков.
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# импорт нащих уникальных ключей
import settings
# команда записывающая ошибки в файл c учетом уровня важности
logging.basicConfig(filename='bot.log', level=logging.INFO)

# функция вызываемая при начале использования бота. 
# update - информация, которая пришла от сервера Телеграм(команда старт, информация о пользователе и тд)
# context - это сообщение передаваемое боту, действие.
def greet_user(update, context):
    print('Вызван /start')
    print(update)
    update.message.reply_text('Привет!')

# Функция, которая пересылает написанный текст обратно пользователю
def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def main():
    # идентификация создателя бота
    mybot = Updater(settings.API_KEY, use_context=True) 
    # обработка команды /start 
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    # в скобочках указано на какие типы сообщений реагировать и вызывваемая функция
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    # запрос на сервер о сообщениях, циклическое действие
    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle() 

main()    
