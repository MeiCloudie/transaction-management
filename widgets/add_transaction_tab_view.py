from tkinter import ttk, messagebox
import customtkinter
import datetime
import pandas as pd

from enums.gold_type_enum import GoldType
from enums.currency_type_enum import CurrencyType


class AddTransactionTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff", bg_color="#d9d9d9",
                       border_width=2, border_color="#989DA1")

        self.tab_add_gold_transaction = self.add("GOLD")
        self.tab_add_currency_transaction = self.add("CURRENCY")

        self.set("GOLD")
        self.configure(corner_radius=5)

        self.load_exchange_rates_from_excel()

        self.create_widgets()

    def load_exchange_rates_from_excel(self):
        try:
            df_exchange_rates = pd.read_excel(
                "./resources/data/data.xlsx", sheet_name="exchange_rates")
            self.exchange_rates = df_exchange_rates.to_dict('records')
        except FileNotFoundError:
            messagebox.showerror("Error", "Data file not found.")
            self.exchange_rates = []
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.exchange_rates = []

    def create_widgets(self):
        self.create_tab_add_gold_transaction(self.tab_add_gold_transaction)
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
        separator_day_month.grid(row=0, column=1, padx=0, pady=0, sticky="ew")

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

        self.currency_combobox_currency_type = customtkinter.CTkComboBox(
            tab, values=["VND", "USD", "EUR"],
            command=self.combobox_currency_type_callback)
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
        self.currency_entry_exchange_rate.pack(padx=20, pady=0,
                                               anchor="w", fill="x")
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
        self.currency_entry_day.grid(row=0, column=0, padx=(0, 5),
                                     pady=0, sticky="ew")

        separator_day_month = ttk.Separator(date_frame, orient="horizontal",
                                            style="Separator.TSeparator")
        separator_day_month.grid(row=0, column=1, padx=0, pady=0, sticky="ew")

        self.currency_entry_month = customtkinter.CTkEntry(
            master=date_frame, placeholder_text="Month", width=95)
        self.currency_entry_month.grid(row=0, column=2, padx=5, pady=0)

        separator_month_year = ttk.Separator(date_frame, orient="horizontal",
                                             style="Separator.TSeparator")
        separator_month_year.grid(row=0, column=3, padx=0, pady=0, sticky="ew")

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

    def gold_confirm_button_callback(self):
        unit_price = self.gold_entry_unit_price.get()
        quantity = self.gold_entry_quantity.get()
        day_submit = self.gold_entry_day.get()
        month_submit = self.gold_entry_month.get()
        year_submit = self.gold_entry_year.get()
        gold_type = self.gold_combobox_gold_type.get()

        if not all([unit_price, quantity, day_submit, month_submit,
                    year_submit, gold_type]):
            messagebox.showerror("Missing Input", "Please fill in all fields.")
            self.focus()
            return

        unit_price = self.validate_and_convert_input(unit_price)
        if unit_price is None:
            messagebox.showerror("Invalid Unit Price",
                                 "Unit Price must be a valid number.")
            self.focus()
            return

        quantity = self.validate_and_convert_input(quantity)
        if quantity is None:
            messagebox.showerror("Invalid Quantity",
                                 "Quantity must be a valid number.")
            self.focus()
            return

        if not all(map(str.isdigit, [day_submit, month_submit, year_submit])):
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numerical values for date fields.")
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

        try:
            new_data = {
                "id": self.generate_gold_id(
                    pd.read_excel("./resources/data/data.xlsx",
                                  sheet_name="transactions")),
                "day": day,
                "month": month,
                "year": year,
                "unit_price": unit_price,
                "quantity": quantity,
                "type": "gold",
                "gold_type": GoldType[gold_type].value,
                "isdeleted": False
            }
            self.append_to_excel(new_data, "transactions")

            messagebox.showinfo(
                "Success",
                "Gold transaction added successfully. Please Refresh Data!")
            self.focus()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred while writing to Excel: {e}")
            self.focus()

    def generate_gold_id(self, df_transactions):
        gold_transactions = df_transactions[df_transactions["type"] == "gold"]
        num_gold_transactions = len(gold_transactions)
        new_id = f"GLD{num_gold_transactions + 1:03}"
        while new_id in df_transactions["id"].values:
            num_gold_transactions += 1
            new_id = f"GLD{num_gold_transactions + 1:03}"
        return new_id

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
        day_submit = self.currency_entry_day.get()
        month_submit = self.currency_entry_month.get()
        year_submit = self.currency_entry_year.get()
        currency_type = self.currency_combobox_currency_type.get()

        if not all([quantity, day_submit, month_submit,
                    year_submit, currency_type]):
            messagebox.showerror("Missing Input", "Please fill in all fields.")
            self.focus()
            return

        quantity = self.validate_and_convert_input(quantity)
        if quantity is None:
            messagebox.showerror("Invalid Quantity",
                                 "Quantity must be a valid number.")
            self.focus()
            return

        if not all(map(str.isdigit, [day_submit, month_submit, year_submit])):
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numerical values for date fields.")
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
            messagebox.showerror(
                "Invalid Currency Type",
                "Currency Type must be 'VND', 'USD', or 'EUR'.")
            self.focus()
            return

        try:
            df_transactions = pd.read_excel(
                "./resources/data/data.xlsx", sheet_name="transactions")
            df_exchange_rates = pd.read_excel(
                "./resources/data/data.xlsx", sheet_name="exchange_rates")

            currency_type_enum = CurrencyType[currency_type].value
            exchange_rate_row = df_exchange_rates[
                df_exchange_rates["currency_type"] ==
                currency_type_enum].iloc[0]
            exchange_rate = exchange_rate_row["rate"]
            exchange_rate_id = exchange_rate_row["id"]

            new_data = {
                "id": self.generate_currency_id(df_transactions),
                "day": day,
                "month": month,
                "year": year,
                "quantity": quantity,
                "type": "currency",
                "currency_type": currency_type_enum,
                "exchange_rate_id": exchange_rate_id,
                "exchange_rate": exchange_rate,
                "effective_day": exchange_rate_row["effective_day"],
                "effective_month": exchange_rate_row["effective_month"],
                "effective_year": exchange_rate_row["effective_year"],
                "isdeleted": False
            }

            self.append_to_excel(new_data, "transactions")

            messagebox.showinfo(
                "Success",
                "Currency transaction added successfully. Please Refresh Data!"
            )
            self.focus()
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while writing to Excel: {e}")
            self.focus()

    def generate_currency_id(self, df_transactions):
        currency_transactions = df_transactions[
            df_transactions["type"] == "currency"]
        num_currency_transactions = len(currency_transactions)
        new_id = f"CUR{num_currency_transactions + 1:03}"
        while new_id in df_transactions["id"].values:
            num_currency_transactions += 1
            new_id = f"CUR{num_currency_transactions + 1:03}"
        return new_id

    def append_to_excel(self, new_data, sheet_name):
        try:
            df_transactions = pd.read_excel(
                "./resources/data/data.xlsx", sheet_name="transactions")
            df_exchange_rates = pd.read_excel(
                "./resources/data/data.xlsx", sheet_name="exchange_rates")

            if sheet_name == "transactions":
                df_transactions = pd.concat(
                    [df_transactions, pd.DataFrame([new_data])],
                    ignore_index=True)
            elif sheet_name == "exchange_rates":
                df_exchange_rates = pd.concat(
                    [df_exchange_rates, pd.DataFrame([new_data])],
                    ignore_index=True)

            with pd.ExcelWriter("./resources/data/data.xlsx",
                                engine="openpyxl", mode="a",
                                if_sheet_exists="replace") as writer:
                df_transactions.to_excel(
                    writer, sheet_name="transactions", index=False)
                df_exchange_rates.to_excel(
                    writer, sheet_name="exchange_rates", index=False)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while writing to Excel: {e}")

    def get_exchange_rate_id(self, currency_type):
        for rate in self.exchange_rates:
            if rate["currency_type"] == CurrencyType[currency_type].value:
                return rate["id"]
        return None

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
