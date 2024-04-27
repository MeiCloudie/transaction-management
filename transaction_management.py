import customtkinter
import os


class TransactionApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Transaction Management")
        self._set_appearance_mode("light")

        # Get the full path to the icon file
        icon_path = os.path.abspath("./logo.ico")

        # Set the window icon using iconbitmap method
        self.iconbitmap(icon_path)


if __name__ == "__main__":
    app = TransactionApp()
    app.mainloop()
