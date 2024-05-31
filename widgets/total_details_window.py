import customtkinter
from sys import platform

from models.gold_transaction_model import GoldTransaction
from models.currency_transaction_model import CurrencyTransaction


class TotalDetailsWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, transactions, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Total Details")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(700, 600)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent
        self.transactions = transactions

        self.create_widget()

        if platform.startswith("win"):
            self.after(200,
                       lambda: self.iconbitmap("./resources/images/logo.ico"))

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
