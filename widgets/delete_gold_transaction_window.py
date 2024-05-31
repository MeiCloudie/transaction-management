from tkinter import ttk, messagebox
import customtkinter
from sys import platform
import pandas as pd


class DeleteGoldTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Delete Transaction")
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
        delete_frame = customtkinter.CTkFrame(
            master=self, fg_color="#ffffff", border_width=2,
            border_color="#5B5B5B")
        delete_frame.pack(padx=20, pady=20, fill="both")

        gold_transaction_label = customtkinter.CTkLabel(
            delete_frame, text="GOLD TRANSACTION",
            font=("Arial", 20, "bold")
        )
        gold_transaction_label.pack(padx=20, pady=(20, 0), anchor="w")

        gold_transaction_code = customtkinter.CTkLabel(
            delete_frame, text=f"Code: {
                self.parent.selected_gold_transaction_code}"
        )
        gold_transaction_code.pack(padx=20, pady=(0, 5), anchor="w")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            delete_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=20, pady=(0, 10), fill="x")

        gold_unit_price_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
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
            delete_frame, fg_color="transparent")
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
            delete_frame, fg_color="transparent")
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
            delete_frame, fg_color="transparent")
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
            delete_frame, fg_color="transparent")
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

        buttons_frame = customtkinter.CTkFrame(
            delete_frame, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=(100, 5), anchor="w", fill="x")

        button_confirm = customtkinter.CTkButton(
            buttons_frame,
            text="CONFIRM",
            width=150,
            command=self.gold_confirm_button_callback)
        button_confirm.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)

        button_cancel = customtkinter.CTkButton(
            buttons_frame,
            text="CANCEL",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.destroy)
        button_cancel.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

    def gold_confirm_button_callback(self):
        try:
            df_transactions = pd.read_excel(
                "./resources/data/data.xlsx", sheet_name="transactions")
            df_exchange_rates = pd.read_excel(
                "./resources/data/data.xlsx", sheet_name="exchange_rates")

            transaction_found = False
            for idx, transaction in df_transactions.iterrows():
                if transaction[
                    "id"
                ] == self.parent.selected_gold_transaction_code:
                    df_transactions.at[idx, "isdeleted"] = True
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
                "Gold transaction deleted successfully! Please Refresh Data!")
            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while writing to Excel: {e}")
            self.focus()
