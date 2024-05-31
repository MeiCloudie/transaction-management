from abc import ABC, abstractmethod


class AbstractTransaction(ABC):
    def __init__(self, id, day, month, year, *args):
        self._id = id
        self._day = day
        self._month = month
        self._year = year
        if len(args) == 1:
            self._quantity = args[0]
            self._unit_price = None
        elif len(args) == 2:
            self._unit_price = args[0]
            self._quantity = args[1]
        else:
            raise ValueError("Invalid number of arguments")

        self._total_amount = self.calculate_total_amount()

    @abstractmethod
    def calculate_total_amount(self):
        pass
