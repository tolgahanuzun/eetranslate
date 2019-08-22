import logging
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator


translator = Translator()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def push_messages(func):
    def inner(bot, update):
        func(bot, update)
        db_api = "db-api"
        db_header = {
            'Content-Type': "application/json",
            'apikey': "key"
        }
        payload = {"user_id": f'{update.message.chat_id}', "content": f"{update.message.text}", "source": func.__name__ }
        requests.post(db_api, json=payload, headers=db_header)
    return inner

@push_messages
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=f'You can see the active commands with /help.')

@push_messages
def to_tr(bot, update):
    content = update.message.text[3:] # `/tr `
    translate = translator.translate(content, dest='tr') 
    bot.send_message(chat_id=update.message.chat_id, text=f'{content} = {translate.text}')

@push_messages
def to_eng(bot, update):
    content = update.message.text[3:] # `/eng `
    translate = translator.translate(content, dest='en')
    bot.send_message(chat_id=update.message.chat_id, text=f'{content} = {translate.text}')

@push_messages
def can_help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='''
/en Merhaba, ben herhangi bir dili ingilizceye çeviririm.
/tr Hello, I can translate any language into English.''')

@push_messages
def echo(bot, update):
    """Echo the user message."""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    updater = Updater("KEY")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tr", to_tr))
    dp.add_handler(CommandHandler("en", to_eng))
    dp.add_handler(CommandHandler("help", can_help))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
