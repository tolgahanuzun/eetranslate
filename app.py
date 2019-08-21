import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator


translator = Translator()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=f'You can see the active commands with /help.')

def to_tr(bot, update):
    content = update.message.text[3:] # `/tr `
    translate = translator.translate(content, dest='tr') 
    bot.send_message(chat_id=update.message.chat_id, text=f'{content} = {translate.text}')


def to_eng(bot, update):
    content = update.message.text[3:] # `/eng `
    translate = translator.translate(content, dest='en')
    bot.send_message(chat_id=update.message.chat_id, text=f'{content} = {translate.text}')


def can_help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='''
/en Merhaba, ben herhangi bir dili ingilizceye çeviririm.
/tr Hello, I can translate any language into English.''')


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
