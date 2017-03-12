import logging
import os
import json
import argparse
import random

import telegram.ext

import database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def display_welcome_message(bot, update):
    message = 'Чтобы получить новость про Питон, напишите /python_news.'
    update.message.reply_text(message)


def get_random_post(database):
    random_id = random.randint(1, database.size())
    return database.load_post_by_database_id(random_id)


def display_random_python_post(bot, update):
    post = get_random_post(bot.database)
    post_message = '%s\n\n%s' % (post['summary'], post['link'])
    update.message.reply_text(post_message)


def log_error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def get_telegram_bot_token():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if token == None:
        raise ValueError('Please put bot\'s token to TELEGRAM_BOT_TOKEN ' 
                         'environmental variable')
    return token


def get_command_handlers():
    command_handlers = {
                        'start': display_welcome_message,
                        'python_news': display_random_python_post,
                        }
    return command_handlers


def get_dispatcher_with_command_handlers(bot_dispatcher, command_handlers):
    for command, handler in command_handlers.items():
        bot_dispatcher.add_handler(telegram.ext.CommandHandler(command, handler))
    return bot_dispatcher


def start_bot(bot):
    ignore_past_updates = True
    bot.start_polling(clean=ignore_past_updates)
    bot.idle()  # run until Ctrl-C is pressed


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='display log messages')
    parser.add_argument('file_with_posts', help='database containing posts to display')
    return parser


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    token = get_telegram_bot_token()
    updater = telegram.ext.Updater(token)
    updater.bot.database = database.PostDatabase(args.file_with_posts)
    if args.verbose:
        updater.dispatcher.add_error_handler(log_error)
    command_handlers = get_command_handlers()
    updater.dispatcher = get_dispatcher_with_command_handlers(updater.dispatcher,
                                                              command_handlers)
    print('The bot is started, press Ctrl-C to stop.')
    start_bot(updater)
