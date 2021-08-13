from typing import List
from dataclasses import dataclass
from enum import Enum
from tinydb import TinyDB, Query, table


@dataclass
class User:
    user_id: int
    card: int = None
    limit: int = None


class _USERS(Enum):
    """
        user_id: int
        card_id: int?
        daily_limit: int?
    """
    USER_ID = 'user_id'
    CARD_ID = 'card_id'
    DAILY_LIMIT = 'daily_limit'


class UserDAO:
    def __init__(self, db: TinyDB) -> None:
        self.table = db.table('users')

    def reset_user(self, user_id: int) -> None:
        self.table.remove(UserDAO._query_by(user_id))
        self.table.insert({_USERS.USER_ID.value: user_id})

    def update_card_id(self, user_id: int, card_id: int) -> None:
        self._safe_update(user_id, {_USERS.CARD_ID.value: card_id},
                          UserDAO._query_by(user_id))

    def update_daily_limit(self, user_id: int, limit: int) -> None:
        self._safe_update(user_id, {_USERS.DAILY_LIMIT.value: limit},
                          UserDAO._query_by(user_id))

    def get_user_info(self, user_id: int) -> User:
        res = self._safe_search(user_id, UserDAO._query_by(user_id))
        if len(res) == 0:
            return None
        elif len(res) > 1:
            raise Exception(res)
        one = res[0]
        return User(
            user_id,
            card=one.get(_USERS.CARD_ID.value),
            limit=one.get(_USERS.DAILY_LIMIT.value)
        )

    def _safe_search(self, user_id: int, *args, **kwargs) -> List:
        res = self.table.search(*args, **kwargs)
        if len(res) == 0:
            self.reset_user(user_id)
        res = self.table.search(*args, **kwargs)
        assert len(res) > 0
        return res

    def _safe_update(self, user_id: int, *args, **kwargs):
        if len(self.table.update(*args, **kwargs)) == 0:
            self.reset_user(user_id)
        assert len(self.table.update(*args, **kwargs)) == 1

    @staticmethod
    def _query_by(user_id: int) -> Query:
        User = Query()
        return User.user_id == user_id
