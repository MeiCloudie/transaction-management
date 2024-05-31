import customtkinter
from sys import platform
import datetime

from models.gold_transaction_model import GoldTransaction
from models.currency_transaction_model import CurrencyTransaction


class StatisticsDetailsMonthWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, transactions, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Statistics Details")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(1400, 900)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent
        self.transactions = transactions

        self.create_widget()

        if platform.startswith("win"):
            self.after(200,
                       lambda: self.iconbitmap("./resources/images/logo.ico"))

    def create_widget(self):
        frame_scroll = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent",
            height=1000)
        frame_scroll.pack(padx=5, pady=0, fill="both")

        month_statistics_chart = \
            self.parent.create_statistics_chart_frame(frame_scroll,
                                                      self.transactions,
                                                      self.parent.tab_month,
                                                      btn_details_status=False)
        month_statistics_chart.grid(row=0, column=0, columnspan=2,
                                    padx=10, pady=10, sticky="ew")

        frame_scroll.grid_columnconfigure(0, weight=1)
        frame_scroll.grid_columnconfigure(1, weight=2)

        weeks = self.parent.get_weeks_of_month(datetime.datetime.now().year,
                                               datetime.datetime.now().month)
        week_totals = self.calculate_weekly_totals(weeks)

        for i, (week, totals) in enumerate(zip(weeks, week_totals)):
            row = (i // 2) + 1
            column = i % 2
            self.create_week_frame(frame_scroll, i + 1, week, totals,
                                   row, column)

    def create_week_frame(self, parent, week_number, week_dates,
                          totals, row, column):
        start_date, end_date = week_dates
        gold_total, currency_total = totals
        week_label_text = f"Week {week_number} ({start_date.strftime(
            '%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')})"

        frame_week = customtkinter.CTkFrame(
            parent,
            fg_color="#ffffff",
            border_width=2,
            border_color="#989DA1"
        )
        frame_week.grid(row=row, column=column,
                        padx=10, pady=10, sticky="ew")

        week_label = customtkinter.CTkLabel(
            master=frame_week,
            text=week_label_text,
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="w"
        )
        week_label.pack(padx=20, pady=(20, 5), fill="x")

        frame_gold = customtkinter.CTkFrame(
            master=frame_week, fg_color="transparent")
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
            text=f"{self.format_price_number(gold_total)} VND",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        gold_total_amount_value.grid(
            row=0, column=1, sticky="e", padx=0, pady=0)

        frame_currency = customtkinter.CTkFrame(
            master=frame_week, fg_color="transparent")
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
            text=f"{self.format_price_number(currency_total)} VND",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        currency_total_amount_value.grid(
            row=0, column=1, sticky="e", padx=0, pady=0)

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount

    def calculate_weekly_totals(self, weeks):
        week_totals = []
        for start, end in weeks:
            gold_total = sum(transaction._total_amount
                             for transaction in self.transactions
                             if isinstance(transaction, GoldTransaction)
                             and start <= datetime.date(transaction._year,
                                                        transaction._month,
                                                        transaction._day) <=
                             end)
            currency_total = sum(transaction._total_amount
                                 for transaction in self.transactions
                                 if isinstance(transaction,
                                               CurrencyTransaction)
                                 and
                                 start <= datetime.date(transaction._year,
                                                        transaction._month,
                                                        transaction._day) <=
                                 end)
            week_totals.append((gold_total, currency_total))
        return week_totals
