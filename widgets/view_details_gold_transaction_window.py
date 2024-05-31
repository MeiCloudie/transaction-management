from tkinter import ttk
import customtkinter
from sys import platform


class ViewDetailsGoldTransactionWindow(customtkinter.CTkToplevel):
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
