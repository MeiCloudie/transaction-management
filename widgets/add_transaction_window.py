import customtkinter
from sys import platform

from widgets.add_transaction_tab_view import AddTransactionTabView


class AddTransactionWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Add Transaction")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.configure(fg_color="#d9d9d9")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(
                "./resources/images/logo.ico"))

    def create_widget(self):
        self.add_transaction_tab_views = AddTransactionTabView(
            master=self)
        self.add_transaction_tab_views.pack(padx=20, pady=5, fill="x")
