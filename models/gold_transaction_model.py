from models.transaction_model import Transaction


class GoldTransaction(Transaction):
    def __init__(self, id, day, month, year, unit_price, quantity, gold_type,
                 isdeleted=False):
        super().__init__(id, day, month, year, unit_price, quantity,
                         isdeleted=isdeleted)
        self._gold_type = gold_type

    def calculate_total_amount(self):
        return self._unit_price * self._quantity
