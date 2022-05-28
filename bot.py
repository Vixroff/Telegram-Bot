from emoji import emojize
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint, choice
import settings
from glob import glob

logging.basicConfig(filename='bot.log', level=logging.INFO)

def get_emoji(user_data):
    if 'emoji' not in user_data:
        emoji = choice(settings.USER_EMOJI)
        return emojize(emoji, use_aliases=True)
    return user_data['emoji']

def greet_user(update, context):
    print('Вызван /start')
    context.user_data["emoji"] = get_emoji(context.user_data)
    update.message.reply_text(f'Привет {context.user_data["emoji"]}!')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    context.user_data["emoji"] = get_emoji(context.user_data)
    update.message.reply_text(f'{text} {context.user_data["emoji"]}')

def play_guess_number(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Вы загадали {user_number}, я загадал {bot_number}. Вы выиграли!'
    elif user_number == bot_number:
        message = f'Вы загадали {user_number}, я загадал {bot_number}. Ничья!'
    elif user_number < bot_number:
        message = f'Вы загадали {user_number}, я загадал {bot_number}. Вы проиграли!'
    return message

def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_guess_number(user_number)
        except (TypeError, ValueError):
            message = f'Введите целое число'
    else:
        message = 'Введите число'
    update.message.reply_text(message)

def send_photo_cat(update, context):
    #создаем список файлов с котиками. glob возвращает все файлы по шаблону
    cat_photo_list = glob('images/cat_*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    #id чата с текущим пользователем(чтобы не отправилось всем подписчикам в боте)
    chat_id = update.effective_chat.id  
    context.bot.send_photo(chat_id = chat_id, photo = open(cat_photo_filename, 'rb'))

def main():
    mybot = Updater(settings.API_KEY, use_context=True) 
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_photo_cat))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle() 

if __name__ == '__main__':
    main()    
