from tkinter import ttk
import customtkinter
import datetime

from models.gold_transaction_model import GoldTransaction
from models.currency_transaction_model import CurrencyTransaction
from widgets.tab_group_by_sort_by import TabGroupBySortBy


class TabFilter(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff", bg_color="#f2f2f2",
                       border_width=1, border_color="#989DA1")

        self.tab_last_month = self.add("LAST MONTH")
        self.tab_this_month = self.add("THIS MONTH")
        self.tab_future = self.add("FUTURE")
        self.tab_view_all = self.add("VIEW ALL")

        self.set("THIS MONTH")
        self.configure(corner_radius=5)

        self.create_tab_filter_widgets()

    def create_tab_filter_widgets(self):
        last_month_transactions = self.get_transactions_last_month()
        this_month_transactions = self.get_transactions_this_month()
        future_transactions = self.get_transactions_future()
        all_transactions = self.get_transactions_all()

        self.create_tab_with_total_frames(
            self.tab_last_month, last_month_transactions)
        self.create_tab_with_total_frames(
            self.tab_this_month, this_month_transactions)
        self.create_tab_with_total_frames(
            self.tab_future, future_transactions)
        self.create_tab_with_total_frames(
            self.tab_view_all, all_transactions)

        self.tab_group_by_sort_by_last_month = TabGroupBySortBy(
            master=self.tab_last_month, transactions=last_month_transactions)
        self.tab_group_by_sort_by_last_month.pack(
            padx=10, pady=(0, 10), fill="x")
        self.tab_group_by_sort_by_this_month = TabGroupBySortBy(
            master=self.tab_this_month, transactions=this_month_transactions)
        self.tab_group_by_sort_by_this_month.pack(
            padx=10, pady=(0, 10), fill="x")
        self.tab_group_by_sort_by_future = TabGroupBySortBy(
            master=self.tab_future, transactions=future_transactions)
        self.tab_group_by_sort_by_future.pack(padx=10, pady=(0, 10), fill="x")
        self.tab_group_by_sort_by_view_all = TabGroupBySortBy(
            master=self.tab_view_all, transactions=all_transactions)
        self.tab_group_by_sort_by_view_all.pack(
            padx=10, pady=(0, 10), fill="x")

    def create_tab_with_total_frames(self, tab, transactions):
        total_frame = customtkinter.CTkFrame(
            master=tab, fg_color="transparent")
        total_frame.pack(side="top", fill="x")

        self.create_total_transaction_frame(total_frame, transactions)
        self.create_total_amount_frame(total_frame, transactions)

    def create_total_amount_frame(self, tab, transactions):
        total_total_amount_frame = customtkinter.CTkFrame(
            master=tab,
            fg_color="#eaeaea",
            corner_radius=5,
            border_width=1,
            border_color="#989DA1"
        )
        total_total_amount_frame.grid(row=0, column=0, padx=10, pady=10)

        total_total_amount_title = customtkinter.CTkLabel(
            master=total_total_amount_frame,
            text="Total Amount (VND)",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w"
        )
        total_total_amount_title.pack(padx=20, pady=(10, 5), anchor="w")

        gold_total_amount = sum(
            transaction._total_amount for transaction
            in transactions if isinstance(transaction, GoldTransaction)
        )
        formatted_gold_total_amount = self.format_price_number(
            gold_total_amount)
        currency_total_amount = sum(
            transaction._total_amount for transaction
            in transactions if isinstance(transaction, CurrencyTransaction)
        )
        formatted_currency_total_amount = self.format_price_number(
            currency_total_amount)

        gold_label = customtkinter.CTkLabel(
            master=total_total_amount_frame,
            text=f"Gold: {formatted_gold_total_amount:>61}",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        gold_label.pack(padx=40, pady=2, anchor="w")

        currency_label = customtkinter.CTkLabel(
            master=total_total_amount_frame,
            text=f"Currency: {formatted_currency_total_amount:>54}",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        currency_label.pack(padx=40, pady=2, anchor="w")

        separator = ttk.Separator(
            total_total_amount_frame, orient="horizontal")
        separator.pack(fill="x", padx=10, pady=5)

        grand_total = gold_total_amount + currency_total_amount
        formatted_grand_total = self.format_price_number(
            grand_total)
        grand_total_label = customtkinter.CTkLabel(
            master=total_total_amount_frame,
            text=f"Grand Total: {formatted_grand_total:>50}",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        grand_total_label.pack(padx=40, pady=(5, 10), anchor="w")

    def create_total_transaction_frame(self, tab, transactions):
        total_transaction_frame = customtkinter.CTkFrame(
            master=tab,
            fg_color="#eaeaea",
            corner_radius=5,
            border_width=1,
            border_color="#989DA1"
        )
        total_transaction_frame.grid(row=0, column=1, padx=10, pady=10)

        total_transaction_title = customtkinter.CTkLabel(
            master=total_transaction_frame,
            text="Total Transaction",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w"
        )
        total_transaction_title.pack(padx=20, pady=(10, 5), anchor="w")

        gold_transaction = sum(
            1 for transaction in transactions if isinstance(transaction,
                                                            GoldTransaction)
        )

        currency_transaction = sum(
            1 for transaction in transactions
            if isinstance(transaction,
                          CurrencyTransaction)
        )

        gold_label = customtkinter.CTkLabel(
            master=total_transaction_frame,
            text=f"Gold: {gold_transaction:>61}",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        gold_label.pack(padx=40, pady=2, anchor="w")

        currency_label = customtkinter.CTkLabel(
            master=total_transaction_frame,
            text=f"Currency: {currency_transaction:>54}",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        currency_label.pack(padx=40, pady=2, anchor="w")

        separator = ttk.Separator(
            total_transaction_frame, orient="horizontal")
        separator.pack(fill="x", padx=10, pady=5)

        grand_total = gold_transaction + currency_transaction
        grand_total_label = customtkinter.CTkLabel(
            master=total_transaction_frame,
            text=f"Grand Total: {grand_total:>50}",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        grand_total_label.pack(padx=40, pady=(5, 10), anchor="w")

    def get_transactions_last_month(self):
        today = datetime.datetime.now()
        if today.month == 1:
            last_month = 12
            last_month_year = today.year - 1
        else:
            last_month = today.month - 1
            last_month_year = today.year
        return self.get_transactions_by_month_year(last_month, last_month_year)

    def get_transactions_this_month(self):
        today = datetime.datetime.now()
        return self.get_transactions_by_month_year(today.month, today.year)

    def get_transactions_future(self):
        today = datetime.datetime.now()
        future_transactions = []
        for transaction in self.master.transaction_list.get_transactions():
            if (
                transaction._year > today.year
                or (transaction._year == today.year and
                    transaction._month > today.month)
                or (
                    transaction._year == today.year
                    and transaction._month == today.month
                    and transaction._day > today.day
                )
            ):
                future_transactions.append(transaction)
        return future_transactions

    def get_transactions_all(self):
        return self.master.transaction_list.get_transactions()

    def get_transactions_by_month_year(self, month, year):
        transactions_month_year = []
        for transaction in self.master.transaction_list.get_transactions():
            if transaction._month == month and transaction._year == year:
                transactions_month_year.append(transaction)
        return transactions_month_year

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount
