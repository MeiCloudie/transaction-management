import customtkinter
from sys import platform
import datetime

from models.gold_transaction_model import GoldTransaction
from models.currency_transaction_model import CurrencyTransaction


class StatisticsDetailsWeekWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, transactions, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Statistics Details")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(1400, 900)
        self.maxsize(1400, 900)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent
        self.transactions = transactions

        self.create_widget()

        if platform.startswith("win"):
            self.after(200,
                       lambda: self.iconbitmap("./resources/images/logo.ico"))

    def create_widget(self):
        self.frame_scroll = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent",
            height=860)
        self.frame_scroll.pack(padx=5, pady=0, fill="both")

        month_statistics_chart = \
            self.parent.create_statistics_chart_frame(self.frame_scroll,
                                                      self.transactions,
                                                      self.parent.tab_week,
                                                      btn_details_status=False)
        month_statistics_chart.grid(row=0, column=0, columnspan=2,
                                    padx=10, pady=10, sticky="ew")

        self.frame_scroll.grid_columnconfigure(0, weight=1)
        self.frame_scroll.grid_columnconfigure(1, weight=2)

        self.create_date_frame()

    def create_date_frame(self):
        date_statistics_chart = self.parent.create_statistics_chart_frame(
            self.frame_scroll, self.transactions, self.parent.tab_week,
            btn_details_status=False)
        date_statistics_chart.grid(row=0, column=0, columnspan=2,
                                   padx=10, pady=10, sticky="ew")

        current_date = datetime.datetime.now().date()

        start_of_week = current_date - \
            datetime.timedelta(days=current_date.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        transactions_this_week = [
            txn for txn in self.transactions
            if start_of_week <=
            datetime.date(txn._year, txn._month, txn._day) <= end_of_week
        ]

        gold_daily_totals, currency_daily_totals = self.calculate_daily_totals(
            transactions_this_week)

        for i, ((gold_date, gold_total), (currency_date, currency_total)) \
                in enumerate(zip(gold_daily_totals.items(),
                                 currency_daily_totals.items())):
            row = (i // 2) + 1
            column = i % 2
            self.create_day_frame(
                self.frame_scroll, gold_date, gold_total,
                currency_total, row, column)

    def create_day_frame(self, parent, gold_date, gold_total,
                         currency_total, row, column):
        formatted_date = gold_date.strftime("%A %d/%m/%Y")

        frame_day = customtkinter.CTkFrame(
            parent,
            fg_color="#ffffff",
            border_width=2,
            border_color="#989DA1"
        )
        frame_day.grid(row=row, column=column,
                       padx=10, pady=10, sticky="ew")

        day_label = customtkinter.CTkLabel(
            master=frame_day,
            text=formatted_date,
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="w"
        )
        day_label.pack(padx=20, pady=(20, 5), fill="x")

        formatted_gold_total = self.format_price_number(gold_total)
        formatted_currency_total = self.format_price_number(currency_total)

        frame_gold = customtkinter.CTkFrame(
            master=frame_day, fg_color="transparent")
        frame_gold.pack(padx=40, pady=5, fill="x")

        frame_gold.columnconfigure(0, weight=0)
        frame_gold.columnconfigure(1, weight=1)

        gold_label = customtkinter.CTkLabel(
            master=frame_gold,
            text="GOLD TRANSACTION:",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w"
        )
        gold_label.grid(row=0, column=0, sticky="w", padx=0, pady=0)

        gold_total_amount_value = customtkinter.CTkLabel(
            master=frame_gold,
            text=f"{formatted_gold_total} VND",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        gold_total_amount_value.grid(
            row=0, column=1, sticky="e", padx=0, pady=0)

        frame_currency = customtkinter.CTkFrame(
            master=frame_day, fg_color="transparent")
        frame_currency.pack(padx=40, pady=(5, 20), fill="x")

        frame_currency.columnconfigure(0, weight=0)
        frame_currency.columnconfigure(1, weight=1)

        currency_label = customtkinter.CTkLabel(
            master=frame_currency,
            text="CURRENCY TRANSACTION:",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w"
        )
        currency_label.grid(row=0, column=0, sticky="w", padx=0, pady=0)

        currency_total_amount_value = customtkinter.CTkLabel(
            master=frame_currency,
            text=f"{formatted_currency_total} VND",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        currency_total_amount_value.grid(
            row=0, column=1, sticky="e", padx=0, pady=0)

    def calculate_daily_totals(self, transactions):
        gold_daily_totals = {}
        currency_daily_totals = {}

        current_date = datetime.datetime.now().date()

        start_of_week = current_date - \
            datetime.timedelta(days=current_date.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        for i in range(7):
            date = start_of_week + datetime.timedelta(days=i)
            gold_daily_totals[date] = 0
            currency_daily_totals[date] = 0

        for transaction in transactions:
            transaction_date = datetime.date(
                transaction._year, transaction._month, transaction._day)
            if start_of_week <= transaction_date <= end_of_week:
                if isinstance(transaction, GoldTransaction):
                    gold_daily_totals[transaction_date] += \
                        transaction._total_amount
                elif isinstance(transaction, CurrencyTransaction):
                    currency_daily_totals[transaction_date] += \
                        transaction._total_amount

        return gold_daily_totals, currency_daily_totals

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount
