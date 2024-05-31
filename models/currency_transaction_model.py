from models.transaction_model import Transaction
from enums.currency_type_enum import CurrencyType


class CurrencyTransaction(Transaction):
    def __init__(self, id, day, month, year, quantity,
                 currency_type, exchange_rate, isdeleted=False):
        self._currency_type = currency_type
        self._exchange_rate = exchange_rate
        super().__init__(id, day, month, year, quantity, isdeleted=isdeleted)

    def calculate_total_amount(self):
        if self._currency_type == CurrencyType.VND:
            return self._quantity
        elif self._currency_type == CurrencyType.USD \
                or self._currency_type == CurrencyType.EUR:
            return self._quantity * self._exchange_rate._rate
        else:
            return 0
