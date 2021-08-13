from typing import Dict
from datetime import datetime, tzinfo
import json
from urllib.request import urlopen


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


def load_json(card: int) -> Dict:
    response = urlopen(f'https://meal.gift-cards.ru/api/1/cards/{card}')
    data = json.load(response)
    if data['status'] != 'OK':
        print(data)
        raise Exception()
    return data['data']


def balance_for_today(data: Dict) -> int:
    available = data['balance']['availableAmount']
    balance = 600
    history = data['history']
    if len(history) == 0:
        return balance
    tzinfo = datetime.strptime(history[0]['time'], DATETIME_FORMAT).tzinfo
    today = datetime.now(tzinfo).date()
    for item in data['history']:
        if today == datetime.strptime(item['time'], DATETIME_FORMAT).date():
            if item['amount'] < 0:
                balance += item['amount']
        else:
            break
    return min(available, balance)
