import tkinter
from tkinter import ttk, messagebox
import customtkinter
from sys import platform
import datetime
import pandas as pd

from enums.currency_type_enum import CurrencyType


class EditCurrencyTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Edit Transaction")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent

        self.load_exchange_rates_from_excel()
        self.create_widget()

        if platform.startswith("win"):
            self.after(200,
                       lambda: self.iconbitmap("./resources/images/logo.ico"))

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

            transaction_found = False
            for idx, transaction in df_transactions.iterrows():
                if transaction[
                        "id"
                ] == self.parent.selected_currency_transaction_code:
                    df_transactions.at[idx, "day"] = day
                    df_transactions.at[idx, "month"] = month
                    df_transactions.at[idx, "year"] = year
                    df_transactions.at[idx, "quantity"] = quantity
                    df_transactions.at[idx,
                                       "currency_type"] = currency_type_enum
                    df_transactions.at[idx,
                                       "exchange_rate_id"] = exchange_rate_id
                    df_transactions.at[idx, "exchange_rate"] = exchange_rate
                    df_transactions.at[idx,
                                       "effective_day"
                                       ] = exchange_rate_row["effective_day"]
                    df_transactions.at[idx,
                                       "effective_month"
                                       ] = exchange_rate_row["effective_month"]
                    df_transactions.at[idx,
                                       "effective_year"
                                       ] = exchange_rate_row["effective_year"]
                    transaction_found = True
                    break

            if not transaction_found:
                messagebox.showerror("Error", "Transaction ID not found.")
                return

            with pd.ExcelWriter("./resources/data/data.xlsx",
                                engine="openpyxl", mode="a",
                                if_sheet_exists="replace") as writer:
                df_transactions.to_excel(
                    writer, sheet_name="transactions", index=False)
                df_exchange_rates.to_excel(
                    writer, sheet_name="exchange_rates", index=False)

            messagebox.showinfo(
                "Success",
                "Currency transaction updated successfully! \
                \nPlease Refresh Data!")
            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while writing to Excel: {e}")
            self.focus()

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
