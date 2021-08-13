from typing import Tuple
from domain import load_json, balance_for_today
from tinydb.database import TinyDB
from user_dao import UserDAO
from view import View


DEFAULT_LIMIT = 600


class Controller:
    def __init__(self, db: TinyDB, view: View, user_id: int) -> None:
        self.user_dao = UserDAO(db)
        self.view = view
        self.user_id = user_id
        pass

    def on_start(self) -> None:
        self.user_dao.reset_user(self.user_id)
        return self.view.started(DEFAULT_LIMIT)

    def on_set_card(self, card: int) -> None:
        self.user_dao.update_card_id(self.user_id, card)
        balance = self._calc_balance()
        return self.view.card_added(**balance)

    def on_set_limit(self, limit: int) -> None:
        self.user_dao.update_daily_limit(self.user_id, limit)
        balance = self._calc_balance()
        if balance is None:
            return self.view.limit_applied_no_card()
        else:
            return self.view.limit_applied(balance['today'])

    def _calc_balance(self) -> Tuple[int, int]:
        user = self.user_dao.get_user_info(self.user_id)
        if user.card is None:
            return None
        if user.limit is None:
            user.limit = DEFAULT_LIMIT
        data = load_json(user.card)
        today = balance_for_today(data)
        total = data['balance']['availableAmount']
        return {'today': today, 'total': total}

    def on_info(self) -> None:
        balance = self._calc_balance()
        if balance is None:
            return self.view.no_card()
        return self.view.info(**balance)

    def on_help(self) -> None:
        user = self.user_dao.get_user_info(self.user_id)
        return self.view.help(user.card, user.limit)

    def on_other(self) -> None:
        self.on_info()
