from tkinter import ttk
import customtkinter
from sys import platform


class ViewDetailsCurrencyTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("View Details Transaction")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")
        self.parent = parent

        self.create_widget()

        if platform.startswith("win"):
            self.after(200,
                       lambda: self.iconbitmap("./resources/images/logo.ico"))

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
