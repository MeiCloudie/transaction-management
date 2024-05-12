import json
from tkinter import ttk, messagebox
import customtkinter
from enum import Enum
from abc import ABC, abstractmethod
from PIL import Image
import datetime
from datetime import timedelta
from sys import platform


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
    def calculate_total_amount(self):
        return self._unit_price * self._quantity


class GoldTransaction(Transaction):
    def __init__(self, id, day, month, year, unit_price, quantity, gold_type):
        super().__init__(id, day, month, year, unit_price, quantity)
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
                 currency_type, exchange_rate):
        self._currency_type = currency_type
        self._exchange_rate = exchange_rate
        super().__init__(id, day, month, year, quantity)

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


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")


class TransactionApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Transaction Management")
        icon_path = "./logo.ico"
        self.iconbitmap(icon_path)
        self.minsize(1720, 960)

        self.transaction_list = TransactionList()
        self.create_widget()

    def create_widget(self):
        self.load_data_from_json()

        self.header_frame = HeaderFrame(master=self)
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.tab_filter = TabFilter(master=self)
        self.tab_filter.grid(row=1, column=0, padx=10,
                             pady=(0, 10), sticky="ew")

        self.grid_columnconfigure(0, weight=1)

    def load_data_from_json(self):
        try:
            with open("data.json", "r") as json_file:
                data = json.load(json_file)
                transactions_data = data.get("transactions", [])
                exchange_rates_data = data.get("exchange_rates", [])

                for transaction_data in transactions_data:
                    if transaction_data["type"] == "gold":
                        transaction = GoldTransaction(
                            transaction_data["id"],
                            transaction_data["day"],
                            transaction_data["month"],
                            transaction_data["year"],
                            transaction_data["unit_price"],
                            transaction_data["quantity"],
                            GoldType(transaction_data["gold_type"])
                        )
                    elif transaction_data["type"] == "currency":
                        exchange_rate_data = transaction_data["exchange_rate"]
                        exchange_rate = ExchangeRate(
                            exchange_rate_data["id"],
                            CurrencyType(exchange_rate_data["currency_type"]),
                            exchange_rate_data["rate"],
                            exchange_rate_data["effective_day"],
                            exchange_rate_data["effective_month"],
                            exchange_rate_data["effective_year"]
                        )
                        transaction = CurrencyTransaction(
                            transaction_data["id"],
                            transaction_data["day"],
                            transaction_data["month"],
                            transaction_data["year"],
                            transaction_data["quantity"],
                            CurrencyType(transaction_data["currency_type"]),
                            exchange_rate
                        )
                    else:
                        continue

                    self.transaction_list.add_transaction(transaction)

                for exchange_rate_data in exchange_rates_data:
                    _ = ExchangeRate(
                        exchange_rate_data["id"],
                        CurrencyType(exchange_rate_data["currency_type"]),
                        exchange_rate_data["rate"],
                        exchange_rate_data["effective_day"],
                        exchange_rate_data["effective_month"],
                        exchange_rate_data["effective_year"]
                    )

        except FileNotFoundError:
            messagebox.showerror("Error", "Data file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in data file.")


class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
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
            hover_color="light blue")
        self.btn_report.pack(side="right", padx=5, pady=5)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

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
        self.show_frame(self.date_frame)
        self.hide_frame(self.category_frame)

    def show_default_frame_sort_by(self):
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
        treeview_gold_transaction = \
            self.create_gold_transaction_treeview_by_date(frame)
        self.populate_treeview_with_gold_transactions_by_date(
            treeview_gold_transaction, transactions, day, month, year)
        treeview_gold_transaction.pack(padx=10, pady=10, fill="x")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=10, pady=10, fill="x")

        treeview_currency_transaction \
            = self.create_currency_transaction_treeview_by_date(frame)
        self.populate_treeview_with_currency_transactions_by_date(
            treeview_currency_transaction, transactions, day, month, year)
        treeview_currency_transaction.pack(padx=10, pady=10, fill="x")

    def create_gold_transaction_treeview_by_date(self, frame):
        gold_transaction_label = customtkinter.CTkLabel(
            frame, text="GOLD TRANSACTIONS", text_color="black",
            font=("Arial", 16, "bold"))
        gold_transaction_label.pack(
            padx=10, pady=(5, 0), side="top", anchor="w")

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
        currency_transaction_label = customtkinter.CTkLabel(
            frame, text="CURRENCY TRANSACTIONS", text_color="black",
            font=("Arial", 16, "bold"))
        currency_transaction_label.pack(
            padx=10, pady=(5, 0), side="top", anchor="w")

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
            elif isinstance(transactions[0], CurrencyTransaction):
                treeview_transaction \
                    = self.create_currency_tv_sort_by_total_amount(
                        frame_items, transactions)
                self.populate_tv_with_currency_sort_by_total_amount(
                    treeview_transaction, transactions)

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
                values for date fields.")
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
        self.configure(fg_color="#d9d9d9")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap("./logo.ico"))

    def create_widget(self):
        self.add_transaction_tab_views = AddTransactionTabView(master=self)
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

        entry_unit_price = customtkinter.CTkEntry(
            master=tab, placeholder_text="Ex: 85.200.000")
        entry_unit_price.pack(padx=20, pady=0, anchor="w", fill="x")

        label_quantity = customtkinter.CTkLabel(
            master=tab,
            text="Quantity (tael):",
            font=("Arial", 14),
            text_color="black",
        )
        label_quantity.pack(padx=20, pady=5, anchor="w")

        entry_quantity = customtkinter.CTkEntry(
            master=tab, placeholder_text="Ex: 10")
        entry_quantity.pack(padx=20, pady=0, anchor="w", fill="x")

        label_gold_type = customtkinter.CTkLabel(
            master=tab,
            text="Gold Type:",
            font=("Arial", 14),
            text_color="black",
        )
        label_gold_type.pack(padx=20, pady=5, anchor="w")

        combobox_gold_type = customtkinter.CTkComboBox(tab, values=[
            "SJC", "PNJ", "DOJI"
        ],
            command=self.combobox_gold_type_callback)
        combobox_gold_type.set("SJC")
        combobox_gold_type.pack(padx=20, pady=0, anchor="w", fill="x")

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

        entry_day = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Day", width=95)
        entry_day.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        separator_day_month = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_day_month.grid(row=0, column=1,
                                 padx=1, pady=0, sticky="ew")

        _entry_month = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Month", width=95)
        _entry_month.grid(row=0, column=2, padx=5, pady=0)

        separator_month_year = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_month_year.grid(
            row=0, column=3, padx=1, pady=0, sticky="ew")

        entry_year = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Year", width=95)
        entry_year.grid(row=0, column=4, padx=(5, 0), pady=0)

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
            command=self.gold_cancel_button_callback)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=5)

    def combobox_gold_type_callback(self, choice):
        print("combobox_gold_type dropdown clicked:", choice)

    def gold_confirm_button_callback(self):
        print("gold_confirm_button_callback")

    def gold_cancel_button_callback(self):
        print("gold_cancel_button_callback")

    def create_tab_add_currency_transaction(self, tab):
        label_quantity = customtkinter.CTkLabel(
            master=tab,
            text="Quantity:",
            font=("Arial", 14),
            text_color="black",
        )
        label_quantity.pack(padx=20, pady=5, anchor="w")

        entry_quantity = customtkinter.CTkEntry(
            master=tab, placeholder_text="Ex: 50")
        entry_quantity.pack(padx=20, pady=0, anchor="w", fill="x")

        label_currency_type = customtkinter.CTkLabel(
            master=tab,
            text="Currency Type:",
            font=("Arial", 14),
            text_color="black",
        )
        label_currency_type.pack(padx=20, pady=5, anchor="w")

        combobox_currency_type = customtkinter.CTkComboBox(tab, values=[
            "VND", "USD", "EUR"
        ],
            command=self.combobox_currency_type_callback)
        combobox_currency_type.set("VND")
        combobox_currency_type.pack(padx=20, pady=0, anchor="w", fill="x")

        label_exchange_rate = customtkinter.CTkLabel(
            master=tab,
            text="Exchange Rate (VND):",
            font=("Arial", 14),
            text_color="black",
        )
        label_exchange_rate.pack(padx=20, pady=5, anchor="w")

        entry_exchange_rate = customtkinter.CTkEntry(
            master=tab, placeholder_text="Ex: 23.130")
        entry_exchange_rate.pack(padx=20, pady=0, anchor="w", fill="x")

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

        entry_day = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Day", width=95)
        entry_day.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        separator_day_month = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_day_month.grid(row=0, column=1,
                                 padx=1, pady=0, sticky="ew")

        _entry_month = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Month", width=95)
        _entry_month.grid(row=0, column=2, padx=5, pady=0)

        separator_month_year = ttk.Separator(
            date_frame, orient="horizontal", style="Separator.TSeparator")
        separator_month_year.grid(
            row=0, column=3, padx=1, pady=0, sticky="ew")

        entry_year = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Year", width=95)
        entry_year.grid(row=0, column=4, padx=(5, 0), pady=0)

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
            command=self.currency_cancel_button_callback)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=5)

    def combobox_currency_type_callback(self, choice):
        print("combobox_currency_type dropdown clicked:", choice)

    def currency_confirm_button_callback(self):
        print("currency_confirm_button_callback")

    def currency_cancel_button_callback(self):
        print("currency_cancel_button_callback")


if __name__ == "__main__":
    app = TransactionApp()
    app.mainloop()
