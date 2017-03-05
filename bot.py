import logging
import os
import json
from argparse import ArgumentParser, FileType

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def display_welcome_message(bot, update):
    message = 'Welcome 🙌\n'\
              'Type in /help for a list of commands.'
    update.message.reply_text(message)


def display_help(bot, update):
    message = 'List of commands:\n'\
              '/python_news -- get relatively new post mentioning Python'
    update.message.reply_text(message)


def display_random_python_post(bot, update):
    raise NotImplemented


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
                        'help': display_help,
                        'python_news': display_random_python_post,
                        }
    return command_handlers


def get_dispatcher_with_command_handlers(bot_dispatcher, command_handlers):
    for command, handler in command_handlers.items():
        bot_dispatcher.add_handler(CommandHandler(command, handler))
    return bot_dispatcher


def start_bot(bot):
    ignore_past_updates = True
    bot.start_polling(clean=ignore_past_updates)
    bot.idle()  # run until Ctrl-C is pressed


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='display log messages')
    parser.add_argument('file_with_posts', help='database containing posts to display')
    return parser


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    token = get_telegram_bot_token()
    bot = Updater(token)
    if args.verbose:
        bot.dispatcher.add_error_handler(log_error)
    command_handlers = get_command_handlers()
    bot.dispatcher = get_dispatcher_with_command_handlers(bot.dispatcher, command_handlers)
    print('The bot is started, press Ctrl-C to stop.')
    start_bot(bot)
