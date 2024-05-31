from tkinter import ttk, messagebox
import customtkinter
from PIL import Image
import datetime

from enum import Enum
from enums.month_label_enum import MonthLabel
from models.gold_transaction_model import GoldTransaction
from models.currency_transaction_model import CurrencyTransaction
from widgets.view_details_gold_transaction_window \
    import ViewDetailsGoldTransactionWindow
from widgets.view_details_currency_transaction_window \
    import ViewDetailsCurrencyTransactionWindow
from widgets.edit_gold_transaction_window \
    import EditGoldTransactionWindow
from widgets.edit_currency_transaction_window \
    import EditCurrencyTransactionWindow
from widgets.delete_gold_transaction_window \
    import DeleteGoldTransactionWindow
from widgets.delete_currency_transaction_window \
    import DeleteCurrencyTransactionWindow


class TabGroupBySortByType(Enum):
    GROUPBYDATE = 0
    GROUPBYCATEGORY = 1
    SORTBYDATE = 2
    SORTBYTOTALAMOUNT = 3


class TabGroupBySortBy(customtkinter.CTkTabview):
    def __init__(self, master, transactions, **kwargs):
        super().__init__(master, **kwargs)
        self.transactions = transactions
        self.configure(fg_color="#dbdbdb", bg_color="#ffffff")

        self.tab_group_by = self.add("GROUP BY")
        self.tab_sort_by = self.add("SORT BY")

        self.set("GROUP BY")
        self.configure(corner_radius=5)

        self.option_segmented_button_date = True
        self.option_segmented_button_total_amount = True

        self.gold_treeviews = {}
        self.currency_treeviews = {}

        self.items_per_page = 10
        self.current_page = 0
        self.total_pages = (len(self.transactions) +
                            self.items_per_page - 1) // self.items_per_page

        self.sort_by_current_page = 0
        self.sort_by_total_pages = 1
        self.sort_by_option = "Date"
        self.sort_by_order = "Descending"

        self.pagination_frame = None
        self.pagination_frame_for_sort_by = None

        self.create_tab_group_by_sort_by_widgets()

    def create_tab_group_by_sort_by_widgets(self):
        # Group By
        self.create_option_menu_group_by()

        self.date_frame = self.create_date_group_by_frame(
            self.tab_group_by,
            self.get_paginated_transactions_by_date())
        self.category_frame = self.create_category_group_by_frame(
            self.tab_group_by, self.transactions)

        self.category_frame.pack_forget()

        self.show_default_frame_group_by()

        # Sort By
        self.buttons_frame = customtkinter.CTkFrame(self.tab_sort_by)
        self.buttons_frame.pack(padx=10, pady=5, fill="x")
        self.buttons_frame.configure(fg_color="transparent")
        self.create_option_menu_sort_by(self.buttons_frame)
        self.create_segmented_button_sort_by(self.buttons_frame)
        self.grid_columnconfigure(0, weight=1)

        self.sort_by_total_pages = (
            len(self.transactions) + self.items_per_page - 1
        ) // self.items_per_page

        self.date_sort_by_frame = self.create_date_sort_by_frame(
            self.tab_sort_by, self.get_paginated_transactions_sort_by_date(),
            option=self.option_segmented_button_date)
        self.total_amount_sort_by_frame = \
            self.create_total_amount_sort_by_frame(
                self.tab_sort_by,
                self.get_paginated_transactions_sort_by_total_amount(),
                option=self.option_segmented_button_total_amount)

        self.total_amount_sort_by_frame.pack_forget()

        self.show_default_frame_sort_by()

    # Paging
    def create_pagination_controls(self, parent):
        if self.pagination_frame is not None:
            self.pagination_frame.destroy()
        self.pagination_frame = \
            customtkinter.CTkFrame(parent, fg_color="#ffffff",
                                   bg_color="#dbdbdb")
        self.pagination_frame.pack(padx=20, pady=5, fill="x")

        previous_button = customtkinter.CTkButton(
            self.pagination_frame, text="Previous", command=self.previous_page)
        previous_button.pack(side="left", padx=(0, 5))

        next_button = customtkinter.CTkButton(
            self.pagination_frame, text="Next", command=self.next_page)
        next_button.pack(side="right", padx=(5, 0))

        self.pagination_label = customtkinter.CTkLabel(
            self.pagination_frame,
            text=f"Page {self.current_page + 1} of {self.total_pages}")
        self.pagination_label.pack(side="left", expand=True)

    def get_paginated_transactions_by_date(self):
        sorted_transactions_by_date = self.sort_transactions_by_date(
            self.transactions)
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        return sorted_transactions_by_date[start:end]

    def get_paginated_transactions_sort_by_date(self):
        sorted_transactions_by_date = self.sort_transactions_by_date(
            self.transactions, sort_type=self.option_segmented_button_date)
        start = self.sort_by_current_page * self.items_per_page
        end = start + self.items_per_page
        return sorted_transactions_by_date[start:end]

    def get_paginated_transactions_sort_by_total_amount(self):
        sorted_transactions_by_total_amount = \
            self.sort_transactions_by_total_amount(
                self.transactions,
                sort_type=self.option_segmented_button_total_amount)
        start = self.sort_by_current_page * self.items_per_page
        end = start + self.items_per_page
        return sorted_transactions_by_total_amount[start:end]

    def sort_transactions_by_date(self, transactions, sort_type=True):
        return sorted(transactions, key=lambda x: (x._year, x._month, x._day),
                      reverse=sort_type)

    def sort_transactions_by_total_amount(self, transactions, sort_type=True):
        return sorted(transactions, key=lambda x: x._total_amount,
                      reverse=sort_type)

    def update_page(self):
        self.date_frame.pack_forget()
        self.date_frame.destroy()

        self.date_frame = self.create_date_group_by_frame(
            self.tab_group_by,
            self.get_paginated_transactions_by_date())

        self.pagination_label.configure(
            text=f"Page {self.current_page + 1} of {self.total_pages}")

        self.show_default_frame_group_by()

    def update_sort_by_page(self):
        self.sort_by_total_pages = (
            len(self.transactions) + self.items_per_page - 1
        ) // self.items_per_page

        if self.sort_by_option == "Date":
            self.date_sort_by_frame.pack_forget()
            self.date_sort_by_frame.destroy()

            self.date_sort_by_frame = self.create_date_sort_by_frame(
                self.tab_sort_by,
                self.get_paginated_transactions_sort_by_date(),
                option=self.option_segmented_button_date)

            self.pagination_label_for_sort_by.configure(
                text=f"Page {self.sort_by_current_page + 1} of {
                    self.sort_by_total_pages}")

            self.show_default_frame_sort_by()
        elif self.sort_by_option == "Total Amount":
            self.total_amount_sort_by_frame.pack_forget()
            self.total_amount_sort_by_frame.destroy()

            self.total_amount_sort_by_frame = \
                self.create_total_amount_sort_by_frame(
                    self.tab_sort_by,
                    self.get_paginated_transactions_sort_by_total_amount(),
                    option=self.option_segmented_button_total_amount)

            self.pagination_label_for_sort_by.configure(
                text=f"Page {self.sort_by_current_page + 1} of {
                    self.sort_by_total_pages}")

            self.show_default_frame_sort_by()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def next_sort_by_page(self):
        if self.sort_by_current_page < self.sort_by_total_pages - 1:
            self.sort_by_current_page += 1
            self.update_sort_by_page()

    def previous_sort_by_page(self):
        if self.sort_by_current_page > 0:
            self.sort_by_current_page -= 1
            self.update_sort_by_page()

    # Set up Tab View
    def show_default_frame_group_by(self):
        self.gold_treeviews = {}
        self.currency_treeviews = {}
        self.show_frame(self.date_frame)
        self.hide_frame(self.category_frame)
        self.create_pagination_controls(self.tab_group_by)

    def show_default_frame_sort_by(self):
        self.gold_treeviews = {}
        self.currency_treeviews = {}
        if self.sort_by_option == "Date":
            self.show_frame(self.date_sort_by_frame)
            self.hide_frame(self.total_amount_sort_by_frame)
        elif self.sort_by_option == "Total Amount":
            self.show_frame(self.total_amount_sort_by_frame)
            self.hide_frame(self.date_sort_by_frame)
        self.create_sort_by_pagination_controls(self.tab_sort_by)

    def create_sort_by_pagination_controls(self, parent):
        if self.pagination_frame_for_sort_by is not None:
            self.pagination_frame_for_sort_by.destroy()
        self.pagination_frame_for_sort_by = \
            customtkinter.CTkFrame(parent, fg_color="#ffffff",
                                   bg_color="#dbdbdb", corner_radius=5)
        self.pagination_frame_for_sort_by.pack(padx=20, pady=5, fill="x")

        previous_button = customtkinter.CTkButton(
            self.pagination_frame_for_sort_by, text="Previous",
            command=self.previous_sort_by_page)
        previous_button.pack(side="left", padx=(0, 5))

        next_button = customtkinter.CTkButton(
            self.pagination_frame_for_sort_by, text="Next",
            command=self.next_sort_by_page)
        next_button.pack(side="right", padx=(5, 0))

        self.pagination_label_for_sort_by = customtkinter.CTkLabel(
            self.pagination_frame_for_sort_by,
            text=f"Page {self.sort_by_current_page + 1
                         } of {self.sort_by_total_pages}")
        self.pagination_label_for_sort_by.pack(side="left", expand=True)

    def create_option_menu_group_by(self):
        self.buttons_frame = customtkinter.CTkFrame(self.tab_group_by)
        self.buttons_frame.pack(padx=10, pady=5, fill="x")
        self.buttons_frame.configure(fg_color="transparent")

        self.optionmenu = customtkinter.CTkOptionMenu(
            self.buttons_frame,
            values=["Date", "Category"],
            command=self.option_menu_group_by_callback)
        self.optionmenu.set("Date")
        self.optionmenu.pack(padx=10, pady=0, side="left")

        self.grid_columnconfigure(0, weight=1)

    def create_option_menu_sort_by(self, frame):
        self.optionmenu = customtkinter.CTkOptionMenu(
            frame,
            values=["Date", "Total Amount"],
            command=self.option_menu_sort_by_callback)
        self.optionmenu.set("Date")
        self.optionmenu.pack(padx=10, pady=0, side="left")

    def create_segmented_button_sort_by(self, frame):
        self.segmented_button = customtkinter.CTkSegmentedButton(
            frame,
            values=["Descending", "Ascending"],
            command=self.segmented_button_callback
        )
        self.segmented_button.set("Descending")
        self.segmented_button.pack(padx=(5, 10), pady=0, side="left")

    def option_menu_group_by_callback(self, choice):
        if choice == "Date":
            self.show_frame(self.date_frame)
            self.hide_frame(self.category_frame)
            self.create_pagination_controls(self.tab_group_by)
        elif choice == "Category":
            self.show_frame(self.category_frame)
            self.hide_frame(self.date_frame)
            if self.pagination_frame is not None:
                self.pagination_frame.destroy()
                self.pagination_frame = None

    def option_menu_sort_by_callback(self, choice):
        self.sort_by_option = choice
        self.sort_by_current_page = 0
        self.sort_by_total_pages = (
            len(self.transactions) + self.items_per_page - 1
        ) // self.items_per_page
        self.update_sort_by_page()
        if choice == "Date":
            if self.option_segmented_button_date:
                self.segmented_button.set("Descending")
            else:
                self.segmented_button.set("Ascending")
        elif choice == "Total Amount":
            if self.option_segmented_button_total_amount:
                self.segmented_button.set("Descending")
            else:
                self.segmented_button.set("Ascending")

    def segmented_button_callback(self, selected_option):
        if self.sort_by_option == "Date":
            self.option_segmented_button_date = selected_option == "Descending"
            self.sort_by_current_page = 0
            self.update_sort_by_page()
        elif self.sort_by_option == "Total Amount":
            self.option_segmented_button_total_amount = \
                selected_option == "Descending"
            self.sort_by_current_page = 0
            self.update_sort_by_page()

    # Group By Frame
    def create_date_group_by_frame(self, parent, transactions):
        frame = customtkinter.CTkScrollableFrame(
            parent, fg_color="transparent",
            height=530)

        self.get_date_in_transactions(frame, transactions)

        return frame

    def create_category_group_by_frame(self, parent, transactions):
        frame = customtkinter.CTkScrollableFrame(
            parent, fg_color="transparent",
            height=530)

        self.create_content_treeview_by_category(
            frame, transactions)

        return frame

    # Group By Date
    def get_date_in_transactions(self, parent, transactions):
        unique_dates = set()

        for transaction in transactions:
            day = transaction._day
            month = MonthLabel(transaction._month)
            year = transaction._year

            date_object = datetime.date(year, month.value, day)

            unique_dates.add(date_object)

        sorted_dates = sorted(unique_dates, reverse=True)

        for date_obj in sorted_dates:
            day = date_obj.day
            month = MonthLabel(date_obj.month)
            year = date_obj.year

            group_by_date_items_frame = self.create_group_by_date_items_frame(
                parent, day, month, year, transactions=transactions)
            group_by_date_items_frame.pack(padx=5, pady=(5, 10), fill="x")

    def create_group_by_date_items_frame(self, parent, day, month, year,
                                         transactions):
        frame = customtkinter.CTkFrame(
            parent, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")

        frame_date = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_date.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=5)

        day_label = customtkinter.CTkLabel(
            frame_date, text=str(day), text_color="black",
            font=("Arial", 55, "bold"))
        day_label.pack(padx=5, pady=0, side="left")

        frame_month_year = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_month_year.grid(row=0, column=1, sticky="e", padx=0, pady=0)

        month_label = customtkinter.CTkLabel(
            frame_month_year, text=str(month), text_color="black",
            font=("Arial", 14))
        month_label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

        year_label = customtkinter.CTkLabel(
            frame_month_year, text=str(year), text_color="black",
            font=("Arial", 14))
        year_label.grid(row=1, column=0, padx=5, pady=0, sticky="w")

        frame_total_amount = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_total_amount.grid(row=0, column=2, sticky="e", padx=10, pady=5)

        total_amount_label = customtkinter.CTkLabel(
            frame_total_amount, text="Total Amount (VND)", text_color="black",
            font=("Arial", 14))
        total_amount_label.grid(row=0, column=0, padx=5, pady=0, sticky="e")

        total_amount_number_label = customtkinter.CTkLabel(
            frame_total_amount, text="", text_color="black",
            font=("Arial", 20, "bold"))
        total_amount_number_label.grid(
            row=1, column=0, padx=5, pady=0, sticky="e")

        total_amount = self.calculate_total_amount_by_date(
            transactions, day, month, year)
        formatted_total_amount = self.format_price_number(
            total_amount)
        total_amount_number_label.configure(text=str(formatted_total_amount))

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=3,
                       sticky="ew", padx=10, pady=5)

        frame_treeviews = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_treeviews.grid(row=2, column=0, padx=5,
                             pady=5, sticky="ew", columnspan=3)

        self.create_content_treeview_by_date(
            frame_treeviews, transactions, day, month, year)

        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)

        return frame

    def calculate_total_amount_by_date(self, transactions, day, month, year):
        total_amount = 0
        for transaction in transactions:
            if (transaction._day, MonthLabel(transaction._month),
                    transaction._year) == (day, month, year):
                total_amount += transaction._total_amount
        return total_amount

    def create_content_treeview_by_date(self, frame, transactions,
                                        day, month, year):
        self.selected_gold_status = False
        self.selected_currency_status = False

        if (day, month, year) not in self.gold_treeviews:
            gold_treeview = \
                self.create_gold_transaction_treeview_by_date(frame)
            self.populate_treeview_with_gold_transactions_by_date(
                gold_treeview, transactions, day, month, year)
            gold_treeview.pack(padx=10, pady=10, fill="x")
            self.gold_treeviews[(day, month, year)] = gold_treeview
        else:
            gold_treeview = self.gold_treeviews[(day, month, year)]

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=10, pady=10, fill="x")

        if (day, month, year) not in self.currency_treeviews:
            currency_treeview = \
                self.create_currency_transaction_treeview_by_date(
                    frame)
            self.populate_treeview_with_currency_transactions_by_date(
                currency_treeview, transactions, day, month, year)
            currency_treeview.pack(padx=10, pady=10, fill="x")
            self.currency_treeviews[(day, month, year)] = currency_treeview
        else:
            currency_treeview = self.currency_treeviews[(day, month, year)]

        gold_treeview.bind('<<TreeviewSelect>>', lambda event:
                           self.on_gold_treeview_select(
                               event,
                               tab_type=TabGroupBySortByType.GROUPBYDATE,
                               transactions=transactions))
        currency_treeview.bind('<<TreeviewSelect>>',
                               lambda event: self.on_currency_treeview_select(
                                   event,
                                   tab_type=TabGroupBySortByType.GROUPBYDATE,
                                   transactions=transactions))

    def create_gold_transaction_treeview_by_date(self, frame):
        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        gold_transaction_label = customtkinter.CTkLabel(
            frame_label_actions, text="GOLD TRANSACTIONS", text_color="black",
            font=("Arial", 16, "bold"))
        gold_transaction_label.grid(row=0, column=0, padx=0, pady=0,
                                    sticky="w")
        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=0, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./resources/images/details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./resources/images/edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./resources/images/delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_gold_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_gold_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_gold_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_gold_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_gold_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_gold_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            # "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type", "Total Amount (VND)"
        ), show="headings", height=5)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        # treeview.heading("Transaction Date",
        #                  text="Transaction Date", anchor="w")
        treeview.heading("Unit Price (VND/tael)",
                         text="Unit Price (VND/tael)", anchor="w")
        treeview.heading("Quantity (tael)", text="Quantity (tael)", anchor="w")
        treeview.heading("Gold Type", text="Gold Type", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")

        return treeview

    def create_currency_transaction_treeview_by_date(self, frame):
        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        currency_transaction_label = customtkinter.CTkLabel(
            frame_label_actions, text="CURRENCY TRANSACTIONS",
            text_color="black",
            font=("Arial", 16, "bold"))
        currency_transaction_label.grid(row=0, column=0, padx=0, pady=0,
                                        sticky="w")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=0, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./resources/images/details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./resources/images/edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./resources/images/delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_currency_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_currency_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_currency_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_currency_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_currency_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_currency_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            # "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)", "Total Amount (VND)"
        ), show="headings", height=5)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        # treeview.heading("Transaction Date",
        #                  text="Transaction Date", anchor="w")
        treeview.heading("Quantity", text="Quantity", anchor="w")
        treeview.heading("Currency Type", text="Currency Type", anchor="w")
        treeview.heading("Exchange Rate (VND)",
                         text="Exchange Rate (VND)", anchor="w")
        treeview.heading("Total Amount (VND)",
                         text="Total Amount (VND)", anchor="w")
        return treeview

    def populate_treeview_with_gold_transactions_by_date(self, treeview,
                                                         transactions,
                                                         day, month, year):
        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                if (transaction._day, MonthLabel(transaction._month),
                        transaction._year) == (day, month, year):
                    # transaction_date = "{} {} {}".format(
                    #     transaction._day, MonthLabel(transaction._month),
                    #     transaction._year)
                    formatted_unit_price = self.format_price_number(
                        transaction._unit_price)
                    formatted_total_amount = self.format_price_number(
                        transaction._total_amount)
                    treeview.insert("", "end", values=(
                        transaction._id,
                        # transaction_date,
                        formatted_unit_price,
                        transaction._quantity,
                        transaction._gold_type.name,
                        formatted_total_amount
                    ))

    def populate_treeview_with_currency_transactions_by_date(self, treeview,
                                                             transactions,
                                                             day, month, year):
        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                if (transaction._day, MonthLabel(transaction._month),
                        transaction._year) == (day, month, year):
                    # transaction_date = "{} {} {}".format(
                    #     transaction._day, MonthLabel(transaction._month),
                    #     transaction._year)
                    formatted_quantity = self.format_price_number(
                        transaction._quantity)
                    formatted_exchange_rate = self.format_price_number(
                        transaction._exchange_rate._rate)
                    formatted_total_amount = self.format_price_number(
                        transaction._total_amount)
                    treeview.insert("", "end", values=(
                        transaction._id,
                        # transaction_date,
                        formatted_quantity,
                        transaction._currency_type.name,
                        formatted_exchange_rate,
                        formatted_total_amount
                    ))

    # Group By Category
    def create_content_treeview_by_category(self, frame, transactions):
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

        treeview_gold_transaction = \
            self.create_gold_transaction_treeview_by_category(
                frame_gold, gold_transactions)
        self.populate_treeview_with_gold_transactions_by_category(
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

        treeview_currency_transaction \
            = self.create_currency_transaction_treeview_by_category(
                frame_currency, currency_transactions)
        self.populate_treeview_with_currency_transactions_by_category(
            treeview_currency_transaction, currency_transactions)
        treeview_currency_transaction.pack(padx=20, pady=(10, 20), fill="x")

        treeview_gold_transaction.bind(
            '<<TreeviewSelect>>', lambda event:
            self.on_gold_treeview_select(
                event,
                tab_type=TabGroupBySortByType.GROUPBYCATEGORY,
                transactions=transactions))
        treeview_currency_transaction.bind(
            '<<TreeviewSelect>>', lambda event:
            self.on_currency_treeview_select(
                event,
                tab_type=TabGroupBySortByType.GROUPBYCATEGORY,
                transactions=transactions))

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

    def calculate_total_amount_by_category(self, transactions):
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction._total_amount
        return total_amount

    def create_gold_transaction_treeview_by_category(self, frame,
                                                     gold_transactions):
        total_amount_gold = self.calculate_total_amount_by_category(
            gold_transactions)
        formatted_total_amount_gold = self.format_price_number(
            total_amount_gold)
        self.create_header_transaction_treeview(
            frame, formatted_total_amount_gold, "GOLD TRANSACTIONS")

        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=7, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./resources/images/details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./resources/images/edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./resources/images/delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_gold_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_gold_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_gold_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_gold_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_gold_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_gold_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

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

    def create_currency_transaction_treeview_by_category(self, frame,
                                                         currency_transactions
                                                         ):
        total_amount_currency = self.calculate_total_amount_by_category(
            currency_transactions)
        formatted_total_amount_currency = self.format_price_number(
            total_amount_currency)
        self.create_header_transaction_treeview(
            frame, formatted_total_amount_currency, "CURRENCY TRANSACTIONS")

        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=7, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./resources/images/details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./resources/images/edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./resources/images/delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_currency_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_currency_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_currency_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_currency_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_currency_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_currency_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

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

    def populate_treeview_with_gold_transactions_by_category(self, treeview,
                                                             transactions):
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

    def populate_treeview_with_currency_transactions_by_category(self,
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

    # Sort By Frame
    def create_date_sort_by_frame(self, parent, transactions, option):
        frame = customtkinter.CTkScrollableFrame(
            parent, fg_color="transparent",
            height=530)

        self.get_date_in_transactions_with_option_sort(
            frame, transactions, option)

        return frame

    def create_total_amount_sort_by_frame(self, parent, transactions, option):
        frame = customtkinter.CTkScrollableFrame(
            parent, fg_color="transparent",
            height=530)

        self.create_content_treeview_sort_by_total_amount(
            frame, transactions, option)

        return frame

    # Sort By Date
    def get_date_in_transactions_with_option_sort(self, parent, transactions,
                                                  option):
        unique_dates = set()

        for transaction in transactions:
            day = transaction._day
            month = MonthLabel(transaction._month)
            year = transaction._year

            date_object = datetime.date(year, month.value, day)

            unique_dates.add(date_object)

        sorted_dates = sorted(unique_dates, reverse=option)

        for date_obj in sorted_dates:
            day = date_obj.day
            month = MonthLabel(date_obj.month)
            year = date_obj.year

            group_by_date_items_frame = self.create_group_by_date_items_frame(
                parent, day, month, year, transactions=transactions)
            group_by_date_items_frame.pack(padx=5, pady=(5, 10), fill="x")

    # Sort By Total Amount
    def create_content_treeview_sort_by_total_amount(self, frame,
                                                     transactions, option):
        sorted_transactions = sorted(
            transactions, key=lambda x: x._total_amount, reverse=option)

        for transaction in sorted_transactions:
            transaction_list = [transaction]
            self.create_frame_for_content_treeview(
                frame, transaction_list)

    def create_frame_for_content_treeview(self, frame, transactions):
        frame_items = customtkinter.CTkFrame(
            frame, fg_color="#ffffff",
            border_width=2, border_color="#4a4a4a")
        frame_items.pack(padx=5, pady=5, fill="x")

        if transactions:
            if isinstance(transactions[0], GoldTransaction):
                treeview_transaction = \
                    self.create_gold_tv_sort_by_total_amount(
                        frame_items, transactions)
                self.populate_tv_with_gold_sort_by_total_amount(
                    treeview_transaction, transactions)
                treeview_transaction.bind(
                    '<<TreeviewSelect>>', lambda event:
                    self.on_gold_treeview_select(
                        event,
                        tab_type=TabGroupBySortByType.SORTBYTOTALAMOUNT,
                        transactions=transactions))
            elif isinstance(transactions[0], CurrencyTransaction):
                treeview_transaction \
                    = self.create_currency_tv_sort_by_total_amount(
                        frame_items, transactions)
                self.populate_tv_with_currency_sort_by_total_amount(
                    treeview_transaction, transactions)
                treeview_transaction.bind(
                    '<<TreeviewSelect>>', lambda event:
                    self.on_currency_treeview_select(
                        event,
                        tab_type=TabGroupBySortByType.SORTBYTOTALAMOUNT,
                        transactions=transactions))

            treeview_transaction.pack(
                padx=20, pady=(10, 20), fill="x")

        separator_style = ttk.Style()
        separator_style.configure(
            "Separator.TSeparator", background="#989DA1", borderwidth=1)

        separator = ttk.Separator(
            frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(padx=10, pady=10, fill="x")

    def create_header_transaction_treeview_sort_by(self, frame,
                                                   total_amount, label):
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

    def calculate_total_amount_sort_by_total_amount(self, transactions):
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction._total_amount
        return total_amount

    def create_gold_tv_sort_by_total_amount(self, frame,
                                            gold_transactions):
        total_amount_gold = self.calculate_total_amount_sort_by_total_amount(
            gold_transactions)
        formatted_total_amount_gold = self.format_price_number(
            total_amount_gold)
        self.create_header_transaction_treeview_sort_by(
            frame, formatted_total_amount_gold, "GOLD TRANSACTIONS")

        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=7, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./resources/images/details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./resources/images/edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./resources/images/delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_gold_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_gold_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_gold_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_gold_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_gold_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_gold_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type",
            # "Total Amount (VND)"
        ), show="headings", height=1)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Unit Price (VND/tael)",
                         text="Unit Price (VND/tael)", anchor="w")
        treeview.heading("Quantity (tael)", text="Quantity (tael)", anchor="w")
        treeview.heading("Gold Type", text="Gold Type", anchor="w")
        # treeview.heading("Total Amount (VND)",
        #                  text="Total Amount (VND)", anchor="w")

        return treeview

    def create_currency_tv_sort_by_total_amount(self, frame,
                                                currency_transactions
                                                ):
        total_amount_currency = \
            self.calculate_total_amount_sort_by_total_amount(
                currency_transactions)
        formatted_total_amount_currency = self.format_price_number(
            total_amount_currency)
        self.create_header_transaction_treeview_sort_by(
            frame, formatted_total_amount_currency, "CURRENCY TRANSACTIONS")

        frame_label_actions = customtkinter.CTkFrame(
            frame, fg_color="transparent")
        frame_label_actions.pack(padx=10, pady=(5, 0), fill="x")

        frame_action_buttons = customtkinter.CTkFrame(
            frame_label_actions, fg_color="transparent")
        frame_action_buttons.grid(row=0, column=1, padx=7, pady=0, sticky="e")

        label_actions = customtkinter.CTkLabel(
            frame_action_buttons, text="Actions:", text_color="black",
            font=("Arial", 14))
        label_actions.pack(side="left", padx=5, pady=0)

        details_icon = customtkinter.CTkImage(
            Image.open('./resources/images/details.ico'))
        edit_icon = customtkinter.CTkImage(
            Image.open('./resources/images/edit.ico'))
        delete_icon = customtkinter.CTkImage(
            Image.open('./resources/images/delete.ico'))

        btn_details = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=details_icon,
            width=30, height=30,
            fg_color="#ffffff",
            hover_color="light blue",
            border_width=1,
            border_color="#5b8dcb",
            corner_radius=5,
            command=self.open_view_details_currency_transaction_window)
        btn_details.pack(side="left", padx=2, pady=0)

        self.view_details_currency_transaction_window = None

        btn_edit = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=edit_icon,
            width=30, height=30,
            command=self.open_edit_currency_transaction_window)
        btn_edit.pack(side="left", padx=2, pady=0)

        self.edit_currency_transaction_window = None

        btn_delete = customtkinter.CTkButton(
            frame_action_buttons,
            text=None,
            image=delete_icon,
            width=30, height=30,
            fg_color="red",
            hover_color="dark red",
            corner_radius=5,
            command=self.open_delete_currency_transaction_window)
        btn_delete.pack(side="left", padx=2, pady=0)

        self.delete_currency_transaction_window = None

        frame_label_actions.columnconfigure(0, weight=0)
        frame_label_actions.columnconfigure(1, weight=1)

        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)",
            # "Total Amount (VND)"
        ), show="headings", height=1)

        treeview.heading("Transaction Code",
                         text="Transaction Code", anchor="w")
        treeview.heading("Transaction Date",
                         text="Transaction Date", anchor="w")
        treeview.heading("Quantity", text="Quantity", anchor="w")
        treeview.heading("Currency Type", text="Currency Type", anchor="w")
        treeview.heading("Exchange Rate (VND)",
                         text="Exchange Rate (VND)", anchor="w")
        # treeview.heading("Total Amount (VND)",
        #                  text="Total Amount (VND)", anchor="w")
        return treeview

    def populate_tv_with_gold_sort_by_total_amount(self,
                                                   treeview,
                                                   transactions):
        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                transaction_date = "{} {} {}".format(
                    transaction._day, MonthLabel(transaction._month),
                    transaction._year)
                formatted_unit_price = self.format_price_number(
                    transaction._unit_price)
                # formatted_total_amount = self.format_price_number(
                #     transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_unit_price,
                    transaction._quantity,
                    transaction._gold_type.name,
                    # formatted_total_amount
                ))

    def populate_tv_with_currency_sort_by_total_amount(self,
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
                # formatted_total_amount = self.format_price_number(
                #     transaction._total_amount)
                treeview.insert("", "end", values=(
                    transaction._id,
                    transaction_date,
                    formatted_quantity,
                    transaction._currency_type.name,
                    formatted_exchange_rate,
                    # formatted_total_amount
                ))

    # General auxiliary functions
    def on_gold_treeview_select(self, event, tab_type, transactions):
        if tab_type == TabGroupBySortByType.GROUPBYDATE or \
                tab_type == TabGroupBySortByType.SORTBYDATE:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_gold_status = True
                self.selected_gold_transaction_code = values[0]
                self.selected_gold_unit_price = values[1]
                self.selected_gold_quantity = values[2]
                self.selected_gold_type = values[3]
                self.selected_gold_total_amount = values[4]

                self.selected_gold_transaction_date = None

                for transaction in transactions:
                    if isinstance(transaction, GoldTransaction):
                        if str(transaction._id) == \
                                str(self.selected_gold_transaction_code):
                            day = transaction._day
                            month = transaction._month
                            year = transaction._year

                            month_name = str(MonthLabel(month))

                            formatted_date = f"{day} {month_name} {year}"

                            self.selected_gold_transaction_date \
                                = formatted_date
                            break

            else:
                self.selected_gold_status = False

        if tab_type == TabGroupBySortByType.GROUPBYCATEGORY:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_gold_status = True
                self.selected_gold_transaction_code = values[0]
                self.selected_gold_transaction_date = values[1]
                self.selected_gold_unit_price = values[2]
                self.selected_gold_quantity = values[3]
                self.selected_gold_type = values[4]
                self.selected_gold_total_amount = values[5]
            else:
                self.selected_gold_status = False

        if tab_type == TabGroupBySortByType.SORTBYTOTALAMOUNT:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_gold_status = True
                self.selected_gold_transaction_code = values[0]
                self.selected_gold_transaction_date = values[1]
                self.selected_gold_unit_price = values[2]
                self.selected_gold_quantity = values[3]
                self.selected_gold_type = values[4]

                self.selected_gold_total_amount = None

                for transaction in transactions:
                    if isinstance(transaction, GoldTransaction):
                        if str(transaction._id) == \
                                str(self.selected_gold_transaction_code):
                            formatted_total_amount = self.format_price_number(
                                transaction._total_amount)
                            self.selected_gold_total_amount = \
                                formatted_total_amount
                            break
            else:
                self.selected_gold_status = False

    def on_currency_treeview_select(self, event, tab_type, transactions):
        if tab_type == TabGroupBySortByType.GROUPBYDATE or \
                tab_type == TabGroupBySortByType.SORTBYDATE:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_currency_status = True
                self.selected_currency_transaction_code = values[0]
                self.selected_currency_quantity = values[1]
                self.selected_currency_type = values[2]
                self.selected_currency_exchange_rate = values[3]
                self.selected_currency_total_amount = values[4]

                self.selected_currency_transaction_date = None

                for transaction in transactions:
                    if isinstance(transaction, CurrencyTransaction):
                        if str(transaction._id) == \
                                str(self.selected_currency_transaction_code):
                            day = transaction._day
                            month = transaction._month
                            year = transaction._year

                            month_name = str(MonthLabel(month))

                            formatted_date = f"{day} {month_name} {year}"

                            self.selected_currency_transaction_date \
                                = formatted_date
                            break

            else:
                self.selected_currency_status = False

        if tab_type == TabGroupBySortByType.GROUPBYCATEGORY:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_currency_status = True
                self.selected_currency_transaction_code = values[0]
                self.selected_currency_transaction_date = values[1]
                self.selected_currency_quantity = values[2]
                self.selected_currency_type = values[3]
                self.selected_currency_exchange_rate = values[4]
                self.selected_currency_total_amount = values[5]
            else:
                self.selected_currency_status = False

        if tab_type == TabGroupBySortByType.SORTBYTOTALAMOUNT:
            treeview = event.widget
            selected_items = treeview.selection()
            if selected_items:
                selected_item = selected_items[0]
                values = treeview.item(selected_item, "values")

                self.selected_currency_status = True
                self.selected_currency_transaction_code = values[0]
                self.selected_currency_transaction_date = values[1]
                self.selected_currency_quantity = values[2]
                self.selected_currency_type = values[3]
                self.selected_currency_exchange_rate = values[4]

                self.selected_currency_total_amount = None

                for transaction in transactions:
                    if isinstance(transaction, CurrencyTransaction):
                        if str(transaction._id) == \
                                str(self.selected_currency_transaction_code):
                            formatted_total_amount = self.format_price_number(
                                transaction._total_amount)
                            self.selected_currency_total_amount = \
                                formatted_total_amount
                            break

            else:
                self.selected_currency_status = False

    def open_view_details_gold_transaction_window(self):
        if self.selected_gold_status:
            if self.view_details_gold_transaction_window is None \
                or not self.view_details_gold_transaction_window \
                    .winfo_exists():
                self.view_details_gold_transaction_window \
                    = ViewDetailsGoldTransactionWindow(
                        self)
                self.view_details_gold_transaction_window.after(
                    10, self.view_details_gold_transaction_window.lift)
            else:
                self.view_details_gold_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a gold transaction to view details.")

    def open_view_details_currency_transaction_window(self):
        if self.selected_currency_status:
            if self.view_details_currency_transaction_window is None \
                or not self.view_details_currency_transaction_window \
                    .winfo_exists():
                self.view_details_currency_transaction_window \
                    = ViewDetailsCurrencyTransactionWindow(
                        self)
                self.view_details_currency_transaction_window.after(
                    10, self.view_details_currency_transaction_window.lift)
            else:
                self.view_details_currency_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a currency transaction to view details.")

    def open_edit_gold_transaction_window(self):
        if self.selected_gold_status:
            if self.edit_gold_transaction_window is None \
                or not self.edit_gold_transaction_window \
                    .winfo_exists():
                self.edit_gold_transaction_window \
                    = EditGoldTransactionWindow(
                        self)
                self.edit_gold_transaction_window.after(
                    10, self.edit_gold_transaction_window.lift)
            else:
                self.edit_gold_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a gold transaction to edit.")

    def open_edit_currency_transaction_window(self):
        if self.selected_currency_status:
            if self.edit_currency_transaction_window is None \
                or not self.edit_currency_transaction_window \
                    .winfo_exists():
                self.edit_currency_transaction_window \
                    = EditCurrencyTransactionWindow(
                        self)
                self.edit_currency_transaction_window.after(
                    10, self.edit_currency_transaction_window.lift)
            else:
                self.edit_currency_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a currency transaction to edit.")

    def open_delete_gold_transaction_window(self):
        if self.selected_gold_status:
            if self.delete_gold_transaction_window is None \
                or not self.delete_gold_transaction_window \
                    .winfo_exists():
                self.delete_gold_transaction_window \
                    = DeleteGoldTransactionWindow(
                        self)
                self.delete_gold_transaction_window.after(
                    10, self.delete_gold_transaction_window.lift)
            else:
                self.delete_gold_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a gold transaction to delete.")

    def open_delete_currency_transaction_window(self):
        if self.selected_currency_status:
            if self.delete_currency_transaction_window is None \
                or not self.delete_currency_transaction_window \
                    .winfo_exists():
                self.delete_currency_transaction_window \
                    = DeleteCurrencyTransactionWindow(
                        self)
                self.delete_currency_transaction_window.after(
                    10, self.delete_currency_transaction_window.lift)
            else:
                self.delete_currency_transaction_window.focus()
        else:
            messagebox.showinfo(
                "Notification",
                "Please select a currency transaction to delete.")

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount

    def show_frame(self, frame):
        frame.pack(padx=10, pady=5, fill="x")

    def hide_frame(self, frame):
        frame.pack_forget()
