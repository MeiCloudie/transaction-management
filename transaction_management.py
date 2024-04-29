import json
from tkinter import ttk, messagebox
import customtkinter
import os
from enum import Enum


class CurrencyType(Enum):
    VND = 0
    USD = 1
    EUR = 2


class TransactionApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Transaction Management")
        self._set_appearance_mode("light")
        icon_path = os.path.abspath("./logo.ico")
        self.iconbitmap(icon_path)

        self.transaction_list = TransactionList()
        self.create_widgets()
        self.load_data_from_json()

    def create_widgets(self):
        # Tạo bảng TreeView cho giao dịch vàng
        self.gold_transaction_treeview = ttk.Treeview(
            self, columns=(
                "ID", "Day", "Month", "Year",
                "Unit Price", "Quantity", "Gold Type", "Total Amount"
            ), show="headings")
        self.gold_transaction_treeview.heading("ID", text="ID")
        self.gold_transaction_treeview.heading("Day", text="Day")
        self.gold_transaction_treeview.heading("Month", text="Month")
        self.gold_transaction_treeview.heading("Year", text="Year")
        self.gold_transaction_treeview.heading("Unit Price", text="Unit Price")
        self.gold_transaction_treeview.heading("Quantity", text="Quantity")
        self.gold_transaction_treeview.heading("Gold Type", text="Gold Type")
        self.gold_transaction_treeview.heading(
            "Total Amount", text="Total Amount")
        self.gold_transaction_treeview.pack(padx=10, pady=10)

        # Tạo bảng TreeView cho giao dịch tiền tệ
        self.currency_transaction_treeview = ttk.Treeview(self, columns=(
            "ID", "Day", "Month", "Year", "Unit Price", "Quantity",
            "Currency Type", "Exchange Rate", "Total Amount"), show="headings")
        self.currency_transaction_treeview.heading("#0", text="STT")
        self.currency_transaction_treeview.heading("ID", text="ID")
        self.currency_transaction_treeview.heading("Day", text="Day")
        self.currency_transaction_treeview.heading("Month", text="Month")
        self.currency_transaction_treeview.heading("Year", text="Year")
        self.currency_transaction_treeview.heading(
            "Unit Price", text="Unit Price")
        self.currency_transaction_treeview.heading("Quantity", text="Quantity")
        self.currency_transaction_treeview.heading(
            "Currency Type", text="Currency Type")
        self.currency_transaction_treeview.heading(
            "Exchange Rate", text="Exchange Rate")
        self.currency_transaction_treeview.heading(
            "Total Amount", text="Total Amount")
        self.currency_transaction_treeview.pack(padx=10, pady=10)

        # Tạo label cho tổng số giao dịch và tổng số tiền
        self.total_label = ttk.Label(
            self,
            text="Total Gold Transactions: 0 | "
            "Total Currency Transactions: 0 | "
            "Total Gold Amount: 0.0 | "
            "Total Currency Amount: 0.0"
        )
        self.total_label.pack(pady=5)

    def add_transaction(self):
        pass

    def refresh_transaction_list(self):
        for row in self.gold_transaction_treeview.get_children():
            self.gold_transaction_treeview.delete(row)

        for row in self.currency_transaction_treeview.get_children():
            self.currency_transaction_treeview.delete(row)

        for transaction in self.transaction_list.get_transactions():
            if isinstance(transaction, GoldTransaction):
                transaction_data = (
                    transaction._id,
                    transaction._day,
                    transaction._month,
                    transaction._year,
                    transaction._unit_price,
                    transaction._quantity,
                    transaction._gold_type,
                    transaction.calculate_total_amount(),
                    "Gold"
                )
                self.gold_transaction_treeview.insert(
                    "", "end", values=transaction_data)
            elif isinstance(transaction, CurrencyTransaction):
                transaction_data = (
                    transaction._id,
                    transaction._day,
                    transaction._month,
                    transaction._year,
                    transaction._unit_price,
                    transaction._quantity,
                    transaction._currency_type.name,
                    transaction._exchange_rate._rate,
                    transaction.cal_total_amount(),
                    "Currency"
                )
                self.currency_transaction_treeview.insert(
                    "", "end", values=transaction_data)
            else:
                continue

        self.update_total_label()

    def update_total_label(self):
        total_label_content = (
            f"Total Gold Transactions: {
                self.transaction_list._total_gold_transactions} | "
            f"Total Currency Transactions: {
                self.transaction_list._total_currency_transactions} | "
            f"Total Gold Amount: {self.transaction_list._total_gold_amount} | "
            f"Total Currency Amount: {
                self.transaction_list._total_currency_amount}"
        )
        self.total_label.config(text=total_label_content)

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
                            transaction_data["gold_type"]
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
                            transaction_data["unit_price"],
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

        self.refresh_transaction_list()


class Transaction:
    def __init__(self, id, day, month, year, unit_price, quantity):
        self._id = id
        self._day = day
        self._month = month
        self._year = year
        self._unit_price = unit_price
        self._quantity = quantity
        self._total_amount = self.calculate_total_amount()

    def calculate_total_amount(self):
        return self._unit_price * self._quantity


class GoldTransaction(Transaction):
    def __init__(self, id, day, month, year, unit_price, quantity, gold_type):
        super().__init__(id, day, month, year, unit_price, quantity)
        self._gold_type = gold_type
        self._total_amount = self.calculate_total_amount()

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
    def __init__(self, id, day, month, year, unit_price, quantity,
                 currency_type, exchange_rate):
        super().__init__(id, day, month, year, unit_price, quantity)
        self._currency_type = currency_type
        self._exchange_rate = exchange_rate
        self._total_amount = self.cal_total_amount()

    def cal_total_amount(self):
        if self._currency_type == CurrencyType.VND:
            return self._unit_price * self._quantity
        elif self._currency_type == CurrencyType.USD \
                or self._currency_type == CurrencyType.EUR:
            return self._unit_price * self._quantity \
                * self._exchange_rate._rate
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


if __name__ == "__main__":
    app = TransactionApp()
    app.mainloop()
