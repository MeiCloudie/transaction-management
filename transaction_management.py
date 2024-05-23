import json
import tkinter
from tkinter import ttk, messagebox
import customtkinter
from enum import Enum
from abc import ABC, abstractmethod
from PIL import Image
import datetime
from datetime import timedelta
from sys import platform
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
# import math
import pandas as pd
import numpy as np


class CurrencyType(Enum):
    VND = 0
    USD = 1
    EUR = 2


class GoldType(Enum):
    SJC = 0
    PNJ = 1
    DOJI = 2


class MonthLabel(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def __str__(self):
        return self.name.capitalize()


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


class Transaction(AbstractTransaction):
    def __init__(self, id, day, month, year, *args, isdeleted=False):
        super().__init__(id, day, month, year, *args)
        self._isdeleted = isdeleted

    def calculate_total_amount(self):
        return self._unit_price * self._quantity


class GoldTransaction(Transaction):
    def __init__(self, id, day, month, year, unit_price, quantity, gold_type,
                 isdeleted=False):
        super().__init__(id, day, month, year, unit_price, quantity,
                         isdeleted=isdeleted)
        self._gold_type = gold_type

    def calculate_total_amount(self):
        return self._unit_price * self._quantity


class ExchangeRate:
    def __init__(self, id, currency_type, rate, effective_day, effective_month,
                 effective_year):
        self._id = id
        self._currency_type = currency_type
        self._rate = rate
        self._effective_day = effective_day
        self._effective_month = effective_month
        self._effective_year = effective_year


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


class TransactionList:
    def __init__(self):
        self._transactions = []
        self._total_gold_transactions = 0
        self._total_currency_transactions = 0
        self._total_gold_amount = 0.0
        self._total_currency_amount = 0.0

    def add_transaction(self, transaction):
        self._transactions.append(transaction)
        if isinstance(transaction, GoldTransaction):
            self._total_gold_transactions += 1
            self._total_gold_amount += transaction._total_amount
        elif isinstance(transaction, CurrencyTransaction):
            self._total_currency_transactions += 1
            self._total_currency_amount += transaction._total_amount

    def remove_transaction(self, transaction):
        if transaction in self._transactions:
            self._transactions.remove(transaction)

    def get_transactions(self):
        return self._transactions

    def clear(self):
        self._transactions = []


# Initialize data
# transactions
transactions_data = [
    {
        "id": "GLD001", "day": 2, "month": 5, "year": 2024,
        "unit_price": 85200000.0, "quantity": 2.0, "type": "gold",
        "gold_type": 0, "isdeleted": False, "exchange_rate_id": None,
        "currency_type": None, "exchange_rate": None, "effective_day": None,
        "effective_month": None, "effective_year": None
    },
    {
        "id": "GLD002", "day": 2, "month": 5, "year": 2024,
        "unit_price": 75500000.0, "quantity": 3.0, "type": "gold",
        "gold_type": 1, "isdeleted": False, "exchange_rate_id": None,
        "currency_type": None, "exchange_rate": None, "effective_day": None,
        "effective_month": None, "effective_year": None
    },
    {
        "id": "GLD003", "day": 22, "month": 4, "year": 2024,
        "unit_price": 84800000.0, "quantity": 3.0, "type": "gold",
        "gold_type": 2, "isdeleted": False, "exchange_rate_id": None,
        "currency_type": None, "exchange_rate": None, "effective_day": None,
        "effective_month": None, "effective_year": None
    },
    {
        "id": "GLD004", "day": 15, "month": 6, "year": 2024,
        "unit_price": 83200000.0, "quantity": 1.0, "type": "gold",
        "gold_type": 0, "isdeleted": False, "exchange_rate_id": None,
        "currency_type": None, "exchange_rate": None, "effective_day": None,
        "effective_month": None, "effective_year": None
    },
    {
        "id": "GLD005", "day": 19, "month": 2, "year": 2024,
        "unit_price": 74500000.0, "quantity": 1.0, "type": "gold",
        "gold_type": 1, "isdeleted": False, "exchange_rate_id": None,
        "currency_type": None, "exchange_rate": None, "effective_day": None,
        "effective_month": None, "effective_year": None
    },
    {
        "id": "GLD006", "day": 25, "month": 4, "year": 2024,
        "unit_price": 84800000.0, "quantity": 2.0, "type": "gold",
        "gold_type": 2, "isdeleted": False, "exchange_rate_id": None,
        "currency_type": None, "exchange_rate": None, "effective_day": None,
        "effective_month": None, "effective_year": None
    },
    {
        "id": "CUR001", "day": 2, "month": 5, "year": 2024, "quantity": 50.0,
        "type": "currency", "currency_type": 1, "exchange_rate_id": 2,
        "exchange_rate": 25137.0, "effective_day": 1, "effective_month": 1,
        "effective_year": 2024, "isdeleted": False
    },
    {
        "id": "CUR002", "day": 28, "month": 4, "year": 2024, "quantity": 500.0,
        "type": "currency", "currency_type": 2, "exchange_rate_id": 3,
        "exchange_rate": 26777.56, "effective_day": 1, "effective_month": 1,
        "effective_year": 2024, "isdeleted": False
    },
    {
        "id": "CUR003", "day": 12, "month": 4, "year": 2024,
        "quantity": 500000.0, "type": "currency", "currency_type": 0,
        "exchange_rate_id": 1, "exchange_rate": 1.0, "effective_day": 1,
        "effective_month": 1, "effective_year": 2024, "isdeleted": False
    },
    {
        "id": "CUR004", "day": 25, "month": 4, "year": 2024, "quantity": 70.0,
        "type": "currency", "currency_type": 1, "exchange_rate_id": 2,
        "exchange_rate": 25137.0, "effective_day": 1, "effective_month": 1,
        "effective_year": 2024, "isdeleted": False
    },
    {
        "id": "CUR005", "day": 11, "month": 4, "year": 2024, "quantity": 200.0,
        "type": "currency", "currency_type": 2, "exchange_rate_id": 3,
        "exchange_rate": 26777.56, "effective_day": 1, "effective_month": 1,
        "effective_year": 2024, "isdeleted": False
    },
    {
        "id": "CUR006", "day": 15, "month": 6, "year": 2024,
        "quantity": 90000000.0, "type": "currency", "currency_type": 0,
        "exchange_rate_id": 1, "exchange_rate": 1.0, "effective_day": 1,
        "effective_month": 1, "effective_year": 2024, "isdeleted": False
    }
]

# exchange_rates
exchange_rates_data = [
    {
        "id": 1, "currency_type": 0, "rate": 1.0, "effective_day": 1,
        "effective_month": 1, "effective_year": 2024
    },
    {
        "id": 2, "currency_type": 1, "rate": 25137.0, "effective_day": 1,
        "effective_month": 1, "effective_year": 2024
    },
    {
        "id": 3, "currency_type": 2, "rate": 26777.56, "effective_day": 1,
        "effective_month": 1, "effective_year": 2024
    }
]

df_transactions = pd.DataFrame(transactions_data)
df_exchange_rates = pd.DataFrame(exchange_rates_data)

# Write file for testing
# with pd.ExcelWriter("data.xlsx") as writer:
#     df_transactions.to_excel(writer, sheet_name="transactions", index=False)
#     df_exchange_rates.to_excel(
#         writer, sheet_name="exchange_rates", index=False)

# Theme
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")


class TransactionApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Transaction Management")
        icon_path = "./logo.ico"
        self.iconbitmap(icon_path)
        self.minsize(1720, 960)

        self.current_theme = "Dark-Blue"

        self.transaction_list = TransactionList()
        self.load_data_from_excel()
        self.create_widget()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widget(self):
        self.header_frame = HeaderFrame(
            master=self, initial_theme=self.current_theme)
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.tab_filter = TabFilter(master=self)
        self.tab_filter.grid(row=1, column=0, padx=10, pady=(0, 10),
                             sticky="ew")

        self.grid_columnconfigure(0, weight=1)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.quit()
                self.destroy()
            except Exception as e:
                print(f"Error during closing: {e}")

    def load_data_from_excel(self):
        try:
            df_transactions = pd.read_excel("data.xlsx",
                                            sheet_name="transactions")
            df_exchange_rates = pd.read_excel("data.xlsx",
                                              sheet_name="exchange_rates")

            if not self.check_data_validity(df_transactions):
                return

            for _, row in df_transactions.iterrows():
                if row['isdeleted']:
                    continue

                if row['type'] == "gold":
                    transaction = GoldTransaction(
                        row['id'],
                        row['day'],
                        row['month'],
                        row['year'],
                        row['unit_price'],
                        row['quantity'],
                        GoldType(row['gold_type']),
                        isdeleted=row['isdeleted']
                    )
                elif row['type'] == "currency":
                    exchange_rate = ExchangeRate(
                        row['exchange_rate_id'],
                        CurrencyType(row['currency_type']),
                        row['exchange_rate'],
                        row['effective_day'],
                        row['effective_month'],
                        row['effective_year']
                    )
                    transaction = CurrencyTransaction(
                        row['id'],
                        row['day'],
                        row['month'],
                        row['year'],
                        row['quantity'],
                        CurrencyType(row['currency_type']),
                        exchange_rate,
                        isdeleted=row['isdeleted']
                    )
                else:
                    continue

                self.transaction_list.add_transaction(transaction)

            for _, row in df_exchange_rates.iterrows():
                _ = ExchangeRate(
                    row['id'],
                    CurrencyType(row['currency_type']),
                    row['rate'],
                    row['effective_day'],
                    row['effective_month'],
                    row['effective_year']
                )

        except FileNotFoundError:
            messagebox.showerror("Error", "Data file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def refresh_data_from_excel(self):
        messagebox.showinfo("Refreshing Data",
                            "Refreshing data. Please wait...")

        self.transaction_list.clear()
        self.load_data_from_excel()

        if self.header_frame is not None:
            self.header_frame.destroy()
        if self.tab_filter is not None:
            self.tab_filter.destroy()

        self.create_widget()

    def convert_to_int(self, value, field_name, row_index):
        try:
            return int(value)
        except ValueError:
            messagebox.showerror("Data Error", f"Invalid '{
                field_name}' at row {row_index + 1}")
            return None

    def convert_to_float(self, value, field_name, row_index):
        try:
            return float(value)
        except ValueError:
            messagebox.showerror("Data Error", f"Invalid '{
                field_name}' at row {row_index + 1}")
            return None

    def check_data_validity(self, df):
        for idx, row in df.iterrows():
            if pd.isna(row['id']) or not isinstance(row['id'], str):
                messagebox.showerror("Data Error", f"Invalid 'id' at row {
                    idx + 1}")
                return False

            day = self.convert_to_int(row['day'], 'day', idx)
            month = self.convert_to_int(row['month'], 'month', idx)
            year = self.convert_to_int(row['year'], 'year', idx)
            if day is None or month is None or year is None:
                return False

            if not (1 <= day <= 31):
                messagebox.showerror(
                    "Data Error", f"Invalid 'day' at row {idx + 1}")
                return False
            if not (1 <= month <= 12):
                messagebox.showerror(
                    "Data Error", f"Invalid 'month' at row {idx + 1}")
                return False

            if row['type'] == "gold":
                unit_price = self.convert_to_float(
                    row['unit_price'], 'unit_price', idx)
                quantity = self.convert_to_float(row['quantity'], 'quantity',
                                                 idx)
                gold_type = self.convert_to_int(row['gold_type'], 'gold_type',
                                                idx)
                if unit_price is None or quantity is None or gold_type is None:
                    return False
            elif row['type'] == "currency":
                quantity = self.convert_to_float(row['quantity'], 'quantity',
                                                 idx)
                currency_type = self.convert_to_int(
                    row['currency_type'], 'currency_type', idx)
                exchange_rate_id = self.convert_to_int(
                    row['exchange_rate_id'], 'exchange_rate_id', idx)
                exchange_rate = self.convert_to_float(
                    row['exchange_rate'], 'exchange_rate', idx)
                effective_day = self.convert_to_int(
                    row['effective_day'], 'effective_day', idx)
                effective_month = self.convert_to_int(
                    row['effective_month'], 'effective_month', idx)
                effective_year = self.convert_to_int(
                    row['effective_year'], 'effective_year', idx)
                if quantity is None or currency_type is None or \
                        exchange_rate_id is None or exchange_rate is \
                        None or effective_day is None or effective_month is \
                        None or effective_year is None:
                    return False
                if not (1 <= effective_day <= 31):
                    messagebox.showerror(
                        "Data Error", f"Invalid 'effective_day' at row {
                            idx + 1}")
                    return False
                if not (1 <= effective_month <= 12):
                    messagebox.showerror(
                        "Data Error", f"Invalid 'effective_month' at row {
                            idx + 1}")
                    return False
            else:
                messagebox.showerror(
                    "Data Error", f"Invalid 'type' at row {idx + 1}")
                return False
        return True

    def update_theme(self, new_theme):
        update_message = messagebox.showinfo(
            "Updating Theme", "Updating theme. Please wait a moment...")

        self.current_theme = new_theme
        self.header_frame.destroy()
        self.tab_filter.destroy()

        self.create_widget()

        if update_message:
            self.focus()


class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, initial_theme="Dark-Blue", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#dbdbdb", bg_color="#f2f2f2")
        self.refresh_icon = customtkinter.CTkImage(
            Image.open('./refresh.ico'))
        self.filter_icon = customtkinter.CTkImage(
            Image.open('./filter.ico'))
        self.search_icon = customtkinter.CTkImage(
            Image.open('./search.ico'))

        self.label_transaction = customtkinter.CTkLabel(
            self, text="Transaction", text_color="black",
            font=("TkDefaultFont", 24, "bold"))
        self.label_transaction.grid(
            row=0, column=0, sticky="w", padx=12, pady=5)

        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.grid(row=0, column=1, sticky="e", padx=12, pady=5)
        self.buttons_frame.configure(fg_color="transparent")

        self.btn_search = customtkinter.CTkButton(
            self.buttons_frame,
            text=None,
            image=self.search_icon,
            width=30, height=30, command=self.open_search_window)
        self.btn_search.pack(side="right", padx=5, pady=5)

        self.search_window = None

        self.btn_filter = customtkinter.CTkButton(
            self.buttons_frame,
            text=None,
            image=self.filter_icon,
            width=30, height=30, command=self.open_filter_window)
        self.btn_filter.pack(side="right", padx=5, pady=5)

        self.filter_window = None

        self.btn_refresh = customtkinter.CTkButton(
            self.buttons_frame,
            text=None,
            image=self.refresh_icon,
            fg_color="green",
            hover_color="dark green",
            width=30, height=30)
        self.btn_refresh.configure(command=self.master.refresh_data_from_excel)
        self.btn_refresh.pack(side="right", padx=5, pady=5)

        self.btn_add_transaction = customtkinter.CTkButton(
            self.buttons_frame, text="ADD TRANSACTION",
            command=self.open_add_transaction_window)
        self.btn_add_transaction.pack(side="right", padx=5, pady=5)

        self.add_transaction_window = None

        self.btn_report = customtkinter.CTkButton(
            self.buttons_frame, text="REPORT", text_color="#1f6aa5",
            border_width=1,
            border_color="#1f6aa5", fg_color="white",
            hover_color="light blue",
            command=self.open_report_window)
        self.btn_report.pack(side="right", padx=5, pady=5)

        self.report_window = None

        self.vertical_separator = customtkinter.CTkFrame(
            self.buttons_frame, width=2, height=30, fg_color="grey")
        self.vertical_separator.pack(side="right", padx=5, pady=5, fill="y")

        self.optionmenu_theme = customtkinter. \
            CTkOptionMenu(self.buttons_frame,
                          values=[
                              "Dark-Blue", "Blue", "Green"],
                          command=self.option_menu_theme_callback)
        self.optionmenu_theme.set(initial_theme)
        self.optionmenu_theme.pack(side="right", padx=5, pady=5)

        theme_label = customtkinter.CTkLabel(
            self.buttons_frame, text="Theme: ", text_color="black",
            font=("Arial", 14, "bold"))
        theme_label.pack(side="right", padx=0, pady=5)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def option_menu_theme_callback(self, choice):
        if choice == "Dark-Blue":
            customtkinter.set_default_color_theme("dark-blue")
        elif choice == "Blue":
            customtkinter.set_default_color_theme("blue")
        elif choice == "Green":
            customtkinter.set_default_color_theme("green")
        self.master.update_theme(choice)

    def open_filter_window(self):
        if self.filter_window is None or not \
                self.filter_window.winfo_exists():
            self.filter_window = FilterWindow(self)
            self.filter_window.after(10, self.filter_window.lift)
        else:
            self.filter_window.focus()

    def open_search_window(self):
        if self.search_window is None or not \
                self.search_window.winfo_exists():
            self.search_window = SearchWindow(self)
            self.search_window.after(10, self.search_window.lift)
        else:
            self.search_window.focus()

    def open_add_transaction_window(self):
        if self.add_transaction_window is None or not \
                self.add_transaction_window.winfo_exists():
            self.add_transaction_window = AddTransactionWindow(self)
            self.add_transaction_window.after(10,
                                              self.add_transaction_window.lift)
        else:
            self.add_transaction_window.focus()

    def open_report_window(self):
        if self.report_window is None or not \
                self.report_window.winfo_exists():
            self.report_window = ReportWindow(self)
            self.report_window.after(10, self.report_window.lift)
        else:
            self.report_window.focus()


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


class TabGroupBySortByType(Enum):
    GROUPBYDATE = 0
    GROUPBYCATEGORY = 1
    SORTBYDATE = 2
    SORTBYTOTALAMOUNT = 3


class TabGroupBySortBy(customtkinter.CTkTabview):
    def __init__(self, master, transactions, **kwargs):
        super().__init__(master, **kwargs)
        self.transactions = transactions
        self.configure(fg_color="#dbdbdb", bg_color="#ffffff")

        self.tab_group_by = self.add("GROUP BY")
        self.tab_sort_by = self.add("SORT BY")

        self.set("GROUP BY")
        self.configure(corner_radius=5)

        self.option_segmented_button_date = True
        self.option_segmented_button_total_amount = True

        self.gold_treeviews = {}
        self.currency_treeviews = {}

        self.create_tab_group_by_sort_by_widgets()

    def create_tab_group_by_sort_by_widgets(self):
        # Group By
        self.create_option_menu_group_by()

        self.date_frame = self.create_date_group_by_frame(
            self.tab_group_by, self.transactions)
        self.category_frame = self.create_category_group_by_frame(
            self.tab_group_by, self.transactions)

        self.category_frame.pack_forget()

        self.show_default_frame_group_by()

        # Sort By
        self.buttons_frame = customtkinter.CTkFrame(self.tab_sort_by)
        self.buttons_frame.pack(padx=10, pady=5, fill="x")
        self.buttons_frame.configure(fg_color="transparent")
        self.create_option_menu_sort_by(self.buttons_frame)
        self.create_segmented_button_sort_by(
            self.buttons_frame)
        self.grid_columnconfigure(0, weight=1)

        self.date_sort_by_frame = \
            self.create_date_sort_by_frame(
                self.tab_sort_by, self.transactions,
                option=self.option_segmented_button_date)
        self.total_amount_sort_by_frame = \
            self.create_total_amount_sort_by_frame(
                self.tab_sort_by, self.transactions,
                option=self.option_segmented_button_total_amount)

        self.total_amount_sort_by_frame.pack_forget()

        self.show_default_frame_sort_by()

    # Set up Tab View
    def show_default_frame_group_by(self):
        self.gold_treeviews = {}
        self.currency_treeviews = {}
        self.show_frame(self.date_frame)
        self.hide_frame(self.category_frame)

    def show_default_frame_sort_by(self):
        self.gold_treeviews = {}
        self.currency_treeviews = {}
        self.show_frame(self.date_sort_by_frame)
        self.hide_frame(self.total_amount_sort_by_frame)

    def create_option_menu_group_by(self):
        self.buttons_frame = customtkinter.CTkFrame(self.tab_group_by)
        self.buttons_frame.pack(padx=10, pady=5, fill="x")
        self.buttons_frame.configure(fg_color="transparent")

        self.optionmenu = customtkinter. \
            CTkOptionMenu(self.buttons_frame,
                          values=[
                              "Date", "Category"],
                          command=self.option_menu_group_by_callback)
        self.optionmenu.set("Date")
        self.optionmenu.pack(padx=10, pady=0, side="left")

        self.grid_columnconfigure(0, weight=1)

    def create_option_menu_sort_by(self, frame):
        self.optionmenu = customtkinter. \
            CTkOptionMenu(frame,
                          values=[
                              "Date", "Total Amount"],
                          command=self.option_menu_sort_by_callback)
        self.optionmenu.set("Date")
        self.optionmenu.pack(padx=10, pady=0, side="left")

    def create_segmented_button_sort_by(self, frame):
        self.segmented_button = customtkinter.CTkSegmentedButton(
            frame,
            values=["Descending", "Ascending"],
            command=self.segmented_button_callback
        )
        self.segmented_button.set("Descending")
        self.segmented_button.pack(padx=(5, 10), pady=0, side="left")

    def option_menu_group_by_callback(self, choice):
        if choice == "Date":
            self.show_frame(self.date_frame)
            self.hide_frame(self.category_frame)
        elif choice == "Category":
            self.show_frame(self.category_frame)
            self.hide_frame(self.date_frame)

    def option_menu_sort_by_callback(self, choice):
        if choice == "Date":
            self.show_frame(self.date_sort_by_frame)
            self.hide_frame(self.total_amount_sort_by_frame)
            if self.option_segmented_button_date:
                self.segmented_button.set("Descending")
            else:
                self.segmented_button.set("Ascending")
        elif choice == "Total Amount":
            self.show_frame(self.total_amount_sort_by_frame)
            self.hide_frame(self.date_sort_by_frame)
            if self.option_segmented_button_total_amount:
                self.segmented_button.set("Descending")
            else:
                self.segmented_button.set("Ascending")

    def segmented_button_callback(self, selected_option):
        option = self.optionmenu.get()
        if option == "Date":
            self.option_segmented_button_date = selected_option == "Descending"
            self.update_date_sort_by_frame()
        elif option == "Total Amount":
            self.option_segmented_button_total_amount = \
                selected_option == "Descending"
            self.update_total_amount_sort_by_frame()

    def update_date_sort_by_frame(self):
        self.date_sort_by_frame.pack_forget()
        self.date_sort_by_frame.destroy()

        self.date_sort_by_frame = self.create_date_sort_by_frame(
            self.tab_sort_by, self.transactions,
            option=self.option_segmented_button_date)

        self.show_default_frame_sort_by()

    def update_total_amount_sort_by_frame(self):
        self.total_amount_sort_by_frame.pack_forget()
        self.total_amount_sort_by_frame.destroy()

        self.total_amount_sort_by_frame = \
            self.create_total_amount_sort_by_frame(
                self.tab_sort_by, self.transactions,
                option=self.option_segmented_button_total_amount)

        self.show_frame(self.total_amount_sort_by_frame)
        self.hide_frame(self.date_sort_by_frame)

    # Group By Frame
    def create_date_group_by_frame(self, parent, transactions):
        frame = customtkinter.CTkScrollableFrame(
            parent, fg_color="transparent",
            height=530)

        self.get_date_in_transactions(frame, transactions)

        return frame

    def create_category_group_by_frame(self, parent, transactions):
        frame = customtkinter.CTkScrollableFrame(
            parent, fg_color="transparent",
            height=530)

        self.create_content_treeview_by_category(
            frame, transactions)

        return frame

    # Group By Date
    def get_date_in_transactions(self, parent, transactions):
        unique_dates = set()

        for transaction in transactions:
            day = transaction._day
            month = MonthLabel(transaction._month)
            year = transaction._year

            date_object = datetime.date(year, month.value, day)

            unique_dates.add(date_object)

        sorted_dates = sorted(unique_dates, reverse=True)

        for date_obj in sorted_dates:
            day = date_obj.day
            month = MonthLabel(date_obj.month)
            year = date_obj.year

            group_by_date_items_frame = self.create_group_by_date_items_frame(
                parent, day, month, year, transactions=transactions)
            group_by_date_items_frame.pack(padx=5, pady=(5, 10), fill="x")

    def create_group_by_date_items_frame(self, parent, day, month, year,
                                         transactions):
        frame = customtkinter.CTkFrame(
            parent, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")

        frame_date = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_date.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=5)

        day_label = customtkinter.CTkLabel(
            frame_date, text=str(day), text_color="black",
            font=("Arial", 55, "bold"))
        day_label.pack(padx=5, pady=0, side="left")

        frame_month_year = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_month_year.grid(row=0, column=1, sticky="e", padx=0, pady=0)

        month_label = customtkinter.CTkLabel(
            frame_month_year, text=str(month), text_color="black",
            font=("Arial", 14))
        month_label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

        year_label = customtkinter.CTkLabel(
            frame_month_year, text=str(year), text_color="black",
            font=("Arial", 14))
        year_label.grid(row=1, column=0, padx=5, pady=0, sticky="w")

        frame_total_amount = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_total_amount.grid(row=0, column=2, sticky="e", padx=10, pady=5)

        total_amount_label = customtkinter.CTkLabel(
            frame_total_amount, text="Total Amount (VND)", text_color="black",
            font=("Arial", 14))
        total_amount_label.grid(row=0, column=0, padx=5, pady=0, sticky="e")

        total_amount_number_label = customtkinter.CTkLabel(
            frame_total_amount, text="", text_color="black",
            font=("Arial", 20, "bold"))
        total_amount_number_label.grid(
            row=1, column=0, padx=5, pady=0, sticky="e")

        total_amount = self.calculate_total_amount_by_date(
            transactions, day, month, year)
        formatted_total_amount = self.format_price_number(
            total_amount)
        total_amount_number_label.configure(text=str(formatted_total_amount))

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=3,
                       sticky="ew", padx=10, pady=5)

        frame_treeviews = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_treeviews.grid(row=2, column=0, padx=5,
                             pady=5, sticky="ew", columnspan=3)

        self.create_content_treeview_by_date(
            frame_treeviews, transactions, day, month, year)

        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)

        return frame

    def calculate_total_amount_by_date(self, transactions, day, month, year):
        total_amount = 0
        for transaction in transactions:
            if (transaction._day, MonthLabel(transaction._month),
                    transaction._year) == (day, month, year):
                total_amount += transaction._total_amount
        return total_amount

    def create_content_treeview_by_date(self, frame, transactions,
                                        day, month, year):
        self.selected_gold_status = False
        self.selected_currency_status = False

        if (day, month, year) not in self.gold_treeviews:
            gold_treeview = \
                self.create_gold_transaction_treeview_by_date(frame)
            self.populate_treeview_with_gold_transactions_by_date(
                gold_treeview, transactions, day, month, year)
            gold_treeview.pack(padx=10, pady=10, fill="x")
            self.gold_treeviews[(day, month, year)] = gold_treeview
        else:
            gold_treeview = self.gold_treeviews[(day, month, year)]

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=10, pady=10, fill="x")

        if (day, month, year) not in self.currency_treeviews:
            currency_treeview = \
                self.create_currency_transaction_treeview_by_date(
                    frame)
            self.populate_treeview_with_currency_transactions_by_date(
                currency_treeview, transactions, day, month, year)
            currency_treeview.pack(padx=10, pady=10, fill="x")
            self.currency_treeviews[(day, month, year)] = currency_treeview
        else:
            currency_treeview = self.currency_treeviews[(day, month, year)]

        gold_treeview.bind('<<TreeviewSelect>>', lambda event:
                           self.on_gold_treeview_select(
                               event,
                               tab_type=TabGroupBySortByType.GROUPBYDATE,
                               transactions=transactions))
        currency_treeview.bind('<<TreeviewSelect>>',
                               lambda event: self.on_currency_treeview_select(
                                   event,
                                   tab_type=TabGroupBySortByType.GROUPBYDATE,
                                   transactions=transactions))

    def create_gold_transaction_treeview_by_date(self, frame):
        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        gold_transaction_label = customtkinter.CTkLabel(
            frame_label_actions, text="GOLD TRANSACTIONS", text_color="black",
            font=("Arial", 16, "bold"))
        gold_transaction_label.grid(row=0, column=0, padx=0, pady=0,
                                    sticky="w")
        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=0, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_gold_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_gold_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_gold_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_gold_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_gold_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_gold_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            # "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type", "Total Amount (VND)"
        ), show="headings", height=5)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        # treeview.heading("Transaction Date",
        #                  text="Transaction Date", anchor="w")
        treeview.heading("Unit Price (VND/tael)",
                         text="Unit Price (VND/tael)", anchor="w")
        treeview.heading("Quantity (tael)", text="Quantity (tael)", anchor="w")
        treeview.heading("Gold Type", text="Gold Type", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")

        return treeview

    def create_currency_transaction_treeview_by_date(self, frame):
        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        currency_transaction_label = customtkinter.CTkLabel(
            frame_label_actions, text="CURRENCY TRANSACTIONS",
            text_color="black",
            font=("Arial", 16, "bold"))
        currency_transaction_label.grid(row=0, column=0, padx=0, pady=0,
                                        sticky="w")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=0, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_currency_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_currency_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_currency_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_currency_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_currency_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_currency_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            # "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)", "Total Amount (VND)"
        ), show="headings", height=5)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        # treeview.heading("Transaction Date",
        #                  text="Transaction Date", anchor="w")
        treeview.heading("Quantity", text="Quantity", anchor="w")
        treeview.heading("Currency Type", text="Currency Type", anchor="w")
        treeview.heading("Exchange Rate (VND)",
                         text="Exchange Rate (VND)", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")
        return treeview

    def populate_treeview_with_gold_transactions_by_date(self, treeview,
                                                         transactions,
                                                         day, month, year):
        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                if (transaction._day, MonthLabel(transaction._month),
                        transaction._year) == (day, month, year):
                    # transaction_date = "{} {} {}".format(
                    #     transaction._day, MonthLabel(transaction._month),
                    #     transaction._year)
                    formatted_unit_price = self.format_price_number(
                        transaction._unit_price)
                    formatted_total_amount = self.format_price_number(
                        transaction._total_amount)
                    treeview.insert("", "end", values=(
                        transaction._id,
                        # transaction_date,
                        formatted_unit_price,
                        transaction._quantity,
                        transaction._gold_type.name,
                        formatted_total_amount
                    ))

    def populate_treeview_with_currency_transactions_by_date(self, treeview,
                                                             transactions,
                                                             day, month, year):
        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                if (transaction._day, MonthLabel(transaction._month),
                        transaction._year) == (day, month, year):
                    # transaction_date = "{} {} {}".format(
                    #     transaction._day, MonthLabel(transaction._month),
                    #     transaction._year)
                    formatted_quantity = self.format_price_number(
                        transaction._quantity)
                    formatted_exchange_rate = self.format_price_number(
                        transaction._exchange_rate._rate)
                    formatted_total_amount = self.format_price_number(
                        transaction._total_amount)
                    treeview.insert("", "end", values=(
                        transaction._id,
                        # transaction_date,
                        formatted_quantity,
                        transaction._currency_type.name,
                        formatted_exchange_rate,
                        formatted_total_amount
                    ))

    # Group By Category
    def create_content_treeview_by_category(self, frame, transactions):
        gold_transactions = [transaction for transaction in transactions
                             if isinstance(
                                 transaction, GoldTransaction)]
        currency_transactions = [transaction for transaction in transactions
                                 if isinstance(
                                     transaction, CurrencyTransaction)]

        frame_gold = customtkinter.CTkFrame(
            frame, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")
        frame_gold.pack(padx=5, pady=5, fill="x")

        treeview_gold_transaction = \
            self.create_gold_transaction_treeview_by_category(
                frame_gold, gold_transactions)
        self.populate_treeview_with_gold_transactions_by_category(
            treeview_gold_transaction, gold_transactions)
        treeview_gold_transaction.pack(padx=20, pady=(10, 20), fill="x")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=10, pady=10, fill="x")

        frame_currency = customtkinter.CTkFrame(
            frame, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")
        frame_currency.pack(padx=5, pady=5, fill="x")

        treeview_currency_transaction \
            = self.create_currency_transaction_treeview_by_category(
                frame_currency, currency_transactions)
        self.populate_treeview_with_currency_transactions_by_category(
            treeview_currency_transaction, currency_transactions)
        treeview_currency_transaction.pack(padx=20, pady=(10, 20), fill="x")

        treeview_gold_transaction.bind(
            '<<TreeviewSelect>>', lambda event:
            self.on_gold_treeview_select(
                event,
                tab_type=TabGroupBySortByType.GROUPBYCATEGORY,
                transactions=transactions))
        treeview_currency_transaction.bind(
            '<<TreeviewSelect>>', lambda event:
            self.on_currency_treeview_select(
                event,
                tab_type=TabGroupBySortByType.GROUPBYCATEGORY,
                transactions=transactions))

    def create_header_transaction_treeview(self, frame, total_amount, label):
        frame_header = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_header.pack(padx=5, pady=5, fill="x")

        frame_label = customtkinter.CTkFrame(
            frame_header, fg_color="transparent")
        frame_label.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=5)

        gold_transaction_label = customtkinter.CTkLabel(
            frame_label, text=label, text_color="black",
            font=("Arial", 30, "bold"))
        gold_transaction_label.pack(
            padx=10, pady=(5, 0), side="top", anchor="w")

        frame_total_amount = customtkinter.CTkFrame(
            frame_header, fg_color="transparent")
        frame_total_amount.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        total_amount_label = customtkinter.CTkLabel(
            frame_total_amount, text="Total Amount (VND)", text_color="black",
            font=("Arial", 14))
        total_amount_label.grid(row=0, column=0, padx=5, pady=0, sticky="e")

        total_amount_number_label = customtkinter.CTkLabel(
            frame_total_amount, text="{}".format(total_amount),
            text_color="black",
            font=("Arial", 20, "bold"))
        total_amount_number_label.grid(
            row=1, column=0, padx=5, pady=0, sticky="e")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame_header, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=3,
                       sticky="ew", padx=10, pady=5)

        frame_header.columnconfigure(0, weight=1)
        frame_header.columnconfigure(1, weight=1)

    def calculate_total_amount_by_category(self, transactions):
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction._total_amount
        return total_amount

    def create_gold_transaction_treeview_by_category(self, frame,
                                                     gold_transactions):
        total_amount_gold = self.calculate_total_amount_by_category(
            gold_transactions)
        formatted_total_amount_gold = self.format_price_number(
            total_amount_gold)
        self.create_header_transaction_treeview(
            frame, formatted_total_amount_gold, "GOLD TRANSACTIONS")

        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=7, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_gold_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_gold_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_gold_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_gold_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_gold_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_gold_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type", "Total Amount (VND)"
        ), show="headings", height=10)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Unit Price (VND/tael)",
                         text="Unit Price (VND/tael)", anchor="w")
        treeview.heading("Quantity (tael)", text="Quantity (tael)", anchor="w")
        treeview.heading("Gold Type", text="Gold Type", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")

        return treeview

    def create_currency_transaction_treeview_by_category(self, frame,
                                                         currency_transactions
                                                         ):
        total_amount_currency = self.calculate_total_amount_by_category(
            currency_transactions)
        formatted_total_amount_currency = self.format_price_number(
            total_amount_currency)
        self.create_header_transaction_treeview(
            frame, formatted_total_amount_currency, "CURRENCY TRANSACTIONS")

        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=7, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_currency_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_currency_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_currency_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_currency_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_currency_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_currency_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)", "Total Amount (VND)"
        ), show="headings", height=10)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Quantity", text="Quantity", anchor="w")
        treeview.heading("Currency Type", text="Currency Type", anchor="w")
        treeview.heading("Exchange Rate (VND)",
                         text="Exchange Rate (VND)", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")
        return treeview

    def populate_treeview_with_gold_transactions_by_category(self, treeview,
                                                             transactions):
        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_unit_price = self.format_price_number(
                    transaction._unit_price)
                formatted_total_amount = self.format_price_number(
                    transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_unit_price,
                    transaction._quantity,
                    transaction._gold_type.name,
                    formatted_total_amount
                ))

    def populate_treeview_with_currency_transactions_by_category(self,
                                                                 treeview,
                                                                 transactions):
        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_quantity = self.format_price_number(
                    transaction._quantity)
                formatted_exchange_rate = self.format_price_number(
                    transaction._exchange_rate._rate)
                formatted_total_amount = self.format_price_number(
                    transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_quantity,
                    transaction._currency_type.name,
                    formatted_exchange_rate,
                    formatted_total_amount
                ))

    # Sort By Frame
    def create_date_sort_by_frame(self, parent, transactions, option):
        frame = customtkinter.CTkScrollableFrame(
            parent, fg_color="transparent",
            height=530)

        self.get_date_in_transactions_with_option_sort(
            frame, transactions, option)

        return frame

    def create_total_amount_sort_by_frame(self, parent, transactions, option):
        frame = customtkinter.CTkScrollableFrame(
            parent, fg_color="transparent",
            height=530)

        self.create_content_treeview_sort_by_total_amount(
            frame, transactions, option)

        return frame

    # Sort By Date
    def get_date_in_transactions_with_option_sort(self, parent, transactions,
                                                  option):
        unique_dates = set()

        for transaction in transactions:
            day = transaction._day
            month = MonthLabel(transaction._month)
            year = transaction._year

            date_object = datetime.date(year, month.value, day)

            unique_dates.add(date_object)

        sorted_dates = sorted(unique_dates, reverse=option)

        for date_obj in sorted_dates:
            day = date_obj.day
            month = MonthLabel(date_obj.month)
            year = date_obj.year

            group_by_date_items_frame = self.create_group_by_date_items_frame(
                parent, day, month, year, transactions=transactions)
            group_by_date_items_frame.pack(padx=5, pady=(5, 10), fill="x")

    # Sort By Total Amount
    def create_content_treeview_sort_by_total_amount(self, frame,
                                                     transactions, option):
        sorted_transactions = sorted(
            transactions, key=lambda x: x._total_amount, reverse=option)

        for transaction in sorted_transactions:
            transaction_list = [transaction]
            self.create_frame_for_content_treeview(
                frame, transaction_list)

    def create_frame_for_content_treeview(self, frame, transactions):
        frame_items = customtkinter.CTkFrame(
            frame, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")
        frame_items.pack(padx=5, pady=5, fill="x")

        if transactions:
            if isinstance(transactions[0], GoldTransaction):
                treeview_transaction = \
                    self.create_gold_tv_sort_by_total_amount(
                        frame_items, transactions)
                self.populate_tv_with_gold_sort_by_total_amount(
                    treeview_transaction, transactions)
                treeview_transaction.bind(
                    '<<TreeviewSelect>>', lambda event:
                    self.on_gold_treeview_select(
                        event,
                        tab_type=TabGroupBySortByType.SORTBYTOTALAMOUNT,
                        transactions=transactions))
            elif isinstance(transactions[0], CurrencyTransaction):
                treeview_transaction \
                    = self.create_currency_tv_sort_by_total_amount(
                        frame_items, transactions)
                self.populate_tv_with_currency_sort_by_total_amount(
                    treeview_transaction, transactions)
                treeview_transaction.bind(
                    '<<TreeviewSelect>>', lambda event:
                    self.on_currency_treeview_select(
                        event,
                        tab_type=TabGroupBySortByType.SORTBYTOTALAMOUNT,
                        transactions=transactions))

            treeview_transaction.pack(
                padx=20, pady=(10, 20), fill="x")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=10, pady=10, fill="x")

    def create_header_transaction_treeview_sort_by(self, frame,
                                                   total_amount, label):
        frame_header = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_header.pack(padx=5, pady=5, fill="x")

        frame_label = customtkinter.CTkFrame(
            frame_header, fg_color="transparent")
        frame_label.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=5)

        gold_transaction_label = customtkinter.CTkLabel(
            frame_label, text=label, text_color="black",
            font=("Arial", 30, "bold"))
        gold_transaction_label.pack(
            padx=10, pady=(5, 0), side="top", anchor="w")

        frame_total_amount = customtkinter.CTkFrame(
            frame_header, fg_color="transparent")
        frame_total_amount.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        total_amount_label = customtkinter.CTkLabel(
            frame_total_amount, text="Total Amount (VND)", text_color="black",
            font=("Arial", 14))
        total_amount_label.grid(row=0, column=0, padx=5, pady=0, sticky="e")

        total_amount_number_label = customtkinter.CTkLabel(
            frame_total_amount, text="{}".format(total_amount),
            text_color="black",
            font=("Arial", 20, "bold"))
        total_amount_number_label.grid(
            row=1, column=0, padx=5, pady=0, sticky="e")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame_header, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=3,
                       sticky="ew", padx=10, pady=5)

        frame_header.columnconfigure(0, weight=1)
        frame_header.columnconfigure(1, weight=1)

    def calculate_total_amount_sort_by_total_amount(self, transactions):
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction._total_amount
        return total_amount

    def create_gold_tv_sort_by_total_amount(self, frame,
                                            gold_transactions):
        total_amount_gold = self.calculate_total_amount_sort_by_total_amount(
            gold_transactions)
        formatted_total_amount_gold = self.format_price_number(
            total_amount_gold)
        self.create_header_transaction_treeview_sort_by(
            frame, formatted_total_amount_gold, "GOLD TRANSACTIONS")

        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=7, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_gold_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_gold_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_gold_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_gold_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_gold_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_gold_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type",
            # "Total Amount (VND)"
        ), show="headings", height=1)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Unit Price (VND/tael)",
                         text="Unit Price (VND/tael)", anchor="w")
        treeview.heading("Quantity (tael)", text="Quantity (tael)", anchor="w")
        treeview.heading("Gold Type", text="Gold Type", anchor="w")
        # treeview.heading("Total Amount (VND)",
        #                  text="Total Amount (VND)", anchor="w")

        return treeview

    def create_currency_tv_sort_by_total_amount(self, frame,
                                                currency_transactions
                                                ):
        total_amount_currency = \
            self.calculate_total_amount_sort_by_total_amount(
                currency_transactions)
        formatted_total_amount_currency = self.format_price_number(
            total_amount_currency)
        self.create_header_transaction_treeview_sort_by(
            frame, formatted_total_amount_currency, "CURRENCY TRANSACTIONS")

        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=7, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_currency_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_currency_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_currency_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_currency_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_currency_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_currency_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)",
            # "Total Amount (VND)"
        ), show="headings", height=1)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Quantity", text="Quantity", anchor="w")
        treeview.heading("Currency Type", text="Currency Type", anchor="w")
        treeview.heading("Exchange Rate (VND)",
                         text="Exchange Rate (VND)", anchor="w")
        # treeview.heading("Total Amount (VND)",
        #                  text="Total Amount (VND)", anchor="w")
        return treeview

    def populate_tv_with_gold_sort_by_total_amount(self,
                                                   treeview,
                                                   transactions):
        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_unit_price = self.format_price_number(
                    transaction._unit_price)
                # formatted_total_amount = self.format_price_number(
                #     transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_unit_price,
                    transaction._quantity,
                    transaction._gold_type.name,
                    # formatted_total_amount
                ))

    def populate_tv_with_currency_sort_by_total_amount(self,
                                                       treeview,
                                                       transactions):
        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_quantity = self.format_price_number(
                    transaction._quantity)
                formatted_exchange_rate = self.format_price_number(
                    transaction._exchange_rate._rate)
                # formatted_total_amount = self.format_price_number(
                #     transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_quantity,
                    transaction._currency_type.name,
                    formatted_exchange_rate,
                    # formatted_total_amount
                ))

    # General auxiliary functions
    def on_gold_treeview_select(self, event, tab_type, transactions):
        if tab_type == TabGroupBySortByType.GROUPBYDATE or \
                tab_type == TabGroupBySortByType.SORTBYDATE:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_gold_status = True
                self.selected_gold_transaction_code = values[0]
                self.selected_gold_unit_price = values[1]
                self.selected_gold_quantity = values[2]
                self.selected_gold_type = values[3]
                self.selected_gold_total_amount = values[4]

                self.selected_gold_transaction_date = None

                for transaction in transactions:
                    if isinstance(transaction, GoldTransaction):
                        if str(transaction._id) == \
                                str(self.selected_gold_transaction_code):
                            day = transaction._day
                            month = transaction._month
                            year = transaction._year

                            month_name = str(MonthLabel(month))

                            formatted_date = f"{day} {month_name} {year}"

                            self.selected_gold_transaction_date \
                                = formatted_date
                            break

            else:
                self.selected_gold_status = False

        if tab_type == TabGroupBySortByType.GROUPBYCATEGORY:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_gold_status = True
                self.selected_gold_transaction_code = values[0]
                self.selected_gold_transaction_date = values[1]
                self.selected_gold_unit_price = values[2]
                self.selected_gold_quantity = values[3]
                self.selected_gold_type = values[4]
                self.selected_gold_total_amount = values[5]
            else:
                self.selected_gold_status = False

        if tab_type == TabGroupBySortByType.SORTBYTOTALAMOUNT:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_gold_status = True
                self.selected_gold_transaction_code = values[0]
                self.selected_gold_transaction_date = values[1]
                self.selected_gold_unit_price = values[2]
                self.selected_gold_quantity = values[3]
                self.selected_gold_type = values[4]

                self.selected_gold_total_amount = None

                for transaction in transactions:
                    if isinstance(transaction, GoldTransaction):
                        if str(transaction._id) == \
                                str(self.selected_gold_transaction_code):
                            formatted_total_amount = self.format_price_number(
                                transaction._total_amount)
                            self.selected_gold_total_amount = \
                                formatted_total_amount
                            break
            else:
                self.selected_gold_status = False

    def on_currency_treeview_select(self, event, tab_type, transactions):
        if tab_type == TabGroupBySortByType.GROUPBYDATE or \
                tab_type == TabGroupBySortByType.SORTBYDATE:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_currency_status = True
                self.selected_currency_transaction_code = values[0]
                self.selected_currency_quantity = values[1]
                self.selected_currency_type = values[2]
                self.selected_currency_exchange_rate = values[3]
                self.selected_currency_total_amount = values[4]

                self.selected_currency_transaction_date = None

                for transaction in transactions:
                    if isinstance(transaction, CurrencyTransaction):
                        if str(transaction._id) == \
                                str(self.selected_currency_transaction_code):
                            day = transaction._day
                            month = transaction._month
                            year = transaction._year

                            month_name = str(MonthLabel(month))

                            formatted_date = f"{day} {month_name} {year}"

                            self.selected_currency_transaction_date \
                                = formatted_date
                            break

            else:
                self.selected_currency_status = False

        if tab_type == TabGroupBySortByType.GROUPBYCATEGORY:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_currency_status = True
                self.selected_currency_transaction_code = values[0]
                self.selected_currency_transaction_date = values[1]
                self.selected_currency_quantity = values[2]
                self.selected_currency_type = values[3]
                self.selected_currency_exchange_rate = values[4]
                self.selected_currency_total_amount = values[5]
            else:
                self.selected_currency_status = False

        if tab_type == TabGroupBySortByType.SORTBYTOTALAMOUNT:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_currency_status = True
                self.selected_currency_transaction_code = values[0]
                self.selected_currency_transaction_date = values[1]
                self.selected_currency_quantity = values[2]
                self.selected_currency_type = values[3]
                self.selected_currency_exchange_rate = values[4]

                self.selected_currency_total_amount = None

                for transaction in transactions:
                    if isinstance(transaction, CurrencyTransaction):
                        if str(transaction._id) == \
                                str(self.selected_currency_transaction_code):
                            formatted_total_amount = self.format_price_number(
                                transaction._total_amount)
                            self.selected_currency_total_amount = \
                                formatted_total_amount
                            break

            else:
                self.selected_currency_status = False

    def open_view_details_gold_transaction_window(self):
        if self.selected_gold_status:
            if self.view_details_gold_transaction_window is None \
                or not self.view_details_gold_transaction_window \
                    .winfo_exists():
                self.view_details_gold_transaction_window \
                    = ViewDetailsGoldTransactionWindow(
                        self)
                self.view_details_gold_transaction_window.after(
                    10, self.view_details_gold_transaction_window.lift)
            else:
                self.view_details_gold_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a gold transaction to view details.")

    def open_view_details_currency_transaction_window(self):
        if self.selected_currency_status:
            if self.view_details_currency_transaction_window is None \
                or not self.view_details_currency_transaction_window \
                    .winfo_exists():
                self.view_details_currency_transaction_window \
                    = ViewDetailsCurrencyTransactionWindow(
                        self)
                self.view_details_currency_transaction_window.after(
                    10, self.view_details_currency_transaction_window.lift)
            else:
                self.view_details_currency_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a currency transaction to view details.")

    def open_edit_gold_transaction_window(self):
        if self.selected_gold_status:
            if self.edit_gold_transaction_window is None \
                or not self.edit_gold_transaction_window \
                    .winfo_exists():
                self.edit_gold_transaction_window \
                    = EditGoldTransactionWindow(
                        self)
                self.edit_gold_transaction_window.after(
                    10, self.edit_gold_transaction_window.lift)
            else:
                self.edit_gold_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a gold transaction to edit.")

    def open_edit_currency_transaction_window(self):
        if self.selected_currency_status:
            if self.edit_currency_transaction_window is None \
                or not self.edit_currency_transaction_window \
                    .winfo_exists():
                self.edit_currency_transaction_window \
                    = EditCurrencyTransactionWindow(
                        self)
                self.edit_currency_transaction_window.after(
                    10, self.edit_currency_transaction_window.lift)
            else:
                self.edit_currency_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a currency transaction to edit.")

    def open_delete_gold_transaction_window(self):
        if self.selected_gold_status:
            if self.delete_gold_transaction_window is None \
                or not self.delete_gold_transaction_window \
                    .winfo_exists():
                self.delete_gold_transaction_window \
                    = DeleteGoldTransactionWindow(
                        self)
                self.delete_gold_transaction_window.after(
                    10, self.delete_gold_transaction_window.lift)
            else:
                self.delete_gold_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a gold transaction to delete.")

    def open_delete_currency_transaction_window(self):
        if self.selected_currency_status:
            if self.delete_currency_transaction_window is None \
                or not self.delete_currency_transaction_window \
                    .winfo_exists():
                self.delete_currency_transaction_window \
                    = DeleteCurrencyTransactionWindow(
                        self)
                self.delete_currency_transaction_window.after(
                    10, self.delete_currency_transaction_window.lift)
            else:
                self.delete_currency_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a currency transaction to delete.")

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount

    def show_frame(self, frame):
        frame.pack(padx=10, pady=5, fill="x")

    def hide_frame(self, frame):
        frame.pack_forget()


class ViewDetailsGoldTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("View Details Transaction")
        self.iconbitmap(default='./logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        details_frame = customtkinter.CTkFrame(
            master=self, fg_color="#ffffff", border_width=2,
            border_color="#5B5B5B")
        details_frame.pack(padx=20, pady=20, fill="both")

        gold_transaction_label = customtkinter.CTkLabel(
            details_frame, text="GOLD TRANSACTION",
            font=("Arial", 20, "bold")
        )
        gold_transaction_label.pack(padx=20, pady=(20, 0), anchor="w")

        gold_transaction_code = customtkinter.CTkLabel(
            details_frame, text=f"Code: {
                self.parent.selected_gold_transaction_code}"
        )
        gold_transaction_code.pack(padx=20, pady=(0, 5), anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            details_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=20, pady=(0, 10), fill="x")

        gold_unit_price_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        gold_unit_price_frame.pack(padx=20, pady=5, fill="x")

        gold_unit_price_label = customtkinter.CTkLabel(
            gold_unit_price_frame, text="Unit Price (VND/tael):"
        )
        gold_unit_price_label.grid(row=0, column=0, padx=0, pady=0,
                                   sticky="w")

        gold_unit_price_value = customtkinter.CTkLabel(
            gold_unit_price_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_unit_price}"
        )
        gold_unit_price_value.grid(row=0, column=1, padx=0, pady=0,
                                   sticky="e")

        gold_unit_price_frame.columnconfigure(0, weight=0)
        gold_unit_price_frame.columnconfigure(1, weight=1)

        gold_quantity_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        gold_quantity_frame.pack(padx=20, pady=5, fill="x")

        gold_quantity_label = customtkinter.CTkLabel(
            gold_quantity_frame, text="Quantity (tael):"
        )
        gold_quantity_label.grid(row=0, column=0, padx=0, pady=0,
                                 sticky="w")

        gold_quantity_value = customtkinter.CTkLabel(
            gold_quantity_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_quantity}",
        )
        gold_quantity_value.grid(row=0, column=1, padx=0, pady=0,
                                 sticky="e")

        gold_quantity_frame.columnconfigure(0, weight=0)
        gold_quantity_frame.columnconfigure(1, weight=1)

        gold_type_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        gold_type_frame.pack(padx=20, pady=5, fill="x")

        gold_type_label = customtkinter.CTkLabel(
            gold_type_frame, text="Gold Type:"
        )
        gold_type_label.grid(row=0, column=0, padx=0, pady=0,
                             sticky="w")

        gold_type_value = customtkinter.CTkLabel(
            gold_type_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_type}",
        )
        gold_type_value.grid(row=0, column=1, padx=0, pady=0,
                             sticky="e")

        gold_type_frame.columnconfigure(0, weight=0)
        gold_type_frame.columnconfigure(1, weight=1)

        gold_total_amount_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        gold_total_amount_frame.pack(padx=20, pady=5, fill="x")

        gold_total_amount_label = customtkinter.CTkLabel(
            gold_total_amount_frame, text="Total Amount (VND):"
        )
        gold_total_amount_label.grid(row=0, column=0, padx=0, pady=0,
                                     sticky="w")

        gold_total_amount_value = customtkinter.CTkLabel(
            gold_total_amount_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_total_amount}",
        )
        gold_total_amount_value.grid(row=0, column=1, padx=0, pady=0,
                                     sticky="e")

        gold_total_amount_frame.columnconfigure(0, weight=0)
        gold_total_amount_frame.columnconfigure(1, weight=1)

        gold_transaction_date_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        gold_transaction_date_frame.pack(padx=20, pady=5, fill="x")

        gold_transaction_date_label = customtkinter.CTkLabel(
            gold_transaction_date_frame, text="Transaction Date:"
        )
        gold_transaction_date_label.grid(row=0, column=0, padx=0, pady=0,
                                         sticky="w")

        gold_transaction_date_value = customtkinter.CTkLabel(
            gold_transaction_date_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_transaction_date}",
        )
        gold_transaction_date_value.grid(row=0, column=1, padx=0, pady=0,
                                         sticky="e")

        gold_transaction_date_frame.columnconfigure(0, weight=0)
        gold_transaction_date_frame.columnconfigure(1, weight=1)

        btn_close = customtkinter.CTkButton(
            details_frame,
            text="CLOSE",
            fg_color="#d93547",
            hover_color="dark red",
            command=self.destroy
        )
        btn_close.pack(padx=20, pady=(100, 20), anchor="e")


class ViewDetailsCurrencyTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("View Details Transaction")
        self.iconbitmap(default='./logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        details_frame = customtkinter.CTkFrame(
            master=self, fg_color="#ffffff", border_width=2,
            border_color="#5B5B5B")
        details_frame.pack(padx=20, pady=20, fill="both")

        currency_transaction_label = customtkinter.CTkLabel(
            details_frame, text="CURRENCY TRANSACTION",
            font=("Arial", 20, "bold")
        )
        currency_transaction_label.pack(padx=20, pady=(20, 0), anchor="w")

        currency_transaction_code = customtkinter.CTkLabel(
            details_frame, text=f"Code: {
                self.parent.selected_currency_transaction_code}"
        )
        currency_transaction_code.pack(padx=20, pady=(0, 5), anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            details_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=20, pady=(0, 10), fill="x")

        currency_quantity_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        currency_quantity_frame.pack(padx=20, pady=5, fill="x")

        currency_quantity_label = customtkinter.CTkLabel(
            currency_quantity_frame, text="Quantity:"
        )
        currency_quantity_label.grid(row=0, column=0, padx=0, pady=0,
                                     sticky="w")

        currency_quantity_value = customtkinter.CTkLabel(
            currency_quantity_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_currency_quantity}"
        )
        currency_quantity_value.grid(row=0, column=1, padx=0, pady=0,
                                     sticky="e")

        currency_quantity_frame.columnconfigure(0, weight=0)
        currency_quantity_frame.columnconfigure(1, weight=1)

        currency_type_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        currency_type_frame.pack(padx=20, pady=5, fill="x")

        currency_type_label = customtkinter.CTkLabel(
            currency_type_frame, text="Currency Type:"
        )
        currency_type_label.grid(row=0, column=0, padx=0, pady=0,
                                 sticky="w")

        currency_type_value = customtkinter.CTkLabel(
            currency_type_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_currency_type}"
        )
        currency_type_value.grid(row=0, column=1, padx=0, pady=0,
                                 sticky="e")

        currency_type_frame.columnconfigure(0, weight=0)
        currency_type_frame.columnconfigure(1, weight=1)

        currency_exchange_rate_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        currency_exchange_rate_frame.pack(padx=20, pady=5, fill="x")

        currency_exchange_rate_label = customtkinter.CTkLabel(
            currency_exchange_rate_frame, text="Exchange Rate (VND):"
        )
        currency_exchange_rate_label.grid(row=0, column=0, padx=0, pady=0,
                                          sticky="w")

        currency_exchange_rate_value = customtkinter.CTkLabel(
            currency_exchange_rate_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_currency_exchange_rate}"
        )
        currency_exchange_rate_value.grid(row=0, column=1, padx=0, pady=0,
                                          sticky="e")

        currency_exchange_rate_frame.columnconfigure(0, weight=0)
        currency_exchange_rate_frame.columnconfigure(1, weight=1)

        currency_total_amount_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        currency_total_amount_frame.pack(padx=20, pady=5, fill="x")

        currency_total_amount_label = customtkinter.CTkLabel(
            currency_total_amount_frame, text="Total Amount (VND):"
        )
        currency_total_amount_label.grid(row=0, column=0, padx=0, pady=0,
                                         sticky="w")

        currency_total_amount_value = customtkinter.CTkLabel(
            currency_total_amount_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_currency_total_amount}"
        )
        currency_total_amount_value.grid(row=0, column=1, padx=0, pady=0,
                                         sticky="e")

        currency_total_amount_frame.columnconfigure(0, weight=0)
        currency_total_amount_frame.columnconfigure(1, weight=1)

        currency_transaction_date_frame = customtkinter.CTkFrame(
            details_frame, fg_color="transparent")
        currency_transaction_date_frame.pack(padx=20, pady=5, fill="x")

        currency_transaction_date_label = customtkinter.CTkLabel(
            currency_transaction_date_frame, text="Transaction Date:"
        )
        currency_transaction_date_label.grid(row=0, column=0, padx=0, pady=0,
                                             sticky="w")

        currency_transaction_date_value = customtkinter.CTkLabel(
            currency_transaction_date_frame, font=("Arial", 14, "bold"),
            text=f"{
                self.parent.selected_currency_transaction_date}"
        )
        currency_transaction_date_value.grid(row=0, column=1, padx=0, pady=0,
                                             sticky="e")

        currency_transaction_date_frame.columnconfigure(0, weight=0)
        currency_transaction_date_frame.columnconfigure(1, weight=1)

        btn_close = customtkinter.CTkButton(
            details_frame,
            text="CLOSE",
            fg_color="#d93547",
            hover_color="dark red",
            command=self.destroy
        )
        btn_close.pack(padx=20, pady=(100, 20), anchor="e")


class EditGoldTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Edit Transaction")
        self.iconbitmap(default='./logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        edit_frame = customtkinter.CTkFrame(
            master=self, fg_color="#ffffff", border_width=2,
            border_color="#5B5B5B")
        edit_frame.pack(padx=20, pady=20, fill="both")

        gold_transaction_label = customtkinter.CTkLabel(
            edit_frame, text="GOLD TRANSACTION",
            font=("Arial", 20, "bold")
        )
        gold_transaction_label.pack(padx=20, pady=(20, 0), anchor="w")

        gold_transaction_code = customtkinter.CTkLabel(
            edit_frame, text=f"Code: {
                self.parent.selected_gold_transaction_code}"
        )
        gold_transaction_code.pack(padx=20, pady=(0, 5), anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            edit_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=20, pady=(0, 10), fill="x")

        label_unit_price = customtkinter.CTkLabel(
            master=edit_frame,
            text="Unit Price (VND/tael):",
            font=("Arial", 14),
            text_color="black",
        )
        label_unit_price.pack(padx=20, pady=5, anchor="w")

        default_value_gold_unit_price = \
            tkinter.StringVar(value=self.parent.selected_gold_unit_price)
        self.gold_entry_unit_price = customtkinter.CTkEntry(
            master=edit_frame, placeholder_text="Ex: 85,200,000.7",
            textvariable=default_value_gold_unit_price)
        self.gold_entry_unit_price.pack(padx=20, pady=0, anchor="w", fill="x")

        label_quantity = customtkinter.CTkLabel(
            master=edit_frame,
            text="Quantity (tael):",
            font=("Arial", 14),
            text_color="black",
        )
        label_quantity.pack(padx=20, pady=5, anchor="w")

        default_value_gold_quantity = \
            tkinter.StringVar(value=self.parent.selected_gold_quantity)
        self.gold_entry_quantity = customtkinter.CTkEntry(
            master=edit_frame, placeholder_text="Ex: 10",
            textvariable=default_value_gold_quantity)
        self.gold_entry_quantity.pack(padx=20, pady=0, anchor="w", fill="x")

        label_gold_type = customtkinter.CTkLabel(
            master=edit_frame,
            text="Gold Type:",
            font=("Arial", 14),
            text_color="black",
        )
        label_gold_type.pack(padx=20, pady=5, anchor="w")

        self.gold_combobox_gold_type = \
            customtkinter.CTkComboBox(edit_frame,
                                      values=[
                                          "SJC", "PNJ", "DOJI"
                                      ])
        self.gold_combobox_gold_type.set(str(self.parent.selected_gold_type))
        self.gold_combobox_gold_type.pack(
            padx=20, pady=0, anchor="w", fill="x")

        label_transaction_date = customtkinter.CTkLabel(
            master=edit_frame,
            text="Transaction Date:",
            font=("Arial", 14),
            text_color="black",
        )
        label_transaction_date.pack(padx=20, pady=5, anchor="w")

        date_frame = customtkinter.CTkFrame(
            master=edit_frame,
            fg_color="transparent"
        )
        date_frame.pack(padx=20, pady=(0, 5), anchor="w", fill="x")

        date_str = str(self.parent.selected_gold_transaction_date)

        date_obj = datetime.datetime.strptime(date_str, "%d %B %Y")

        day_obj = date_obj.day
        month_obj = date_obj.month
        year_obj = date_obj.year

        default_value_gold_day = \
            tkinter.StringVar(value=int(day_obj))
        self.gold_entry_day = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Day", width=95,
            textvariable=default_value_gold_day)
        self.gold_entry_day.grid(
            row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        separator_day_month = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_day_month.grid(row=0, column=1,
                                 padx=3, pady=0, sticky="ew")

        default_value_gold_month = \
            tkinter.StringVar(value=int(month_obj))
        self.gold_entry_month = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Month", width=95,
            textvariable=default_value_gold_month)
        self.gold_entry_month.grid(row=0, column=2, padx=5, pady=0)

        separator_month_year = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_month_year.grid(
            row=0, column=3, padx=3, pady=0, sticky="ew")

        default_value_gold_year = \
            tkinter.StringVar(value=int(year_obj))
        self.gold_entry_year = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Year", width=95,
            textvariable=default_value_gold_year)
        self.gold_entry_year.grid(row=0, column=4, padx=(5, 0), pady=0)

        buttons_frame = customtkinter.CTkFrame(
            edit_frame, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=(50, 5), anchor="w", fill="x")

        button_confirm = customtkinter.CTkButton(
            buttons_frame,
            text="CONFIRM",
            width=150,
            command=self.gold_confirm_button_callback)
        button_confirm.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)

        button_cancel = customtkinter.CTkButton(
            buttons_frame,
            text="CANCEL",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.destroy)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

    def gold_confirm_button_callback(self):
        unit_price = self.gold_entry_unit_price.get()
        quantity = self.gold_entry_quantity.get()
        day_submit = self.gold_entry_day.get()
        month_submit = self.gold_entry_month.get()
        year_submit = self.gold_entry_year.get()
        gold_type = self.gold_combobox_gold_type.get()

        if not all([unit_price, quantity, day_submit, month_submit,
                    year_submit, gold_type]):
            messagebox.showerror(
                "Missing Input", "Please fill in all fields.")
            self.focus()
            return

        unit_price = self.validate_and_convert_input(unit_price)
        if unit_price is None:
            messagebox.showerror(
                "Invalid Unit Price", "Unit Price must be a valid number.")
            self.focus()
            return

        quantity = self.validate_and_convert_input(quantity)
        if quantity is None:
            messagebox.showerror(
                "Invalid Quantity", "Quantity must be a valid number.")
            self.focus()
            return

        if not all(map(str.isdigit, [day_submit, month_submit, year_submit])):
            messagebox.showerror(
                "Invalid Input", "Please enter valid numerical \
                \nvalues for date fields.")
            self.after(10, self.lift)
            return

        day = int(day_submit)
        month = int(month_submit)
        year = int(year_submit)

        if not self.validate_date(day, month, year):
            messagebox.showerror("Invalid Date", "Date is not valid.")
            self.focus()
            return

        if gold_type not in ["SJC", "PNJ", "DOJI"]:
            messagebox.showerror("Invalid Gold Type",
                                 "Gold Type must be 'SJC', 'PNJ', or 'DOJI'.")
            self.focus()
            return

        data_file = "data.json"
        if os.path.exists(data_file):
            with open(data_file, "r") as file:
                data = json.load(file)
        else:
            data = {"transactions": []}

        transaction_found = False
        for transaction in data["transactions"]:
            if transaction["id"] == self.parent.selected_gold_transaction_code:
                transaction["day"] = day
                transaction["month"] = month
                transaction["year"] = year
                transaction["unit_price"] = unit_price
                transaction["quantity"] = quantity
                transaction["gold_type"] = \
                    GoldType[self.gold_combobox_gold_type.get()].value
                transaction_found = True
                break

        if not transaction_found:
            messagebox.showerror("Error", "Transaction ID not found.")
            return

        with open(data_file, "w") as file:
            json.dump(data, file, indent=4)

        messagebox \
            .showinfo("Success", "Gold transaction updated successfully! \
                            \nPlease Refresh Data!")
        self.destroy()

    def validate_and_convert_input(self, input_str):
        try:
            input_str = input_str.replace(",", "")
            return float(input_str)
        except ValueError:
            return None

    def validate_date(self, day, month, year):
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            return False

        if month < 1 or month > 12:
            return False

        if day < 1 or day > 31:
            return False

        if year < 1500:
            return False

        try:
            datetime.datetime(year, month, day)
        except ValueError:
            return False

        return True

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount


class EditCurrencyTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Edit Transaction")
        self.iconbitmap(default='./logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent

        with open('data.json', 'r') as json_file:
            data = json.load(json_file)

        self.exchange_rates = data['exchange_rates']

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        edit_frame = customtkinter.CTkFrame(
            master=self, fg_color="#ffffff", border_width=2,
            border_color="#5B5B5B")
        edit_frame.pack(padx=20, pady=20, fill="both")

        currency_transaction_label = customtkinter.CTkLabel(
            edit_frame, text="CURRENCY TRANSACTION",
            font=("Arial", 20, "bold")
        )
        currency_transaction_label.pack(padx=20, pady=(20, 0), anchor="w")

        currency_transaction_code = customtkinter.CTkLabel(
            edit_frame, text=f"Code: {
                self.parent.selected_currency_transaction_code}"
        )
        currency_transaction_code.pack(padx=20, pady=(0, 5), anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            edit_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=20, pady=(0, 10), fill="x")

        label_quantity = customtkinter.CTkLabel(
            master=edit_frame,
            text="Quantity:",
            font=("Arial", 14),
            text_color="black",
        )
        label_quantity.pack(padx=20, pady=5, anchor="w")

        default_value_currency_quantity = \
            tkinter.StringVar(value=self.parent.selected_currency_quantity)
        self.currency_entry_quantity = customtkinter.CTkEntry(
            master=edit_frame, placeholder_text="Ex: 50",
            textvariable=default_value_currency_quantity)
        self.currency_entry_quantity.pack(
            padx=20, pady=0, anchor="w", fill="x")

        label_currency_type = customtkinter.CTkLabel(
            master=edit_frame,
            text="Currency Type:",
            font=("Arial", 14),
            text_color="black",
        )
        label_currency_type.pack(padx=20, pady=5, anchor="w")

        self.currency_combobox_currency_type = \
            customtkinter.CTkComboBox(edit_frame,
                                      values=[
                                          "VND", "USD", "EUR"
                                      ],
                                      command=self.
                                      combobox_currency_type_callback)
        self.currency_combobox_currency_type.set(
            str(self.parent.selected_currency_type))
        self.currency_combobox_currency_type.pack(
            padx=20, pady=0, anchor="w", fill="x")

        label_exchange_rate = customtkinter.CTkLabel(
            master=edit_frame,
            text="Exchange Rate (VND):",
            font=("Arial", 14),
            text_color="black",
        )
        label_exchange_rate.pack(padx=20, pady=5, anchor="w")

        self.currency_entry_exchange_rate = customtkinter.CTkEntry(
            master=edit_frame, placeholder_text="23,130.6")
        self.currency_entry_exchange_rate.pack(padx=20, pady=0, anchor="w",
                                               fill="x")
        self.currency_entry_exchange_rate.insert(
            0, str(self.parent.selected_currency_exchange_rate))
        self.currency_entry_exchange_rate.configure(state="readonly")

        label_transaction_date = customtkinter.CTkLabel(
            master=edit_frame,
            text="Transaction Date:",
            font=("Arial", 14),
            text_color="black",
        )
        label_transaction_date.pack(padx=20, pady=5, anchor="w")

        date_frame = customtkinter.CTkFrame(
            master=edit_frame,
            fg_color="transparent"
        )
        date_frame.pack(padx=20, pady=(0, 5), anchor="w", fill="x")

        date_str = str(self.parent.selected_currency_transaction_date)

        date_obj = datetime.datetime.strptime(date_str, "%d %B %Y")

        day_obj = date_obj.day
        month_obj = date_obj.month
        year_obj = date_obj.year

        default_value_currency_day = \
            tkinter.StringVar(value=int(day_obj))
        self.currency_entry_day = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Day", width=95,
            textvariable=default_value_currency_day)
        self.currency_entry_day.grid(row=0, column=0, padx=(0, 5), pady=0,
                                     sticky="ew")

        separator_day_month = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_day_month.grid(row=0, column=1,
                                 padx=3, pady=0, sticky="ew")

        default_value_currency_month = \
            tkinter.StringVar(value=int(month_obj))
        self.currency_entry_month = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Month", width=95,
            textvariable=default_value_currency_month)
        self.currency_entry_month.grid(row=0, column=2, padx=5, pady=0)

        separator_month_year = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_month_year.grid(
            row=0, column=3, padx=3, pady=0, sticky="ew")

        default_value_currency_year = \
            tkinter.StringVar(value=int(year_obj))
        self.currency_entry_year = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Year", width=95,
            textvariable=default_value_currency_year)
        self.currency_entry_year.grid(row=0, column=4, padx=(5, 0), pady=0)

        buttons_frame = customtkinter.CTkFrame(edit_frame,
                                               fg_color="transparent")
        buttons_frame.pack(padx=20, pady=(50, 5), anchor="w", fill="x")

        button_confirm = customtkinter.CTkButton(
            buttons_frame,
            text="CONFIRM",
            width=150,
            command=self.currency_confirm_button_callback)
        button_confirm.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)

        button_cancel = customtkinter.CTkButton(
            buttons_frame,
            text="CANCEL",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.destroy)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

    def combobox_currency_type_callback(self, choice):
        try:
            currency_type = CurrencyType[choice].value
        except KeyError:
            return

        exchange_rate = self.get_exchange_rate(currency_type)
        self.currency_entry_exchange_rate.configure(state="normal")
        self.currency_entry_exchange_rate.delete(0, "end")
        self.currency_entry_exchange_rate.insert(0, str(exchange_rate))
        self.currency_entry_exchange_rate.configure(state="readonly")

    def get_exchange_rate(self, currency_type):
        for rate in self.exchange_rates:
            if rate['currency_type'] == currency_type:
                return self.format_price_number(rate['rate'])

        return self.format_price_number(0.0)

    def currency_confirm_button_callback(self):
        quantity = self.currency_entry_quantity.get()
        exchange_rate = self.currency_entry_exchange_rate.get()
        day_submit = self.currency_entry_day.get()
        month_submit = self.currency_entry_month.get()
        year_submit = self.currency_entry_year.get()
        currency_type = self.currency_combobox_currency_type.get()

        if not all([quantity, exchange_rate, day_submit, month_submit,
                    year_submit, currency_type]):
            messagebox.showerror(
                "Missing Input", "Please fill in all fields.")
            self.focus()
            return

        quantity = self.validate_and_convert_input(quantity)
        if quantity is None:
            messagebox.showerror(
                "Invalid Quantity", "Quantity must be a valid number.")
            self.focus()
            return

        exchange_rate = self.validate_and_convert_input(exchange_rate)
        if exchange_rate is None:
            messagebox.showerror(
                "Invalid Exchange Rate",
                "Exchange Rate must be a valid number.")
            self.focus()
            return

        if not all(map(str.isdigit, [day_submit, month_submit, year_submit])):
            messagebox.showerror(
                "Invalid Input", "Please enter valid numerical \
                \nvalues for date fields.")
            self.after(10, self.lift)
            return

        day = int(day_submit)
        month = int(month_submit)
        year = int(year_submit)

        if not self.validate_date(day, month, year):
            messagebox.showerror("Invalid Date", "Date is not valid.")
            self.focus()
            return

        if currency_type not in ["VND", "USD", "EUR"]:
            messagebox. \
                showerror("Invalid Currency Type",
                          "Currency Type must be 'VND', 'USD', or 'EUR'.")
            self.focus()
            return

        data_file = "data.json"
        if os.path.exists(data_file):
            with open(data_file, "r") as file:
                data = json.load(file)
        else:
            data = {"transactions": []}

        exchange_rates = data["exchange_rates"]

        exchange_rate = None
        for rate in exchange_rates:
            if rate["currency_type"] == CurrencyType[currency_type].value:
                exchange_rate = rate
                break

        if exchange_rate is None:
            messagebox.showerror("Exchange Rate Not Found",
                                 f"No exchange rate found for currency type \
                                {currency_type}.")
            self.focus()
            return

        transaction_found = False
        for transaction in data["transactions"]:
            if transaction["id"] == \
                    self.parent.selected_currency_transaction_code:
                transaction["day"] = day
                transaction["month"] = month
                transaction["year"] = year
                transaction["quantity"] = quantity
                transaction["exchange_rate"] = exchange_rate
                transaction["currency_type"] = \
                    CurrencyType[currency_type].value
                transaction_found = True
                break

        if not transaction_found:
            messagebox.showerror("Error", "Transaction ID not found.")
            return

        with open(data_file, "w") as file:
            json.dump(data, file, indent=4)

        messagebox \
            .showinfo("Success", "Currency transaction updated successfully! \
                            \nPlease Refresh Data!")
        self.destroy()

    def validate_and_convert_input(self, input_str):
        try:
            input_str = input_str.replace(",", "")
            return float(input_str)
        except ValueError:
            return None

    def validate_date(self, day, month, year):
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            return False

        if month < 1 or month > 12:
            return False

        if day < 1 or day > 31:
            return False

        if year < 1500:
            return False

        try:
            datetime.datetime(year, month, day)
        except ValueError:
            return False

        return True

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount


class DeleteGoldTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("View Details Transaction")
        self.iconbitmap(default='./logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        delete_frame = customtkinter.CTkFrame(
            master=self, fg_color="#ffffff", border_width=2,
            border_color="#5B5B5B")
        delete_frame.pack(padx=20, pady=20, fill="both")

        gold_transaction_label = customtkinter.CTkLabel(
            delete_frame, text="GOLD TRANSACTION",
            font=("Arial", 20, "bold")
        )
        gold_transaction_label.pack(padx=20, pady=(20, 0), anchor="w")

        gold_transaction_code = customtkinter.CTkLabel(
            delete_frame, text=f"Code: {
                self.parent.selected_gold_transaction_code}"
        )
        gold_transaction_code.pack(padx=20, pady=(0, 5), anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            delete_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=20, pady=(0, 10), fill="x")

        gold_unit_price_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        gold_unit_price_frame.pack(padx=20, pady=5, fill="x")

        gold_unit_price_label = customtkinter.CTkLabel(
            gold_unit_price_frame, text="Unit Price (VND/tael):"
        )
        gold_unit_price_label.grid(row=0, column=0, padx=0, pady=0,
                                   sticky="w")

        gold_unit_price_value = customtkinter.CTkLabel(
            gold_unit_price_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_unit_price}"
        )
        gold_unit_price_value.grid(row=0, column=1, padx=0, pady=0,
                                   sticky="e")

        gold_unit_price_frame.columnconfigure(0, weight=0)
        gold_unit_price_frame.columnconfigure(1, weight=1)

        gold_quantity_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        gold_quantity_frame.pack(padx=20, pady=5, fill="x")

        gold_quantity_label = customtkinter.CTkLabel(
            gold_quantity_frame, text="Quantity (tael):"
        )
        gold_quantity_label.grid(row=0, column=0, padx=0, pady=0,
                                 sticky="w")

        gold_quantity_value = customtkinter.CTkLabel(
            gold_quantity_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_quantity}",
        )
        gold_quantity_value.grid(row=0, column=1, padx=0, pady=0,
                                 sticky="e")

        gold_quantity_frame.columnconfigure(0, weight=0)
        gold_quantity_frame.columnconfigure(1, weight=1)

        gold_type_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        gold_type_frame.pack(padx=20, pady=5, fill="x")

        gold_type_label = customtkinter.CTkLabel(
            gold_type_frame, text="Gold Type:"
        )
        gold_type_label.grid(row=0, column=0, padx=0, pady=0,
                             sticky="w")

        gold_type_value = customtkinter.CTkLabel(
            gold_type_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_type}",
        )
        gold_type_value.grid(row=0, column=1, padx=0, pady=0,
                             sticky="e")

        gold_type_frame.columnconfigure(0, weight=0)
        gold_type_frame.columnconfigure(1, weight=1)

        gold_total_amount_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        gold_total_amount_frame.pack(padx=20, pady=5, fill="x")

        gold_total_amount_label = customtkinter.CTkLabel(
            gold_total_amount_frame, text="Total Amount (VND):"
        )
        gold_total_amount_label.grid(row=0, column=0, padx=0, pady=0,
                                     sticky="w")

        gold_total_amount_value = customtkinter.CTkLabel(
            gold_total_amount_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_total_amount}",
        )
        gold_total_amount_value.grid(row=0, column=1, padx=0, pady=0,
                                     sticky="e")

        gold_total_amount_frame.columnconfigure(0, weight=0)
        gold_total_amount_frame.columnconfigure(1, weight=1)

        gold_transaction_date_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        gold_transaction_date_frame.pack(padx=20, pady=5, fill="x")

        gold_transaction_date_label = customtkinter.CTkLabel(
            gold_transaction_date_frame, text="Transaction Date:"
        )
        gold_transaction_date_label.grid(row=0, column=0, padx=0, pady=0,
                                         sticky="w")

        gold_transaction_date_value = customtkinter.CTkLabel(
            gold_transaction_date_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_gold_transaction_date}",
        )
        gold_transaction_date_value.grid(row=0, column=1, padx=0, pady=0,
                                         sticky="e")

        gold_transaction_date_frame.columnconfigure(0, weight=0)
        gold_transaction_date_frame.columnconfigure(1, weight=1)

        buttons_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=(100, 5), anchor="w", fill="x")

        button_confirm = customtkinter.CTkButton(
            buttons_frame,
            text="CONFIRM",
            width=150,
            command=self.gold_confirm_button_callback)
        button_confirm.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)

        button_cancel = customtkinter.CTkButton(
            buttons_frame,
            text="CANCEL",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.destroy)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

    def gold_confirm_button_callback(self):
        data_file = "data.json"
        if os.path.exists(data_file):
            with open(data_file, "r") as file:
                data = json.load(file)
        else:
            data = {"transactions": []}

        transaction_found = False
        for transaction in data["transactions"]:
            if transaction["id"] == self.parent.selected_gold_transaction_code:
                transaction["isdeleted"] = True
                transaction_found = True
                break

        if not transaction_found:
            messagebox.showerror("Error", "Transaction ID not found.")
            return

        with open(data_file, "w") as file:
            json.dump(data, file, indent=4)

        messagebox \
            .showinfo("Success", "Gold transaction deleted successfully! \
                            \nPlease Refresh Data!")
        self.destroy()


class DeleteCurrencyTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("View Details Transaction")
        self.iconbitmap(default='./logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        delete_frame = customtkinter.CTkFrame(
            master=self, fg_color="#ffffff", border_width=2,
            border_color="#5B5B5B")
        delete_frame.pack(padx=20, pady=20, fill="both")

        currency_transaction_label = customtkinter.CTkLabel(
            delete_frame, text="CURRENCY TRANSACTION",
            font=("Arial", 20, "bold")
        )
        currency_transaction_label.pack(padx=20, pady=(20, 0), anchor="w")

        currency_transaction_code = customtkinter.CTkLabel(
            delete_frame, text=f"Code: {
                self.parent.selected_currency_transaction_code}"
        )
        currency_transaction_code.pack(padx=20, pady=(0, 5), anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            delete_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=20, pady=(0, 10), fill="x")

        currency_quantity_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        currency_quantity_frame.pack(padx=20, pady=5, fill="x")

        currency_quantity_label = customtkinter.CTkLabel(
            currency_quantity_frame, text="Quantity:"
        )
        currency_quantity_label.grid(row=0, column=0, padx=0, pady=0,
                                     sticky="w")

        currency_quantity_value = customtkinter.CTkLabel(
            currency_quantity_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_currency_quantity}"
        )
        currency_quantity_value.grid(row=0, column=1, padx=0, pady=0,
                                     sticky="e")

        currency_quantity_frame.columnconfigure(0, weight=0)
        currency_quantity_frame.columnconfigure(1, weight=1)

        currency_type_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        currency_type_frame.pack(padx=20, pady=5, fill="x")

        currency_type_label = customtkinter.CTkLabel(
            currency_type_frame, text="Currency Type:"
        )
        currency_type_label.grid(row=0, column=0, padx=0, pady=0,
                                 sticky="w")

        currency_type_value = customtkinter.CTkLabel(
            currency_type_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_currency_type}"
        )
        currency_type_value.grid(row=0, column=1, padx=0, pady=0,
                                 sticky="e")

        currency_type_frame.columnconfigure(0, weight=0)
        currency_type_frame.columnconfigure(1, weight=1)

        currency_exchange_rate_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        currency_exchange_rate_frame.pack(padx=20, pady=5, fill="x")

        currency_exchange_rate_label = customtkinter.CTkLabel(
            currency_exchange_rate_frame, text="Exchange Rate (VND):"
        )
        currency_exchange_rate_label.grid(row=0, column=0, padx=0, pady=0,
                                          sticky="w")

        currency_exchange_rate_value = customtkinter.CTkLabel(
            currency_exchange_rate_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_currency_exchange_rate}"
        )
        currency_exchange_rate_value.grid(row=0, column=1, padx=0, pady=0,
                                          sticky="e")

        currency_exchange_rate_frame.columnconfigure(0, weight=0)
        currency_exchange_rate_frame.columnconfigure(1, weight=1)

        currency_total_amount_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        currency_total_amount_frame.pack(padx=20, pady=5, fill="x")

        currency_total_amount_label = customtkinter.CTkLabel(
            currency_total_amount_frame, text="Total Amount (VND):"
        )
        currency_total_amount_label.grid(row=0, column=0, padx=0, pady=0,
                                         sticky="w")

        currency_total_amount_value = customtkinter.CTkLabel(
            currency_total_amount_frame, font=("Arial", 14, "bold"), text=f"{
                self.parent.selected_currency_total_amount}"
        )
        currency_total_amount_value.grid(row=0, column=1, padx=0, pady=0,
                                         sticky="e")

        currency_total_amount_frame.columnconfigure(0, weight=0)
        currency_total_amount_frame.columnconfigure(1, weight=1)

        currency_transaction_date_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        currency_transaction_date_frame.pack(padx=20, pady=5, fill="x")

        currency_transaction_date_label = customtkinter.CTkLabel(
            currency_transaction_date_frame, text="Transaction Date:"
        )
        currency_transaction_date_label.grid(row=0, column=0, padx=0, pady=0,
                                             sticky="w")

        currency_transaction_date_value = customtkinter.CTkLabel(
            currency_transaction_date_frame, font=("Arial", 14, "bold"),
            text=f"{
                self.parent.selected_currency_transaction_date}"
        )
        currency_transaction_date_value.grid(row=0, column=1, padx=0, pady=0,
                                             sticky="e")

        currency_transaction_date_frame.columnconfigure(0, weight=0)
        currency_transaction_date_frame.columnconfigure(1, weight=1)

        buttons_frame = customtkinter.CTkFrame(delete_frame,
                                               fg_color="transparent")
        buttons_frame.pack(padx=20, pady=(100, 5), anchor="w", fill="x")

        button_confirm = customtkinter.CTkButton(
            buttons_frame,
            text="CONFIRM",
            width=150,
            command=self.currency_confirm_button_callback)
        button_confirm.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)

        button_cancel = customtkinter.CTkButton(
            buttons_frame,
            text="CANCEL",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.destroy)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

    def currency_confirm_button_callback(self):
        data_file = "data.json"
        if os.path.exists(data_file):
            with open(data_file, "r") as file:
                data = json.load(file)
        else:
            data = {"transactions": []}

        transaction_found = False
        for transaction in data["transactions"]:
            if transaction["id"] == \
                    self.parent.selected_currency_transaction_code:
                transaction["isdeleted"] = True
                transaction_found = True
                break

        if not transaction_found:
            messagebox.showerror("Error", "Transaction ID not found.")
            return

        with open(data_file, "w") as file:
            json.dump(data, file, indent=4)

        messagebox \
            .showinfo("Success", "Currency transaction deleted successfully! \
                            \nPlease Refresh Data!")
        self.destroy()


class FilterWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Transaction Management - FILTER")
        self.iconbitmap(default='./logo.ico')
        self.minsize(1720, 960)
        self.configure(fg_color="white")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

        self.transactions = \
            self.master.master.transaction_list.get_transactions()

    def create_widget(self):
        self.header_frame_for_filter_window = HeaderFrameForWindow(
            master=self, label_header="FILTER",
            submit_event=lambda: self.submit_event(self.transactions),
            show_submit=True)
        self.header_frame_for_filter_window.pack(padx=10, pady=10, fill="x")

        self.create_selector_frames()

        self.create_filter_result_frame()

    def create_selector_frames(self):
        selector_frame = customtkinter.CTkFrame(
            master=self, fg_color="transparent")
        selector_frame.pack(side="top", fill="x")

        self.create_time_range_selector_frame(selector_frame)
        self.create_total_amount_selector_frame(selector_frame)

    def create_time_range_selector_frame(self, frame):
        time_range_selector_frame = customtkinter.CTkFrame(
            master=frame,
            fg_color="#dbdbdb", bg_color="#ffffff"
        )
        time_range_selector_frame.grid(row=0, column=0, padx=10, pady=5)

        current_date = datetime.datetime.now()
        next_month_date = current_date + timedelta(days=30)

        label_title = customtkinter.CTkLabel(
            master=time_range_selector_frame,
            text="Select time range",
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="w"
        )
        label_title.pack(padx=20, pady=(10, 5), anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=5)

        from_frame = customtkinter.CTkFrame(
            master=time_range_selector_frame,
            fg_color="transparent"
        )
        from_frame.pack(padx=20, pady=(5, 0), anchor="w")

        from_title = customtkinter.CTkLabel(
            master=from_frame,
            text="From:",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        from_title.grid(row=0, column=0, padx=10, pady=5)

        self.from_frame_entry_day = customtkinter.CTkEntry(
            master=from_frame, placeholder_text="Day", width=60)
        self.from_frame_entry_day.grid(row=0, column=1, padx=10, pady=5)

        separator_day_month_from_frame = ttk.Separator(
            from_frame, orient="horizontal", style="Separator.TSeparator")
        separator_day_month_from_frame.grid(row=0, column=2,
                                            padx=0, pady=5, sticky="ew")

        self.from_frame_entry_month = customtkinter.CTkEntry(
            master=from_frame, placeholder_text="Month", width=60)
        self.from_frame_entry_month.grid(row=0, column=3, padx=10, pady=5)

        separator_month_year_from_frame = ttk.Separator(
            from_frame, orient="horizontal", style="Separator.TSeparator")
        separator_month_year_from_frame.grid(
            row=0, column=4, padx=0, pady=5, sticky="ew")

        self.from_frame_entry_year = customtkinter.CTkEntry(
            master=from_frame, placeholder_text="Year", width=60)
        self.from_frame_entry_year.grid(row=0, column=5, padx=10, pady=5)

        self.from_frame_entry_day.insert(0, str(current_date.day))
        self.from_frame_entry_month.insert(0, str(current_date.month))
        self.from_frame_entry_year.insert(0, str(current_date.year))

        to_frame = customtkinter.CTkFrame(
            master=time_range_selector_frame,
            fg_color="transparent"
        )
        to_frame.pack(padx=20, pady=(0, 10), anchor="w")

        to_title = customtkinter.CTkLabel(
            master=to_frame,
            text="To:    ",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        to_title.grid(row=0, column=0, padx=10, pady=5)

        self.to_frame_entry_day = customtkinter.CTkEntry(
            master=to_frame, placeholder_text="Day", width=60)
        self.to_frame_entry_day.grid(row=0, column=1, padx=10, pady=5)

        separator_day_month_to_frame = ttk.Separator(
            to_frame, orient="horizontal", style="Separator.TSeparator")
        separator_day_month_to_frame.grid(row=0, column=2,
                                          padx=0, pady=5, sticky="ew")

        self.to_frame_entry_month = customtkinter.CTkEntry(
            master=to_frame, placeholder_text="Month", width=60)
        self.to_frame_entry_month.grid(row=0, column=3, padx=10, pady=5)

        separator_month_year_to_frame = ttk.Separator(
            to_frame, orient="horizontal", style="Separator.TSeparator")
        separator_month_year_to_frame.grid(
            row=0, column=4, padx=0, pady=5, sticky="ew")

        self.to_frame_entry_year = customtkinter.CTkEntry(
            master=to_frame, placeholder_text="Year", width=60)
        self.to_frame_entry_year.grid(row=0, column=5, padx=10, pady=5)

        self.to_frame_entry_day.insert(0, str(next_month_date.day))
        self.to_frame_entry_month.insert(0, str(next_month_date.month))
        self.to_frame_entry_year.insert(0, str(next_month_date.year))

    def create_total_amount_selector_frame(self, frame):
        total_amount_selector_frame = customtkinter.CTkFrame(
            master=frame,
            fg_color="#dbdbdb", bg_color="#ffffff"
        )
        total_amount_selector_frame.grid(row=0, column=1, padx=10, pady=5)

        label_title = customtkinter.CTkLabel(
            master=total_amount_selector_frame,
            text="Select filter by Total Amount",
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="w"
        )
        label_title.pack(padx=20, pady=(10, 5), anchor="w")

        label_chose_range = customtkinter.CTkLabel(
            master=total_amount_selector_frame,
            text="Chose range (VND):",
            font=("Arial", 14),
            text_color="black",
            anchor="w"
        )
        label_chose_range.pack(padx=20, pady=5, anchor="w")

        self.create_optionmenu_chose_range(total_amount_selector_frame)

    def create_optionmenu_chose_range(self, frame):
        self.optionmenu = customtkinter.CTkOptionMenu(
            frame,
            values=["All", "< 100M", "100M - 500M", "500M - 1B", "> 1B"]
        )
        self.optionmenu.set("All")
        self.optionmenu.pack(padx=30, pady=(5, 20), side="left")

    def create_filter_result_frame(self):
        self.result_frame = customtkinter.CTkScrollableFrame(
            self, fg_color="#dbdbdb", bg_color="#ffffff",
            height=700)
        self.result_frame.pack(padx=10, pady=10, fill="x")

    def submit_event(self, transactions):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        from_day_str = self.from_frame_entry_day.get()
        from_month_str = self.from_frame_entry_month.get()
        from_year_str = self.from_frame_entry_year.get()
        to_day_str = self.to_frame_entry_day.get()
        to_month_str = self.to_frame_entry_month.get()
        to_year_str = self.to_frame_entry_year.get()
        chose_range = self.optionmenu.get()

        if not all([from_day_str, from_month_str, from_year_str, to_day_str,
                    to_month_str, to_year_str]):
            messagebox.showerror(
                "Missing Input", "Please fill in all date fields.")
            self.after(10, self.lift)
            return

        if not all(map(str.isdigit, [from_day_str, from_month_str,
                                     from_year_str, to_day_str, to_month_str,
                                     to_year_str])):
            messagebox.showerror(
                "Invalid Input", "Please enter valid numerical \
                \nvalues for date fields.")
            self.after(10, self.lift)
            return

        from_day = int(from_day_str)
        from_month = int(from_month_str)
        from_year = int(from_year_str)
        to_day = int(to_day_str)
        to_month = int(to_month_str)
        to_year = int(to_year_str)

        if not self.validate_date(from_day, from_month, from_year) or not \
                self.validate_date(to_day, to_month, to_year):
            messagebox.showerror("Invalid Date", "Date is not valid.")
            self.after(10, self.lift)
            return

        transactions_filter = self.filter_transactions_by_date(
            from_day, from_month, from_year, to_day, to_month, to_year,
            transactions)

        transactions_filter = self.filter_transactions_by_amount(
            transactions_filter, chose_range)

        self.create_content_treeview_filter_result(
            self.result_frame, transactions_filter)

    def validate_date(self, day, month, year):
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            return False

        if month < 1 or month > 12:
            return False

        if day < 1 or day > 31:
            return False

        if year < 1500:
            return False

        try:
            datetime.datetime(year, month, day)
        except ValueError:
            return False

        return True

    def filter_transactions_by_date(self, from_day, from_month, from_year,
                                    to_day, to_month, to_year, transactions):
        from_date = datetime.date(from_year, from_month, from_day)
        to_date = datetime.date(to_year, to_month, to_day)

        transactions_filter = []

        for transaction in transactions:
            transaction_date = datetime.date(
                transaction._year, transaction._month, transaction._day)
            if from_date <= transaction_date <= to_date:
                transactions_filter.append(transaction)

        return transactions_filter

    def filter_transactions_by_amount(self, transactions, chose_range):
        transactions_filter = []

        for transaction in transactions:
            total_amount = transaction._total_amount

            if chose_range == "All":
                transactions_filter.append(transaction)
            elif chose_range == "< 100M" and total_amount < 100000000:
                transactions_filter.append(transaction)
            elif chose_range == "100M - 500M" and 100000000 <= \
                    total_amount < 500000000:
                transactions_filter.append(transaction)
            elif chose_range == "500M - 1B" and 500000000 <= \
                    total_amount < 1000000000:
                transactions_filter.append(transaction)
            elif chose_range == "> 1B" and total_amount >= 1000000000:
                transactions_filter.append(transaction)

        return transactions_filter

    def create_content_treeview_filter_result(self, frame, transactions):
        gold_transactions = [transaction for transaction in transactions
                             if isinstance(
                                 transaction, GoldTransaction)]
        currency_transactions = [transaction for transaction in transactions
                                 if isinstance(
                                     transaction, CurrencyTransaction)]

        frame_gold = customtkinter.CTkFrame(
            frame, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")
        frame_gold.pack(padx=5, pady=5, fill="x")

        treeview_gold_transaction = self.create_gold_treeview_filter_result(
            frame_gold, gold_transactions)
        self.populate_treeview_with_gold_filter_result(
            treeview_gold_transaction, gold_transactions)
        treeview_gold_transaction.pack(padx=20, pady=(10, 20), fill="x")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=10, pady=10, fill="x")

        frame_currency = customtkinter.CTkFrame(
            frame, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")
        frame_currency.pack(padx=5, pady=5, fill="x")

        treeview_currency_transaction\
            = self.create_currency_treeview_filter_result(
                frame_currency, currency_transactions)
        self.populate_treeview_with_currency_filter_result(
            treeview_currency_transaction, currency_transactions)
        treeview_currency_transaction.pack(padx=20, pady=(10, 20), fill="x")

    def create_header_transaction_treeview(self, frame, total_amount, label):
        frame_header = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_header.pack(padx=5, pady=5, fill="x")

        frame_label = customtkinter.CTkFrame(
            frame_header, fg_color="transparent")
        frame_label.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=5)

        gold_transaction_label = customtkinter.CTkLabel(
            frame_label, text=label, text_color="black",
            font=("Arial", 30, "bold"))
        gold_transaction_label.pack(
            padx=10, pady=(5, 0), side="top", anchor="w")

        frame_total_amount = customtkinter.CTkFrame(
            frame_header, fg_color="transparent")
        frame_total_amount.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        total_amount_label = customtkinter.CTkLabel(
            frame_total_amount, text="Total Amount (VND)", text_color="black",
            font=("Arial", 14))
        total_amount_label.grid(row=0, column=0, padx=5, pady=0, sticky="e")

        total_amount_number_label = customtkinter.CTkLabel(
            frame_total_amount, text="{}".format(total_amount),
            text_color="black",
            font=("Arial", 20, "bold"))
        total_amount_number_label.grid(
            row=1, column=0, padx=5, pady=0, sticky="e")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame_header, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=3,
                       sticky="ew", padx=10, pady=5)

        frame_header.columnconfigure(0, weight=1)
        frame_header.columnconfigure(1, weight=1)

    def calculate_total_amount_filter_result(self, transactions):
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction._total_amount
        return total_amount

    def create_gold_treeview_filter_result(self, frame,
                                           gold_transactions):
        total_amount_gold = self.calculate_total_amount_filter_result(
            gold_transactions)
        formatted_total_amount_gold = self.format_price_number(
            total_amount_gold)
        self.create_header_transaction_treeview(
            frame, formatted_total_amount_gold, "GOLD TRANSACTIONS")

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type", "Total Amount (VND)"
        ), show="headings", height=10)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Unit Price (VND/tael)",
                         text="Unit Price (VND/tael)", anchor="w")
        treeview.heading("Quantity (tael)", text="Quantity (tael)", anchor="w")
        treeview.heading("Gold Type", text="Gold Type", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")

        return treeview

    def create_currency_treeview_filter_result(self, frame,
                                               currency_transactions
                                               ):
        total_amount_currency = self.calculate_total_amount_filter_result(
            currency_transactions)
        formatted_total_amount_currency = self.format_price_number(
            total_amount_currency)
        self.create_header_transaction_treeview(
            frame, formatted_total_amount_currency, "CURRENCY TRANSACTIONS")

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)", "Total Amount (VND)"
        ), show="headings", height=10)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Quantity", text="Quantity", anchor="w")
        treeview.heading("Currency Type", text="Currency Type", anchor="w")
        treeview.heading("Exchange Rate (VND)",
                         text="Exchange Rate (VND)", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")
        return treeview

    def populate_treeview_with_gold_filter_result(self, treeview, transactions
                                                  ):
        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_unit_price = self.format_price_number(
                    transaction._unit_price)
                formatted_total_amount = self.format_price_number(
                    transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_unit_price,
                    transaction._quantity,
                    transaction._gold_type.name,
                    formatted_total_amount
                ))

    def populate_treeview_with_currency_filter_result(self,
                                                      treeview,
                                                      transactions):
        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_quantity = self.format_price_number(
                    transaction._quantity)
                formatted_exchange_rate = self.format_price_number(
                    transaction._exchange_rate._rate)
                formatted_total_amount = self.format_price_number(
                    transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_quantity,
                    transaction._currency_type.name,
                    formatted_exchange_rate,
                    formatted_total_amount
                ))

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount


class SearchWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Transaction Management - SEARCH")
        self.iconbitmap(default='./logo.ico')
        self.minsize(1720, 960)
        self.configure(fg_color="white")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

        self.transactions = \
            self.master.master.transaction_list.get_transactions()

    def create_widget(self):
        self.header_frame_for_search_window = HeaderFrameForWindow(
            master=self, label_header="SEARCH",
            submit_event=lambda: self.submit_event(),
            show_submit=False,
            show_search_bar=True
        )
        self.header_frame_for_search_window.pack(padx=10, pady=10, fill="x")

        self.create_search_result_frame()

    def create_search_result_frame(self):
        self.result_frame = customtkinter.CTkScrollableFrame(
            self, fg_color="#dbdbdb", bg_color="#ffffff",
            height=700)
        self.result_frame.pack(padx=10, pady=10, fill="x")

    def submit_event(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        choice = self.header_frame_for_search_window.optionmenu.get()

        for widget in self. \
                header_frame_for_search_window.entry_frame.winfo_children():
            if isinstance(widget, customtkinter.CTkEntry):
                if not widget.get():
                    messagebox.showerror(
                        "Missing Input", "Please fill in all fields.")
                    self.after(10, self.lift)
                    return

        if choice == "Date":
            day = self.header_frame_for_search_window.entry_day.get()
            month = self.header_frame_for_search_window._entry_month.get()
            year = self.header_frame_for_search_window.entry_year.get()
            if not day or not month or not year:
                messagebox.showerror(
                    "Missing Input", "Please fill in all date fields.")
                self.after(10, self.lift)
                return
            if not self.validate_date(day, month, year):
                messagebox.showerror(
                    "Invalid Date", "Please enter a valid date.")
                self.after(10, self.lift)
                return

        transactions_search = self.search_transactions(choice)
        self.total_transactions = len(transactions_search)

        search_result_label = customtkinter.CTkLabel(
            self.result_frame,
            text=f"Search results: {self.total_transactions} transactions",
            text_color="black",
            font=("Arial", 24, "bold"))
        search_result_label.pack(
            padx=10, pady=10, side="top", anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            self.result_frame, orient="horizontal",
            style="Separator.TSeparator")
        separator.pack(padx=10, pady=(10, 20), fill="x")

        self.create_content_treeview_search_result(
            self.result_frame, transactions_search)

    def validate_date(self, day, month, year):
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            return False

        if month < 1 or month > 12:
            return False

        if day < 1 or day > 31:
            return False

        if year < 1500:
            return False

        try:
            datetime.datetime(year, month, day)
        except ValueError:
            return False

        return True

    def search_transactions(self, choice):
        if choice == "Code":
            search_text = \
                self.header_frame_for_search_window.search_entry.get().upper()
            return [transaction for transaction in self.transactions
                    if search_text in transaction._id]
        elif choice == "Date":
            day = int(self.header_frame_for_search_window.entry_day.get())
            month = int(self.header_frame_for_search_window._entry_month.get())
            year = int(self.header_frame_for_search_window.entry_year.get())
            search_text = f"{day}/{month}/{year}"
            return [transaction for transaction in self.transactions
                    if transaction._day == day and transaction._month == month
                    and transaction._year == year]
        elif choice == "Type":
            search_text = \
                self.header_frame_for_search_window.search_entry.get().upper()
            if search_text == "GOLD":
                return [transaction for transaction in self.transactions
                        if isinstance(transaction, GoldTransaction)]
            elif search_text == "CURRENCY":
                return [transaction for transaction in self.transactions
                        if isinstance(transaction, CurrencyTransaction)]
            else:
                return []
        else:
            return []

    def create_content_treeview_search_result(self, frame, transactions):
        gold_transactions = [transaction for transaction in transactions
                             if isinstance(
                                 transaction, GoldTransaction)]
        currency_transactions = [transaction for transaction in transactions
                                 if isinstance(
                                     transaction, CurrencyTransaction)]

        frame_gold = customtkinter.CTkFrame(
            frame, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")
        frame_gold.pack(padx=5, pady=5, fill="x")

        if gold_transactions:
            treeview_gold_transaction \
                = self.create_gold_treeview_search_result(
                    frame_gold, gold_transactions)
            self.populate_treeview_with_gold_search_result(
                treeview_gold_transaction, gold_transactions)
            treeview_gold_transaction.pack(padx=20, pady=(10, 20), fill="x")
        else:
            frame_gold.destroy()

        frame_currency = customtkinter.CTkFrame(
            frame, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")
        frame_currency.pack(padx=5, pady=5, fill="x")

        if currency_transactions:
            treeview_currency_transaction \
                = self.create_currency_treeview_search_result(
                    frame_currency, currency_transactions)
            self.populate_treeview_with_currency_search_result(
                treeview_currency_transaction, currency_transactions)
            treeview_currency_transaction.pack(
                padx=20, pady=(10, 20), fill="x")
        else:
            frame_currency.destroy()

    def create_header_transaction_treeview(self, frame, total_amount, label):
        frame_header = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_header.pack(padx=5, pady=5, fill="x")

        frame_label = customtkinter.CTkFrame(
            frame_header, fg_color="transparent")
        frame_label.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=5)

        gold_transaction_label = customtkinter.CTkLabel(
            frame_label, text=label, text_color="black",
            font=("Arial", 30, "bold"))
        gold_transaction_label.pack(
            padx=10, pady=(5, 0), side="top", anchor="w")

        frame_total_amount = customtkinter.CTkFrame(
            frame_header, fg_color="transparent")
        frame_total_amount.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        total_amount_label = customtkinter.CTkLabel(
            frame_total_amount, text="Total Amount (VND)", text_color="black",
            font=("Arial", 14))
        total_amount_label.grid(row=0, column=0, padx=5, pady=0, sticky="e")

        total_amount_number_label = customtkinter.CTkLabel(
            frame_total_amount, text="{}".format(total_amount),
            text_color="black",
            font=("Arial", 20, "bold"))
        total_amount_number_label.grid(
            row=1, column=0, padx=5, pady=0, sticky="e")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame_header, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=3,
                       sticky="ew", padx=10, pady=5)

        frame_header.columnconfigure(0, weight=1)
        frame_header.columnconfigure(1, weight=1)

    def calculate_total_amount_search_result(self, transactions):
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction._total_amount
        return total_amount

    def create_gold_treeview_search_result(self, frame,
                                           gold_transactions):
        total_amount_gold = self.calculate_total_amount_search_result(
            gold_transactions)
        formatted_total_amount_gold = self.format_price_number(
            total_amount_gold)
        self.create_header_transaction_treeview(
            frame, formatted_total_amount_gold, "GOLD TRANSACTIONS")

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type", "Total Amount (VND)"
        ), show="headings", height=10)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Unit Price (VND/tael)",
                         text="Unit Price (VND/tael)", anchor="w")
        treeview.heading("Quantity (tael)", text="Quantity (tael)", anchor="w")
        treeview.heading("Gold Type", text="Gold Type", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")

        return treeview

    def create_currency_treeview_search_result(self, frame,
                                               currency_transactions
                                               ):
        total_amount_currency = self.calculate_total_amount_search_result(
            currency_transactions)
        formatted_total_amount_currency = self.format_price_number(
            total_amount_currency)
        self.create_header_transaction_treeview(
            frame, formatted_total_amount_currency, "CURRENCY TRANSACTIONS")

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)", "Total Amount (VND)"
        ), show="headings", height=10)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Quantity", text="Quantity", anchor="w")
        treeview.heading("Currency Type", text="Currency Type", anchor="w")
        treeview.heading("Exchange Rate (VND)",
                         text="Exchange Rate (VND)", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")
        return treeview

    def populate_treeview_with_gold_search_result(self, treeview, transactions
                                                  ):
        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_unit_price = self.format_price_number(
                    transaction._unit_price)
                formatted_total_amount = self.format_price_number(
                    transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_unit_price,
                    transaction._quantity,
                    transaction._gold_type.name,
                    formatted_total_amount
                ))

    def populate_treeview_with_currency_search_result(self,
                                                      treeview,
                                                      transactions):
        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_quantity = self.format_price_number(
                    transaction._quantity)
                formatted_exchange_rate = self.format_price_number(
                    transaction._exchange_rate._rate)
                formatted_total_amount = self.format_price_number(
                    transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_quantity,
                    transaction._currency_type.name,
                    formatted_exchange_rate,
                    formatted_total_amount
                ))

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount


class HeaderFrameForWindow(customtkinter.CTkFrame):
    def __init__(self, master, label_header, submit_event,
                 show_submit=True, show_search_bar=False, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#dbdbdb", bg_color="#ffffff")

        self.search_icon = customtkinter.CTkImage(
            Image.open('./search.ico'))

        self.label_transaction = customtkinter.CTkLabel(
            self, text=label_header, text_color="black",
            font=("TkDefaultFont", 24, "bold"))
        self.label_transaction.grid(
            row=0, column=0, sticky="w", padx=12, pady=5)

        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.grid(row=0, column=1, sticky="e", padx=12, pady=5)
        self.buttons_frame.configure(fg_color="transparent")

        self.btn_close = customtkinter.CTkButton(
            self.buttons_frame,
            text=f"CLOSE {label_header}",
            fg_color="#d93547",
            hover_color="dark red",
            command=self.master.destroy
        )
        self.btn_close.pack(side="right", padx=5, pady=5)

        if show_submit:
            self.btn_submit = customtkinter.CTkButton(
                self.buttons_frame,
                text=f"SUBMIT {label_header}",
                fg_color="green",
                hover_color="dark green",
                command=submit_event
            )
            self.btn_submit.pack(side="right", padx=5, pady=5)

        if show_search_bar:
            self.search_bar_frame = customtkinter.CTkFrame(
                master=self.buttons_frame,
                fg_color="transparent")
            self.search_bar_frame.pack(side="right", padx=5, pady=0)

            self.optionmenu = customtkinter. \
                CTkOptionMenu(self.search_bar_frame,
                              values=[
                                  "Code", "Date", "Type"],
                              command=self.option_menu_callback)
            self.optionmenu.set("Code")
            self.optionmenu.grid(row=0, column=0, padx=2, pady=0)

            self.entry_frame = customtkinter.CTkFrame(
                master=self.search_bar_frame,
                fg_color="transparent"
            )
            self.entry_frame.grid(row=0, column=1, padx=2, pady=0)

            self.search_entry = customtkinter.CTkEntry(
                self.entry_frame,
                placeholder_text="Search code... (Ex: GLD001)",
                width=280)
            self.search_entry.grid(row=0, column=0, padx=2, pady=0)

            self.btn_submit_search = customtkinter.CTkButton(
                self.search_bar_frame,
                text=None,
                image=self.search_icon,
                width=30, height=30, command=submit_event)
            self.btn_submit_search.grid(row=0, column=2, padx=2, pady=0)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def option_menu_callback(self, choice):
        if self.entry_frame is not None:
            self.entry_frame.destroy()

        if choice == "Code":
            self.entry_frame = customtkinter.CTkFrame(
                master=self.search_bar_frame,
                fg_color="transparent"
            )
            self.entry_frame.grid(row=0, column=1, padx=2, pady=0)

            self.search_entry = customtkinter.CTkEntry(
                self.entry_frame,
                placeholder_text="Search code... (Ex: GLD001)",
                width=280)
            self.search_entry.grid(row=0, column=1, padx=2, pady=0)
        elif choice == "Date":
            if hasattr(self, "date_frame"):
                self.date_frame.destroy()

            self.entry_frame = customtkinter.CTkFrame(
                master=self.search_bar_frame,
                fg_color="transparent"
            )
            self.entry_frame.grid(row=0, column=1, padx=2, pady=0)

            date_frame = customtkinter.CTkFrame(
                master=self.entry_frame,
                fg_color="transparent"
            )
            date_frame.grid(row=0, column=1, padx=5, pady=0)

            self.entry_day = customtkinter.CTkEntry(
                master=date_frame, placeholder_text="Day", width=80)
            self.entry_day.grid(row=0, column=0, padx=5, pady=0)

            separator_day_month = ttk.Separator(
                date_frame, orient="horizontal", style="Separator.TSeparator")
            separator_day_month.grid(row=0, column=1,
                                     padx=0, pady=0, sticky="ew")

            self._entry_month = customtkinter.CTkEntry(
                master=date_frame, placeholder_text="Month", width=80)
            self._entry_month.grid(row=0, column=2, padx=5, pady=0)

            separator_month_year = ttk.Separator(
                date_frame, orient="horizontal", style="Separator.TSeparator")
            separator_month_year.grid(
                row=0, column=3, padx=0, pady=0, sticky="ew")

            self.entry_year = customtkinter.CTkEntry(
                master=date_frame, placeholder_text="Year", width=80)
            self.entry_year.grid(row=0, column=4, padx=5, pady=0)
        elif choice == "Type":
            self.entry_frame = customtkinter.CTkFrame(
                master=self.search_bar_frame,
                fg_color="transparent"
            )
            self.entry_frame.grid(row=0, column=1, padx=2, pady=0)

            self.search_entry = customtkinter.CTkEntry(
                self.entry_frame, placeholder_text="Search type... (Ex: Gold)",
                width=280)
            self.search_entry.grid(row=0, column=1, padx=2, pady=0)


class AddTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Add Transaction")
        self.iconbitmap(default='./logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        self.add_transaction_tab_views = AddTransactionTabView(
            master=self)
        self.add_transaction_tab_views.pack(padx=20, pady=5, fill="x")


class AddTransactionTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff", bg_color="#d9d9d9",
                       border_width=2, border_color="#989DA1")

        self.tab_add_gold_transaction = self.add("GOLD")
        self.tab_add_currency_transaction = self.add("CURRENCY")

        self.set("GOLD")
        self.configure(corner_radius=5)

        with open('data.json', 'r') as json_file:
            data = json.load(json_file)

        self.exchange_rates = data['exchange_rates']

        self.create_widgets()

    def create_widgets(self):
        self.create_tab_add_gold_transaction(
            self.tab_add_gold_transaction)
        self.create_tab_add_currency_transaction(
            self.tab_add_currency_transaction)

    def create_tab_add_gold_transaction(self, tab):
        label_unit_price = customtkinter.CTkLabel(
            master=tab,
            text="Unit Price (VND/tael):",
            font=("Arial", 14),
            text_color="black",
        )
        label_unit_price.pack(padx=20, pady=5, anchor="w")

        self.gold_entry_unit_price = customtkinter.CTkEntry(
            master=tab, placeholder_text="Ex: 85,200,000.7")
        self.gold_entry_unit_price.pack(padx=20, pady=0, anchor="w", fill="x")

        label_quantity = customtkinter.CTkLabel(
            master=tab,
            text="Quantity (tael):",
            font=("Arial", 14),
            text_color="black",
        )
        label_quantity.pack(padx=20, pady=5, anchor="w")

        self.gold_entry_quantity = customtkinter.CTkEntry(
            master=tab, placeholder_text="Ex: 10")
        self.gold_entry_quantity.pack(padx=20, pady=0, anchor="w", fill="x")

        label_gold_type = customtkinter.CTkLabel(
            master=tab,
            text="Gold Type:",
            font=("Arial", 14),
            text_color="black",
        )
        label_gold_type.pack(padx=20, pady=5, anchor="w")

        self.gold_combobox_gold_type = customtkinter.CTkComboBox(tab, values=[
            "SJC", "PNJ", "DOJI"
        ])
        self.gold_combobox_gold_type.set("SJC")
        self.gold_combobox_gold_type.pack(
            padx=20, pady=0, anchor="w", fill="x")

        label_transaction_date = customtkinter.CTkLabel(
            master=tab,
            text="Transaction Date:",
            font=("Arial", 14),
            text_color="black",
        )
        label_transaction_date.pack(padx=20, pady=5, anchor="w")

        date_frame = customtkinter.CTkFrame(
            master=tab,
            fg_color="transparent"
        )
        date_frame.pack(padx=20, pady=(0, 5), anchor="w", fill="x")

        self.gold_entry_day = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Day", width=95)
        self.gold_entry_day.grid(
            row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        separator_day_month = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_day_month.grid(row=0, column=1,
                                 padx=0, pady=0, sticky="ew")

        self.gold_entry_month = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Month", width=95)
        self.gold_entry_month.grid(row=0, column=2, padx=5, pady=0)

        separator_month_year = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_month_year.grid(
            row=0, column=3, padx=0, pady=0, sticky="ew")

        self.gold_entry_year = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Year", width=95)
        self.gold_entry_year.grid(row=0, column=4, padx=(5, 0), pady=0)

        buttons_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=(100, 5), anchor="w", fill="x")

        button_confirm = customtkinter.CTkButton(
            buttons_frame,
            text="CONFIRM",
            width=150,
            command=self.gold_confirm_button_callback)
        button_confirm.grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=5)

        button_cancel = customtkinter.CTkButton(
            buttons_frame,
            text="CANCEL",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.master.destroy)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=5)

    def gold_confirm_button_callback(self):
        unit_price = self.gold_entry_unit_price.get()
        quantity = self.gold_entry_quantity.get()
        day_submit = self.gold_entry_day.get()
        month_submit = self.gold_entry_month.get()
        year_submit = self.gold_entry_year.get()
        gold_type = self.gold_combobox_gold_type.get()

        if not all([unit_price, quantity, day_submit, month_submit,
                    year_submit, gold_type]):
            messagebox.showerror(
                "Missing Input", "Please fill in all fields.")
            self.focus()
            return

        unit_price = self.validate_and_convert_input(unit_price)
        if unit_price is None:
            messagebox.showerror(
                "Invalid Unit Price", "Unit Price must be a valid number.")
            self.focus()
            return

        quantity = self.validate_and_convert_input(quantity)
        if quantity is None:
            messagebox.showerror(
                "Invalid Quantity", "Quantity must be a valid number.")
            self.focus()
            return

        if not all(map(str.isdigit, [day_submit, month_submit, year_submit])):
            messagebox.showerror(
                "Invalid Input", "Please enter valid numerical \
                \nvalues for date fields.")
            self.after(10, self.lift)
            return

        day = int(day_submit)
        month = int(month_submit)
        year = int(year_submit)

        if not self.validate_date(day, month, year):
            messagebox.showerror("Invalid Date", "Date is not valid.")
            self.focus()
            return

        if gold_type not in ["SJC", "PNJ", "DOJI"]:
            messagebox.showerror("Invalid Gold Type",
                                 "Gold Type must be 'SJC', 'PNJ', or 'DOJI'.")
            self.focus()
            return

        with open("data.json", "r") as file:
            data = json.load(file)

        new_data = {
            "id": "",
            "day": day,
            "month": month,
            "year": year,
            "unit_price": unit_price,
            "quantity": quantity,
            "type": "gold",
            "gold_type": GoldType[self.gold_combobox_gold_type.get()].value,
            "isdeleted": False
        }

        new_data_id = self.generate_gold_id(data["transactions"])
        new_data["id"] = new_data_id

        data["transactions"].append(new_data)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Success", "Gold transaction added successfully. \
                            \nPlease Refresh Data!")
        self.focus()

    def generate_gold_id(self, transactions):
        gold_transactions = [t for t in transactions if t["type"] == "gold"]
        num_gold_transactions = len(gold_transactions)

        new_id = f"GLD{num_gold_transactions + 1:03}"

        for transaction in transactions:
            if transaction["id"] == new_id:
                num_gold_transactions += 1
                new_id = f"GLD{num_gold_transactions + 1:03}"

        return new_id

    def create_tab_add_currency_transaction(self, tab):
        label_quantity = customtkinter.CTkLabel(
            master=tab,
            text="Quantity:",
            font=("Arial", 14),
            text_color="black",
        )
        label_quantity.pack(padx=20, pady=5, anchor="w")

        self.currency_entry_quantity = customtkinter.CTkEntry(
            master=tab, placeholder_text="Ex: 50")
        self.currency_entry_quantity.pack(
            padx=20, pady=0, anchor="w", fill="x")

        label_currency_type = customtkinter.CTkLabel(
            master=tab,
            text="Currency Type:",
            font=("Arial", 14),
            text_color="black",
        )
        label_currency_type.pack(padx=20, pady=5, anchor="w")

        self.currency_combobox_currency_type = \
            customtkinter.CTkComboBox(tab,
                                      values=[
                                          "VND", "USD", "EUR"
                                      ],
                                      command=self.
                                      combobox_currency_type_callback)
        self.currency_combobox_currency_type.set("VND")
        self.currency_combobox_currency_type.pack(
            padx=20, pady=0, anchor="w", fill="x")

        label_exchange_rate = customtkinter.CTkLabel(
            master=tab,
            text="Exchange Rate (VND):",
            font=("Arial", 14),
            text_color="black",
        )
        label_exchange_rate.pack(padx=20, pady=5, anchor="w")

        self.currency_entry_exchange_rate = customtkinter.CTkEntry(
            master=tab, placeholder_text="23,130.6")
        self.currency_entry_exchange_rate.pack(padx=20, pady=0, anchor="w",
                                               fill="x")
        self.currency_entry_exchange_rate.insert(
            0, str(self.exchange_rates[0]["rate"]))
        self.currency_entry_exchange_rate.configure(state="readonly")

        label_transaction_date = customtkinter.CTkLabel(
            master=tab,
            text="Transaction Date:",
            font=("Arial", 14),
            text_color="black",
        )
        label_transaction_date.pack(padx=20, pady=5, anchor="w")

        date_frame = customtkinter.CTkFrame(
            master=tab,
            fg_color="transparent"
        )
        date_frame.pack(padx=20, pady=(0, 5), anchor="w", fill="x")

        self.currency_entry_day = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Day", width=95)
        self.currency_entry_day.grid(row=0, column=0, padx=(0, 5), pady=0,
                                     sticky="ew")

        separator_day_month = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_day_month.grid(row=0, column=1,
                                 padx=0, pady=0, sticky="ew")

        self.currency_entry_month = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Month", width=95)
        self.currency_entry_month.grid(row=0, column=2, padx=5, pady=0)

        separator_month_year = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_month_year.grid(
            row=0, column=3, padx=0, pady=0, sticky="ew")

        self.currency_entry_year = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Year", width=95)
        self.currency_entry_year.grid(row=0, column=4, padx=(5, 0), pady=0)

        buttons_frame = customtkinter.CTkFrame(tab, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=(100, 5), anchor="w", fill="x")

        button_confirm = customtkinter.CTkButton(
            buttons_frame,
            text="CONFIRM",
            width=150,
            command=self.currency_confirm_button_callback)
        button_confirm.grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=5)

        button_cancel = customtkinter.CTkButton(
            buttons_frame,
            text="CANCEL",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.master.destroy)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=5)

    def combobox_currency_type_callback(self, choice):
        try:
            currency_type = CurrencyType[choice].value
        except KeyError:
            return

        exchange_rate = self.get_exchange_rate(currency_type)
        self.currency_entry_exchange_rate.configure(state="normal")
        self.currency_entry_exchange_rate.delete(0, "end")
        self.currency_entry_exchange_rate.insert(0, str(exchange_rate))
        self.currency_entry_exchange_rate.configure(state="readonly")

    def get_exchange_rate(self, currency_type):
        for rate in self.exchange_rates:
            if rate['currency_type'] == currency_type:
                return self.format_price_number(rate['rate'])

        return self.format_price_number(0.0)

    def currency_confirm_button_callback(self):
        quantity = self.currency_entry_quantity.get()
        exchange_rate = self.currency_entry_exchange_rate.get()
        day_submit = self.currency_entry_day.get()
        month_submit = self.currency_entry_month.get()
        year_submit = self.currency_entry_year.get()
        currency_type = self.currency_combobox_currency_type.get()

        if not all([quantity, exchange_rate, day_submit, month_submit,
                    year_submit, currency_type]):
            messagebox.showerror(
                "Missing Input", "Please fill in all fields.")
            self.focus()
            return

        quantity = self.validate_and_convert_input(quantity)
        if quantity is None:
            messagebox.showerror(
                "Invalid Quantity", "Quantity must be a valid number.")
            self.focus()
            return

        exchange_rate = self.validate_and_convert_input(exchange_rate)
        if exchange_rate is None:
            messagebox.showerror(
                "Invalid Exchange Rate",
                "Exchange Rate must be a valid number.")
            self.focus()
            return

        if not all(map(str.isdigit, [day_submit, month_submit, year_submit])):
            messagebox.showerror(
                "Invalid Input", "Please enter valid numerical \
                \nvalues for date fields.")
            self.after(10, self.lift)
            return

        day = int(day_submit)
        month = int(month_submit)
        year = int(year_submit)

        if not self.validate_date(day, month, year):
            messagebox.showerror("Invalid Date", "Date is not valid.")
            self.focus()
            return

        if currency_type not in ["VND", "USD", "EUR"]:
            messagebox. \
                showerror("Invalid Currency Type",
                          "Currency Type must be 'VND', 'USD', or 'EUR'.")
            self.focus()
            return

        with open("data.json", "r") as file:
            data = json.load(file)

        exchange_rates = data["exchange_rates"]

        exchange_rate = None
        for rate in exchange_rates:
            if rate["currency_type"] == CurrencyType[currency_type].value:
                exchange_rate = rate
                break

        if exchange_rate is None:
            messagebox.showerror("Exchange Rate Not Found",
                                 f"No exchange rate found for currency type \
                                {currency_type}.")
            self.focus()
            return

        new_data = {
            "id": "",
            "day": day,
            "month": month,
            "year": year,
            "quantity": quantity,
            "type": "currency",
            "currency_type": CurrencyType[currency_type].value,
            "exchange_rate": exchange_rate,
            "isdeleted": False
        }

        new_data_id = self.generate_currency_id(data["transactions"])
        new_data["id"] = new_data_id

        data["transactions"].append(new_data)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Success",
                            "Currency transaction added successfully. \
                            Please Refresh Data!")
        self.focus()

    def generate_currency_id(self, transactions):
        currency_transactions = [
            t for t in transactions if t["type"] == "currency"]
        num_currency_transactions = len(currency_transactions)

        new_id = f"CUR{num_currency_transactions + 1:03}"

        for transaction in transactions:
            if transaction["id"] == new_id:
                num_currency_transactions += 1
                new_id = f"CUR{num_currency_transactions + 1:03}"

        return new_id

    def validate_and_convert_input(self, input_str):
        try:
            input_str = input_str.replace(",", "")
            return float(input_str)
        except ValueError:
            return None

    def validate_date(self, day, month, year):
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            return False

        if month < 1 or month > 12:
            return False

        if day < 1 or day > 31:
            return False

        if year < 1500:
            return False

        try:
            datetime.datetime(year, month, day)
        except ValueError:
            return False

        return True

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount


class ReportWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Report")
        self.iconbitmap(default='./logo.ico')
        self.minsize(1700, 990)
        self.configure(fg_color="#eaeaea")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        self.header_frame = HeaderFrameForReportWindow(master=self)
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.tab_report = TabReport(master=self)
        self.tab_report.grid(row=1, column=0, padx=10,
                             pady=(0, 10), sticky="ew")

        self.grid_columnconfigure(0, weight=1)


class HeaderFrameForReportWindow(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#dbdbdb", bg_color="#f2f2f2")

        self.label_report = customtkinter.CTkLabel(
            self, text="Overview", text_color="black",
            font=("TkDefaultFont", 24, "bold"))
        self.label_report.grid(
            row=0, column=0, sticky="w", padx=12, pady=5)

        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.grid(row=0, column=1, sticky="e", padx=12, pady=5)
        self.buttons_frame.configure(fg_color="transparent")

        self.btn_close = customtkinter.CTkButton(
            self.buttons_frame,
            text="CLOSE REPORT",
            fg_color="#d93547",
            hover_color="dark red",
            command=self.master.destroy
        )
        self.btn_close.pack(side="right", padx=5, pady=5)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)


class TabReport(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.total_details_window = None
        self.configure(fg_color="#dbdbdb", bg_color="#eaeaea",
                       border_width=1, border_color="#989DA1")

        self.tab_week = self.add("WEEK")
        self.tab_month = self.add("MONTH")

        self.set("MONTH")
        self.configure(corner_radius=5)

        self.all_transactions = \
            self.master.master.master.transaction_list.get_transactions()

        self.create_tab_report_widgets()

    def create_tab_report_widgets(self):
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        current_week = now.isocalendar()[1]

        transactions_this_month = [
            txn for txn in self.all_transactions
            if txn._year == current_year and txn._month == current_month
        ]

        transactions_this_week = [
            txn for txn in self.all_transactions
            if txn._year ==
            current_year and datetime.date(txn._year,
                                           txn._month,
                                           txn._day).isocalendar()[1]
            == current_week
        ]

        # Month
        month_scroll_frame = customtkinter.CTkScrollableFrame(
            self.tab_month, fg_color="transparent",
            height=850)
        month_scroll_frame.pack(padx=0, pady=0, fill="x")

        frame_month_1 = customtkinter.CTkFrame(
            master=month_scroll_frame,
            fg_color="transparent",
        )
        frame_month_1.pack(padx=5, pady=5, fill="x")

        frame_month_1.grid_columnconfigure(0, weight=1)
        frame_month_1.grid_columnconfigure(1, weight=2)

        month_total_chart = \
            self.create_total_chart_frame(frame_month_1,
                                          transactions_this_month,
                                          btn_details_status=True)
        month_total_chart.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        month_recent_transaction = \
            self.create_recent_transaction_frame(frame_month_1,
                                                 transactions_this_month)
        month_recent_transaction.grid(row=0, column=1, columnspan=2,
                                      padx=5, pady=5, sticky="ew")

        frame_month_2 = customtkinter.CTkFrame(
            master=month_scroll_frame,
            fg_color="transparent",
        )
        frame_month_2.pack(padx=5, pady=(0, 5), fill="x")

        month_statistics_chart = \
            self.create_statistics_chart_frame(frame_month_2,
                                               transactions_this_month,
                                               self.tab_month,
                                               btn_details_status=True)
        month_statistics_chart.pack(padx=5, pady=(2, 5), fill="x")

        # Week
        week_scroll_frame = customtkinter.CTkScrollableFrame(
            self.tab_week, fg_color="transparent",
            height=850)
        week_scroll_frame.pack(padx=0, pady=0, fill="x")

        frame_week_1 = customtkinter.CTkFrame(
            master=week_scroll_frame,
            fg_color="transparent",
        )
        frame_week_1.pack(padx=5, pady=5, fill="x")

        frame_week_1.grid_columnconfigure(0, weight=1)
        frame_week_1.grid_columnconfigure(1, weight=2)

        week_total_chart = \
            self.create_total_chart_frame(frame_week_1,
                                          transactions_this_week,
                                          btn_details_status=True)
        week_total_chart.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        week_recent_transaction = \
            self.create_recent_transaction_frame(frame_week_1,
                                                 transactions_this_week)
        week_recent_transaction.grid(row=0, column=1, columnspan=2,
                                     padx=5, pady=5, sticky="ew")

        frame_week_2 = customtkinter.CTkFrame(
            master=week_scroll_frame,
            fg_color="transparent",
        )
        frame_week_2.pack(padx=5, pady=(0, 5), fill="x")

        week_statistics_chart = \
            self.create_statistics_chart_frame(frame_week_2,
                                               transactions_this_week,
                                               self.tab_week,
                                               btn_details_status=True)
        week_statistics_chart.pack(padx=5, pady=(2, 5), fill="x")

    def create_total_chart_frame(self, parent, transactions,
                                 btn_details_status):
        total_chart_frame = customtkinter.CTkFrame(
            master=parent, fg_color="#ffffff",
            border_width=2, border_color="#989DA1",
            corner_radius=5)

        frame_title_and_button = customtkinter.CTkFrame(
            master=total_chart_frame, fg_color="transparent")
        frame_title_and_button.pack(padx=10, pady=(20, 0), fill="x")

        frame_title_and_button.columnconfigure(0, weight=0)
        frame_title_and_button.columnconfigure(1, weight=1)

        total_chart_title = customtkinter.CTkLabel(
            master=frame_title_and_button,
            text="Total",
            font=("Arial", 20, "bold"),
            text_color="black",
        )
        total_chart_title.grid(
            row=0, column=0, sticky="w", padx=12, pady=0)

        if btn_details_status:
            btn_details_report = customtkinter.CTkButton(
                frame_title_and_button,
                text="See Details",
                fg_color="transparent",
                hover_color="#dae6f2",
                text_color="#5C8ECB",
                font=("Arial", 14, "bold"),
                width=30,
                command=lambda: self.open_total_details_window(transactions)
            )
            btn_details_report.grid(
                row=0, column=1, sticky="e", padx=12, pady=0)

        self.total_details_window = None

        if not transactions:
            no_data_label = customtkinter.CTkLabel(
                master=total_chart_frame,
                text="No data available this month!",
                font=("Arial", 20, "bold")
            )
            no_data_label.pack(padx=25, pady=110, fill="x")

            return total_chart_frame

        # total_amount_transaction = 0
        # gold_total_amount_transaction = 0
        # currency_total_amount_transaction = 0
        # total_amount_quantity_transaction = 0
        # gold_total_amount_quantity_transaction = 0
        # currency_total_amount_quantity_transaction = 0
        # for transaction in transactions:
        #     total_amount_transaction += transaction._total_amount
        #     total_amount_quantity_transaction += 1
        #     if isinstance(transaction, GoldTransaction):
        #         gold_total_amount_transaction += transaction._total_amount
        #         gold_total_amount_quantity_transaction += 1
        #     if isinstance(transaction, CurrencyTransaction):
        #         currency_total_amount_transaction += \
        #             transaction._total_amount
        #         currency_total_amount_quantity_transaction += 1

        total_amounts = np.array([txn._total_amount for txn in transactions])
        total_amount_transaction = np.sum(total_amounts)
        total_amount_quantity_transaction = len(transactions)

        gold_transactions = [
            txn for txn in transactions if isinstance(txn, GoldTransaction)]
        currency_transactions = [
            txn for txn in transactions if isinstance(txn,
                                                      CurrencyTransaction)]

        # gold_total_amount_transaction = np.sum(
        #     [txn._total_amount for txn in gold_transactions])
        # currency_total_amount_transaction = np.sum(
        #     [txn._total_amount for txn in currency_transactions])

        gold_total_amount_quantity_transaction = len(gold_transactions)
        currency_total_amount_quantity_transaction = len(currency_transactions)

        formatted_total_amount = self.format_price_number(
            total_amount_transaction)

        total_value = customtkinter.CTkLabel(
            master=total_chart_frame,
            text=f"{formatted_total_amount} VND ({
                total_amount_quantity_transaction})",
            anchor="w"
        )
        total_value.pack(padx=25, pady=0, fill="x")

        gold_percentage = (gold_total_amount_quantity_transaction
                           / total_amount_quantity_transaction) * 100 \
            if total_amount_quantity_transaction != 0 else 0
        currency_percentage = (currency_total_amount_quantity_transaction /
                               total_amount_quantity_transaction) * 100 \
            if total_amount_quantity_transaction != 0 else 0

        piechart_values = [gold_percentage, currency_percentage]
        piechart_labels = ["Gold", "Currency"]
        piechart_colors = ["#f5d45f", "#2ea64d"]

        fig, ax = plt.subplots()
        ax.pie(piechart_values, labels=piechart_labels, autopct='%1.1f%%',
               colors=piechart_colors)
        ax.legend(title="Category", loc='center left',
                  bbox_to_anchor=(-0.55, 0.5))

        fig.set_size_inches(3, 3)

        canvas = FigureCanvasTkAgg(fig, master=total_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

        return total_chart_frame

    def create_recent_transaction_frame(self, parent, transactions):
        recent_transaction_frame = customtkinter.CTkFrame(
            master=parent, fg_color="#ffffff",
            border_width=2, border_color="#989DA1",
            corner_radius=5)

        recent_transaction_title = customtkinter.CTkLabel(
            master=recent_transaction_frame,
            text="Recent Transaction",
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="w"
        )
        recent_transaction_title.pack(padx=20, pady=(20, 5), fill="x")

        gold_transaction_title = customtkinter.CTkLabel(
            master=recent_transaction_frame,
            text="GOLD TRANSACTION",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w"
        )
        gold_transaction_title.pack(padx=20, pady=0, fill="x")

        gold_treeview = \
            self.create_gold_transaction_treeview(recent_transaction_frame)
        self.populate_treeview_with_gold_transactions(
            gold_treeview, transactions)
        gold_treeview.pack(padx=20, pady=5, fill="x")

        currency_transaction_title = customtkinter.CTkLabel(
            master=recent_transaction_frame,
            text="CURRENCY TRANSACTION",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w"
        )
        currency_transaction_title.pack(padx=20, pady=0, fill="x")

        currency_treeview = \
            self.create_currency_transaction_treeview(recent_transaction_frame)
        self.populate_treeview_with_currency_transactions(
            currency_treeview, transactions)
        currency_treeview.pack(padx=20, pady=(5, 20), fill="x")

        return recent_transaction_frame

    def create_statistics_chart_frame(self, parent, transactions,
                                      tab_type, btn_details_status):
        statistics_chart_frame = customtkinter.CTkFrame(
            master=parent, fg_color="#ffffff",
            border_width=2, border_color="#989DA1",
            corner_radius=5)

        frame_title_and_button = customtkinter.CTkFrame(
            master=statistics_chart_frame, fg_color="transparent")
        frame_title_and_button.pack(padx=10, pady=(20, 0), fill="x")

        frame_title_and_button.columnconfigure(0, weight=0)
        frame_title_and_button.columnconfigure(1, weight=1)

        statistics_chart_title = customtkinter.CTkLabel(
            master=frame_title_and_button,
            text="Statistics",
            font=("Arial", 20, "bold"),
            text_color="black",
        )
        statistics_chart_title.grid(
            row=0, column=0, sticky="w", padx=12, pady=0)

        if btn_details_status and tab_type == self.tab_month:
            btn_statistics_report = customtkinter.CTkButton(
                frame_title_and_button,
                text="See Details",
                fg_color="transparent",
                hover_color="#dae6f2",
                text_color="#5C8ECB",
                font=("Arial", 14, "bold"),
                width=30,
                command=lambda: self.open_statistics_details_month_window(
                    transactions)
            )
            btn_statistics_report.grid(row=0, column=1,
                                       sticky="e", padx=12, pady=0)

        self.statistics_details_month_window = None

        if btn_details_status and tab_type == self.tab_week:
            btn_statistics_report = customtkinter.CTkButton(
                frame_title_and_button,
                text="See Details",
                fg_color="transparent",
                hover_color="#dae6f2",
                text_color="#5C8ECB",
                font=("Arial", 14, "bold"),
                width=30,
                command=lambda: self.open_statistics_details_week_window(
                    transactions)
            )
            btn_statistics_report.grid(row=0, column=1,
                                       sticky="e", padx=12, pady=0)

        self.statistics_details_week_window = None

        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        month_name = str(MonthLabel(current_month))

        statistics_value = customtkinter.CTkLabel(
            master=statistics_chart_frame,
            text=f"{month_name} {current_year}",
            font=("Arial", 14),
            anchor="w"
        )
        statistics_value.pack(padx=22, pady=0, fill="x")

        if not transactions:
            no_data_label = customtkinter.CTkLabel(
                master=statistics_chart_frame,
                text="No data available this month!",
                font=("Arial", 20, "bold")
            )
            no_data_label.pack(padx=25, pady=110, fill="x")

            return statistics_chart_frame

        if tab_type == self.tab_month:
            weeks = self.get_weeks_of_month(current_year, current_month)
            totals = self.get_total_amount_per_week(transactions, weeks)

            self.plot_bar_chart_for_this_month(statistics_chart_frame,
                                               weeks, totals)
            self.plot_markers_chart_for_this_month(statistics_chart_frame,
                                                   weeks, totals)

        elif tab_type == self.tab_week:
            self.plot_bar_chart_for_this_week(statistics_chart_frame,
                                              transactions)
            self.plot_markers_chart_for_this_week(statistics_chart_frame,
                                                  transactions)

        return statistics_chart_frame

    def get_weeks_of_month(self, year, month):
        weeks = []
        first_day_of_month = datetime.date(year, month, 1)
        first_day_of_week = first_day_of_month - \
            datetime.timedelta(days=first_day_of_month.weekday())

        i = 0
        while True:
            start_of_week = first_day_of_week + datetime.timedelta(weeks=i)
            end_of_week = start_of_week + datetime.timedelta(days=6)

            if start_of_week.month != month:
                start_of_week = datetime.date(year, month, 1)
            if end_of_week.month != month:
                last_day_of_month = datetime.date(year, month + 1, 1) \
                    - datetime.timedelta(days=1) \
                    if month < 12 else datetime.date(year, 12, 31)
                end_of_week = last_day_of_month

            weeks.append((start_of_week, end_of_week))
            i += 1

            if end_of_week == datetime.date(year, month, 1) \
                + datetime.timedelta(days=(datetime.date(year, month + 1, 1)
                                           - datetime.date(
                                               year, month, 1)).days - 1):
                break

        return weeks

    def plot_bar_chart_for_this_month(self, parent, weeks, totals):
        week_labels = [
            f"Week {i+1}\n{start.strftime('%d/%m/%Y')
                           } - {end.strftime('%d/%m/%Y')}"
            for i, (start, end) in enumerate(weeks)
        ]

        gold_totals = [0] * len(weeks)
        currency_totals = [0] * len(weeks)
        for i, (start, end) in enumerate(weeks):
            for txn in self.all_transactions:
                txn_date = datetime.date(txn._year, txn._month, txn._day)
                if start <= txn_date <= end:
                    if isinstance(txn, GoldTransaction):
                        gold_totals[i] += txn._total_amount
                    elif isinstance(txn, CurrencyTransaction):
                        currency_totals[i] += txn._total_amount

        fig, ax = plt.subplots()
        bar_width = 0.2
        x = np.arange(len(weeks))

        ax.bar(x - bar_width, gold_totals,
               width=bar_width, label='Gold', color='#f5d45f')
        ax.bar(x, currency_totals, width=bar_width,
               label='Currency', color='#2ea64d')
        ax.bar(x + bar_width, totals, width=bar_width,
               label='Total')

        ax.set_xlabel('Weeks')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Weekly Total Amount for Current Month')
        ax.set_xticks(x)
        ax.set_xticklabels(week_labels, ha='center')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_total = max(totals, default=0)
        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}' if x < 1_000_000
            else f'{int(x // 1_000_000)}M'
        )

        for i, v in enumerate(totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center', va='bottom')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 2), fill="x")

    def plot_markers_chart_for_this_month(self, parent, weeks, totals):
        week_labels = [
            f"Week {i+1}\n{start.strftime('%d/%m/%Y')
                           } - {end.strftime('%d/%m/%Y')}"
            for i, (start, end) in enumerate(weeks)
        ]

        gold_totals = [0] * len(weeks)
        currency_totals = [0] * len(weeks)
        for i, (start, end) in enumerate(weeks):
            for txn in self.all_transactions:
                txn_date = datetime.date(txn._year, txn._month, txn._day)
                if start <= txn_date <= end:
                    if isinstance(txn, GoldTransaction):
                        gold_totals[i] += txn._total_amount
                    elif isinstance(txn, CurrencyTransaction):
                        currency_totals[i] += txn._total_amount

        fig, ax = plt.subplots()

        ax.plot(week_labels, gold_totals, marker='o', linestyle='-',
                label='Gold', color='#f5d45f')
        ax.plot(week_labels, currency_totals, marker='o', linestyle='-',
                label='Currency', color='#2ea64d')
        ax.plot(week_labels, totals, marker='o', linestyle='-',
                label='Total')

        ax.set_xlabel('Weeks')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Weekly Total Amount for Current Month')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_total = max(totals, default=0)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))

        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M'
        )

        for i, v in enumerate(totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center',
                    va='bottom')

        for i, v in enumerate(gold_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center', va='bottom',
                    color='#f5d45f')

        for i, v in enumerate(currency_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center', va='bottom',
                    color='#2ea64d')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 2), fill="x")

    def plot_bar_chart_for_this_week(self, parent, transactions):
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        date_labels = [(start_of_week + datetime.timedelta(days=i)
                        ).strftime("%A\n%d/%m/%Y") for i in range(7)]

        totals = {day: 0 for day in days}
        gold_totals = {day: 0 for day in days}
        currency_totals = {day: 0 for day in days}

        for transaction in transactions:
            transaction_date = datetime.date(
                transaction._year, transaction._month, transaction._day)
            day_of_week = transaction_date.strftime('%A')
            if day_of_week in totals:
                totals[day_of_week] += transaction._total_amount
                if isinstance(transaction, GoldTransaction):
                    gold_totals[day_of_week] += transaction._total_amount
                elif isinstance(transaction, CurrencyTransaction):
                    currency_totals[day_of_week] += transaction._total_amount

        total_amounts = [totals[day] for day in days]
        gold_amounts = [gold_totals[day] for day in days]
        currency_amounts = [currency_totals[day] for day in days]

        fig, ax = plt.subplots()
        bar_width = 0.2
        x = np.arange(len(days))

        ax.bar(x - bar_width, gold_amounts, width=bar_width, label='Gold',
               color='#f5d45f')
        ax.bar(
            x, currency_amounts, width=bar_width, label='Currency',
            color='#2ea64d')
        ax.bar(x + bar_width, total_amounts, width=bar_width, label='Total')

        ax.set_xlabel('Days of the Week')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Total Amounts for Each Day of the Week')
        ax.set_xticks(x)
        ax.set_xticklabels(date_labels, ha='center')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_total = max(total_amounts, default=0)
        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(total_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i + bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

    def plot_markers_chart_for_this_week(self, parent, transactions):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        date_labels = [(start_of_week
                        + datetime.timedelta(days=i)).strftime("%A\n%d/%m/%Y")
                       for i in range(7)]

        totals = {day: 0 for day in days}
        gold_totals = {day: 0 for day in days}
        currency_totals = {day: 0 for day in days}

        for transaction in transactions:
            transaction_date = datetime.date(
                transaction._year, transaction._month, transaction._day)
            day_of_week = transaction_date.strftime('%A')
            if day_of_week in totals:
                totals[day_of_week] += transaction._total_amount
                if isinstance(transaction, GoldTransaction):
                    gold_totals[day_of_week] += transaction._total_amount
                elif isinstance(transaction, CurrencyTransaction):
                    currency_totals[day_of_week] += transaction._total_amount

        total_amounts = [totals[day] for day in days]
        gold_amounts = [gold_totals[day] for day in days]
        currency_amounts = [currency_totals[day] for day in days]

        fig, ax = plt.subplots()

        ax.plot(date_labels, gold_amounts, marker='o',
                linestyle='-', label='Gold', color='#f5d45f')
        ax.plot(date_labels, currency_amounts, marker='o',
                linestyle='-', label='Currency', color='#2ea64d')
        ax.plot(date_labels, total_amounts, marker='o',
                linestyle='-', label='Total')

        ax.set_xlabel('Days of the Week')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Total Amounts for Each Day of the Week')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_total = max(total_amounts, default=0)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))

        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M'
        )

        for i, v in enumerate(total_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom')

        for i, v in enumerate(gold_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#f5d45f')

        for i, v in enumerate(currency_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#2ea64d')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

    def get_total_amount_per_week(self, transactions, weeks):
        totals = np.zeros(len(weeks))
        transaction_dates = np.array(
            [datetime.date(txn._year, txn._month, txn._day)
             for txn in transactions])
        transaction_amounts = np.array(
            [txn._total_amount for txn in transactions])

        for i, (start, end) in enumerate(weeks):
            mask = (transaction_dates >= start) & (transaction_dates <= end)
            totals[i] = np.sum(transaction_amounts[mask])

        return totals.tolist()

    def create_gold_transaction_treeview(self, frame):
        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type", "Total Amount (VND)"
        ), show="headings", height=4)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Unit Price (VND/tael)",
                         text="Unit Price (VND/tael)", anchor="w")
        treeview.heading("Quantity (tael)", text="Quantity (tael)", anchor="w")
        treeview.heading("Gold Type", text="Gold Type", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")

        treeview.column("Transaction Code", width=100)
        treeview.column("Transaction Date", width=100)
        treeview.column("Unit Price (VND/tael)", width=100)
        treeview.column("Quantity (tael)", width=100)
        treeview.column("Gold Type", width=100)
        treeview.column("Total Amount (VND)", width=100)

        return treeview

    def create_currency_transaction_treeview(self, frame):
        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)", "Total Amount (VND)"
        ), show="headings", height=4)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Quantity", text="Quantity", anchor="w")
        treeview.heading("Currency Type", text="Currency Type", anchor="w")
        treeview.heading("Exchange Rate (VND)",
                         text="Exchange Rate (VND)", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")

        treeview.column("Transaction Code", width=100)
        treeview.column("Transaction Date", width=100)
        treeview.column("Quantity", width=100)
        treeview.column("Currency Type", width=100)
        treeview.column("Exchange Rate (VND)", width=100)
        treeview.column("Total Amount (VND)", width=100)

        return treeview

    def populate_treeview_with_gold_transactions(self, treeview,
                                                 transactions):
        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_unit_price = self.format_price_number(
                    transaction._unit_price)
                formatted_total_amount = self.format_price_number(
                    transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_unit_price,
                    transaction._quantity,
                    transaction._gold_type.name,
                    formatted_total_amount
                ))

    def populate_treeview_with_currency_transactions(self, treeview,
                                                     transactions):
        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_quantity = self.format_price_number(
                    transaction._quantity)
                formatted_exchange_rate = self.format_price_number(
                    transaction._exchange_rate._rate)
                formatted_total_amount = self.format_price_number(
                    transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_quantity,
                    transaction._currency_type.name,
                    formatted_exchange_rate,
                    formatted_total_amount
                ))

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount

    def open_total_details_window(self, transactions):
        if self.total_details_window is None \
            or not self.total_details_window \
                .winfo_exists():
            self.total_details_window \
                = TotalDetailsWindow(
                    self, transactions=transactions)
            self.total_details_window.after(
                10, self.total_details_window.lift)
        else:
            self.total_details_window.focus()

    def open_statistics_details_month_window(self, transactions):
        if self.statistics_details_month_window is None \
            or not self.statistics_details_month_window \
                .winfo_exists():
            self.statistics_details_month_window \
                = StatisticsDetailsMonthWindow(
                    self, transactions=transactions)
            self.statistics_details_month_window.after(
                10, self.statistics_details_month_window.lift)
        else:
            self.statistics_details_month_window.focus()

    def open_statistics_details_week_window(self, transactions):
        if self.statistics_details_week_window is None \
            or not self.statistics_details_week_window \
                .winfo_exists():
            self.statistics_details_week_window \
                = StatisticsDetailsWeekWindow(
                    self, transactions=transactions)
            self.statistics_details_week_window.after(
                10, self.statistics_details_week_window.lift)
        else:
            self.statistics_details_week_window.focus()


class TotalDetailsWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, transactions, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Total Details")
        self.iconbitmap(default='./logo.ico')
        self.minsize(700, 600)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent
        self.transactions = transactions

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        month_total_chart = \
            self.parent.create_total_chart_frame(self,
                                                 self.transactions,
                                                 btn_details_status=False)
        month_total_chart.pack(padx=10, pady=10, fill="x")

        gold_transaction_frame = customtkinter.CTkFrame(
            self, fg_color="#f5d45f",
            border_width=2, border_color="#989DA1",
            corner_radius=5)
        gold_transaction_frame.pack(padx=10, pady=10, fill="x")

        gold_content_frame = customtkinter.CTkFrame(
            master=gold_transaction_frame, fg_color="transparent")
        gold_content_frame.pack(padx=10, pady=20, fill="x")

        gold_content_frame.columnconfigure(0, weight=0)
        gold_content_frame.columnconfigure(1, weight=1)

        gold_title_and_total_frame = customtkinter.CTkFrame(
            master=gold_content_frame, fg_color="transparent")
        gold_title_and_total_frame.grid(
            row=0, column=0, sticky="w", padx=5, pady=0)

        gold_title = customtkinter.CTkLabel(
            master=gold_title_and_total_frame,
            text="GOLD TRANSACTION",
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="w"
        )
        gold_title.pack(padx=5, pady=0, fill="x")

        total_amount_transaction = 0
        gold_total_amount_transaction = 0
        currency_total_amount_transaction = 0
        total_amount_quantity_transaction = 0
        gold_total_amount_quantity_transaction = 0
        currency_total_amount_quantity_transaction = 0
        for transaction in self.transactions:
            total_amount_transaction += transaction._total_amount
            total_amount_quantity_transaction += 1
            if isinstance(transaction, GoldTransaction):
                gold_total_amount_transaction += transaction._total_amount
                gold_total_amount_quantity_transaction += 1
            if isinstance(transaction, CurrencyTransaction):
                currency_total_amount_transaction += transaction._total_amount
                currency_total_amount_quantity_transaction += 1

        gold_total_value = customtkinter.CTkLabel(
            master=gold_title_and_total_frame,
            text=f"{gold_total_amount_quantity_transaction} transactions",
            font=("Arial", 14),
            text_color="#5B5B5B",
            anchor="w"
        )
        gold_total_value.pack(padx=5, pady=0, fill="x")

        gold_total_amount_value = customtkinter.CTkLabel(
            master=gold_content_frame,
            text=f"{self.format_price_number(gold_total_amount_transaction)}",
            font=("Arial", 20, "bold"),
            text_color="black",
        )
        gold_total_amount_value.grid(
            row=0, column=1, sticky="e", padx=5, pady=0)

        currency_transaction_frame = customtkinter.CTkFrame(
            self, fg_color="#2ea64d",
            border_width=2, border_color="#989DA1",
            corner_radius=5)
        currency_transaction_frame.pack(padx=10, pady=10, fill="x")

        currency_content_frame = customtkinter.CTkFrame(
            master=currency_transaction_frame, fg_color="transparent")
        currency_content_frame.pack(padx=10, pady=20, fill="x")

        currency_content_frame.columnconfigure(0, weight=0)
        currency_content_frame.columnconfigure(1, weight=1)

        currency_title_and_total_frame = customtkinter.CTkFrame(
            master=currency_content_frame, fg_color="transparent")
        currency_title_and_total_frame.grid(
            row=0, column=0, sticky="w", padx=5, pady=0)

        currency_title = customtkinter.CTkLabel(
            master=currency_title_and_total_frame,
            text="CURRENCY TRANSACTION",
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="w"
        )
        currency_title.pack(padx=5, pady=0, fill="x")

        currency_total_value = customtkinter.CTkLabel(
            master=currency_title_and_total_frame,
            text=f"{currency_total_amount_quantity_transaction} transactions",
            font=("Arial", 14),
            text_color="#5B5B5B",
            anchor="w"
        )
        currency_total_value.pack(padx=5, pady=0, fill="x")

        currency_total_amount_value = customtkinter.CTkLabel(
            master=currency_content_frame,
            text=f"{self.format_price_number(
                currency_total_amount_transaction)}",
            font=("Arial", 20, "bold"),
            text_color="black",
        )
        currency_total_amount_value.grid(
            row=0, column=1, sticky="e", padx=5, pady=0)

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount


class StatisticsDetailsMonthWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, transactions, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Statistics Details")
        self.iconbitmap(default='./logo.ico')
        self.minsize(1400, 900)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent
        self.transactions = transactions

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

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


class StatisticsDetailsWeekWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, transactions, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Statistics Details")
        self.iconbitmap(default='./logo.ico')
        self.minsize(1400, 900)
        self.maxsize(1400, 900)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent
        self.transactions = transactions

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

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


if __name__ == "__main__":
    app = TransactionApp()
    try:
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        app.on_closing()
