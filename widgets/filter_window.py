from tkinter import ttk, messagebox
import customtkinter
from sys import platform
import datetime
from datetime import timedelta

from enums.month_label_enum import MonthLabel
from models.gold_transaction_model import GoldTransaction
from models.currency_transaction_model import CurrencyTransaction
from widgets.header_frame_for_window import HeaderFrameForWindow


class FilterWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Transaction Management - FILTER")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(1720, 960)
        self.configure(fg_color="white")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200,
                       lambda: self.iconbitmap("./resources/images/logo.ico"))

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
