from tkinter import ttk, messagebox
import customtkinter
from sys import platform
import datetime

from enums.month_label_enum import MonthLabel
from models.gold_transaction_model import GoldTransaction
from models.currency_transaction_model import CurrencyTransaction
from widgets.header_frame_for_window import HeaderFrameForWindow


class SearchWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Transaction Management - SEARCH")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(1720, 960)
        self.configure(fg_color="white")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(
                "./resources/images/logo.ico"))

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
