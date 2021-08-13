from typing import Dict
import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from tinydb import TinyDB, Query

from view import View
from controller import Controller

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main(token: str, db: TinyDB) -> None:

    def start(update: Update, context):
        view = View(update.message)
        controller = Controller(db, view, update.effective_user.id)
        controller.on_start()

    def help(update: Update, context):
        view = View(update.message)
        controller = Controller(db, view, update.effective_user.id)
        controller.on_help()

    def card(update: Update, context):
        view = View(update.message)
        controller = Controller(db, view, update.effective_user.id)
        card = int(update.message.text.split(' ')[-1])
        controller.on_set_card(card)

    def limit(update: Update, context):
        view = View(update.message)
        controller = Controller(db, view, update.effective_user.id)
        limit = int(update.message.text.split(' ')[-1])
        controller.on_set_limit(limit)

    def info(update: Update, context):
        view = View(update.message)
        controller = Controller(db, view, update.effective_user.id)
        controller.on_info()

    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("card", card))
    dispatcher.add_handler(CommandHandler("limit", limit))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, info))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    token = os.environ['TOKEN']
    os.makedirs('../data', exist_ok=True)
    db = TinyDB('../data/db.json')

    main(token, db)
