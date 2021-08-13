from telegram import Message


RUB = 'р'
def currency(amount: int) -> str:
    return f'{amount}{RUB}'

class View:
    def __init__(self, message: Message) -> None:
        self.m = message

    def started(self, default_limit: int) -> None:
        return self.m.reply_text(
            "Давай знакомиться!\n" +
            "Мне понадобится номер карты, но не тот, что на передней стороне, а с задней, там где штрихкод - 13 цифр.\n" + 
            "Отправь мне этот номер /card 1234567890123\n" + 
            f"Для того чтобы вычислить сколько осталось денег на сегодня по умолчанию используется лимит в {default_limit} рублей.\n" +
            "Ты можешь изменить лимит командой /limit 800"
        )

    def card_added(self, today: int, total: int) -> None:
        return self.m.reply_text(
            "Карта добавлена!\n" +
            self._info_text(today, total)
        )

    def no_card(self) -> None:
        return self.m.reply_text(
            "Сначала необходимо добавить карту.\n" +
            "Отправь 13 цифр с обратной стороны карты (рядом со штрихкодом), командой\n" +
            "/card 1234567890123"
        )

    def limit_applied_no_card(self, new_limit: int) -> None:
        return self.m.reply_text(
            f"Лимит изменен на {new_limit}\n" + 
            "Осталось добавить карту."
        )

    def limit_applied(self, new_limit: int, today: int) -> None:
        return self.m.reply_text(
            f"С учетом нового лимита в {new_limit} рублей,\n" + 
            f"на сегодня осталось {currency(today)}"
        )

    def help(self, card: int, limit: int) -> None:
        return self.m.reply_text("help не дописал еще")

    def _info_text(self, today: int, total: int) -> str:
        return f"сегодня {currency(today)}\nвсего {currency(total)}"

    def info(self, today: int, total: int) -> None:
        return self.m.reply_text(self._info_text(today, total))
