class ExchangeRate:
    def __init__(self, id, currency_type, rate, effective_day, effective_month,
                 effective_year):
        self._id = id
        self._currency_type = currency_type
        self._rate = rate
        self._effective_day = effective_day
        self._effective_month = effective_month
        self._effective_year = effective_year
