from typing import Dict
import os
import logging

import json
from typing import Text
from urllib.request import urlopen

from telegram import Update, ForceReply, user
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from tinydb import TinyDB, Query

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def load_json(card: int) -> Dict:
    response = urlopen(f'https://meal.gift-cards.ru/api/1/cards/{card}')
    data = json.load(response)
    if data['status'] != 'OK':
        print(data)
        raise Exception()
    return data['data']

def main(token: str, db: TinyDB) -> None:
    def set_card(update: Update, context: CallbackContext) -> None:
        try:
            card = int(update.message.text.split(' ')[-1])
            load_json(card)
        except:
            update.message.reply_text('send valid the card number')
            return
        user_id = update.effective_user.id
        User = Query()
        if len(db.search(User.user_id == user_id)) == 0:
            db.insert({'user_id': user_id, 'card': card})
        else:
            db.update({'card': card}, User.user_id == user_id)
        update.message.reply_text('saved')

    def echo(update: Update, context: CallbackContext) -> None:
        user_id = update.effective_user.id
        User = Query()
        user = db.search(User.user_id == user_id)
        if len(user) == 0:
            update.message.reply_text('/set *card_number* first')
            return
        elif len(user) > 1:
            raise Exception('inconsistent data base')
        user = user[0]
        data = load_json(user['card'])
        money = data['balance']['availableAmount']
        update.message.reply_text(f'available amount {money}')

    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("set", set_card))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    token = os.environ['TOKEN']
    db = TinyDB('data/db.json')

    main(token, db)
