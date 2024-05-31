from models.abstract_transaction_model import AbstractTransaction


class Transaction(AbstractTransaction):
    def __init__(self, id, day, month, year, *args, isdeleted=False):
        super().__init__(id, day, month, year, *args)
        self._isdeleted = isdeleted

    def calculate_total_amount(self):
        return self._unit_price * self._quantity
