import customtkinter
from PIL import Image

from widgets.filter_window import FilterWindow
from widgets.search_window import SearchWindow
from widgets.add_transaction_window import AddTransactionWindow
from widgets.report_window import ReportWindow


class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, initial_theme="Dark-Blue", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#dbdbdb", bg_color="#f2f2f2")
        self.refresh_icon = customtkinter.CTkImage(
            Image.open('./resources/images/refresh.ico'))
        self.filter_icon = customtkinter.CTkImage(
            Image.open('./resources/images/filter.ico'))
        self.search_icon = customtkinter.CTkImage(
            Image.open('./resources/images/search.ico'))

        self.label_transaction = customtkinter.CTkLabel(
            self, text="Transaction", text_color="black",
            font=("TkDefaultFont", 24, "bold"))
        self.label_transaction.grid(
            row=0, column=0, sticky="w", padx=12, pady=5)

        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.grid(row=0, column=1, sticky="e", padx=12, pady=5)
        self.buttons_frame.configure(fg_color="transparent")

        self.btn_search = customtkinter.CTkButton(
            self.buttons_frame,
            text=None,
            image=self.search_icon,
            width=30, height=30, command=self.open_search_window)
        self.btn_search.pack(side="right", padx=5, pady=5)

        self.search_window = None

        self.btn_filter = customtkinter.CTkButton(
            self.buttons_frame,
            text=None,
            image=self.filter_icon,
            width=30, height=30, command=self.open_filter_window)
        self.btn_filter.pack(side="right", padx=5, pady=5)

        self.filter_window = None

        self.btn_refresh = customtkinter.CTkButton(
            self.buttons_frame,
            text=None,
            image=self.refresh_icon,
            fg_color="green",
            hover_color="dark green",
            width=30, height=30)
        self.btn_refresh.configure(command=self.master.refresh_data_from_excel)
        self.btn_refresh.pack(side="right", padx=5, pady=5)

        self.btn_add_transaction = customtkinter.CTkButton(
            self.buttons_frame, text="ADD TRANSACTION",
            command=self.open_add_transaction_window)
        self.btn_add_transaction.pack(side="right", padx=5, pady=5)

        self.add_transaction_window = None

        self.btn_report = customtkinter.CTkButton(
            self.buttons_frame, text="REPORT", text_color="#1f6aa5",
            border_width=1,
            border_color="#1f6aa5", fg_color="white",
            hover_color="light blue",
            command=self.open_report_window)
        self.btn_report.pack(side="right", padx=5, pady=5)

        self.report_window = None

        self.vertical_separator = customtkinter.CTkFrame(
            self.buttons_frame, width=2, height=30, fg_color="grey")
        self.vertical_separator.pack(side="right", padx=5, pady=5, fill="y")

        self.optionmenu_theme = customtkinter. \
            CTkOptionMenu(self.buttons_frame,
                          values=[
                              "Dark-Blue", "Blue", "Green"],
                          command=self.option_menu_theme_callback)
        self.optionmenu_theme.set(initial_theme)
        self.optionmenu_theme.pack(side="right", padx=5, pady=5)

        theme_label = customtkinter.CTkLabel(
            self.buttons_frame, text="Theme: ", text_color="black",
            font=("Arial", 14, "bold"))
        theme_label.pack(side="right", padx=0, pady=5)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def option_menu_theme_callback(self, choice):
        if choice == "Dark-Blue":
            customtkinter.set_default_color_theme("dark-blue")
        elif choice == "Blue":
            customtkinter.set_default_color_theme("blue")
        elif choice == "Green":
            customtkinter.set_default_color_theme("green")
        self.master.update_theme(choice)

    def open_filter_window(self):
        if self.filter_window is None or not \
                self.filter_window.winfo_exists():
            self.filter_window = FilterWindow(self)
            self.filter_window.after(10, self.filter_window.lift)
        else:
            self.filter_window.focus()

    def open_search_window(self):
        if self.search_window is None or not \
                self.search_window.winfo_exists():
            self.search_window = SearchWindow(self)
            self.search_window.after(10, self.search_window.lift)
        else:
            self.search_window.focus()

    def open_add_transaction_window(self):
        if self.add_transaction_window is None or not \
                self.add_transaction_window.winfo_exists():
            self.add_transaction_window = AddTransactionWindow(self)
            self.add_transaction_window.after(10,
                                              self.add_transaction_window.lift)
        else:
            self.add_transaction_window.focus()

    def open_report_window(self):
        if self.report_window is None or not \
                self.report_window.winfo_exists():
            self.report_window = ReportWindow(self)
            self.report_window.after(10, self.report_window.lift)
        else:
            self.report_window.focus()
