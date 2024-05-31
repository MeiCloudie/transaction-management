from tkinter import messagebox
import customtkinter
import pandas as pd

from enums.gold_type_enum import GoldType
from enums.currency_type_enum import CurrencyType
from models.gold_transaction_model import GoldTransaction
from models.exchange_rate_model import ExchangeRate
from models.currency_transaction_model import CurrencyTransaction
from models.transaction_list_model import TransactionList
from widgets.header_frame import HeaderFrame
from widgets.tab_filter import TabFilter


class TransactionApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")

        self.title("Transaction Management")
        icon_path = "./resources/images/logo.ico"
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
            df_transactions = pd.read_excel("./resources/data/data.xlsx",
                                            sheet_name="transactions")
            df_exchange_rates = pd.read_excel("./resources/data/data.xlsx",
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


if __name__ == "__main__":
    app = TransactionApp()
    try:
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        app.on_closing()
