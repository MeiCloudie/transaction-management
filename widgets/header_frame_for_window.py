from tkinter import ttk
import customtkinter
from PIL import Image


class HeaderFrameForWindow(customtkinter.CTkFrame):
    def __init__(self, master, label_header, submit_event,
                 show_submit=True, show_search_bar=False, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#dbdbdb", bg_color="#ffffff")

        self.search_icon = customtkinter.CTkImage(
            Image.open('./resources/images/search.ico'))

        self.label_transaction = customtkinter.CTkLabel(
            self, text=label_header, text_color="black",
            font=("TkDefaultFont", 24, "bold"))
        self.label_transaction.grid(
            row=0, column=0, sticky="w", padx=12, pady=5)

        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.grid(row=0, column=1, sticky="e", padx=12, pady=5)
        self.buttons_frame.configure(fg_color="transparent")

        self.btn_close = customtkinter.CTkButton(
            self.buttons_frame,
            text=f"CLOSE {label_header}",
            fg_color="#d93547",
            hover_color="dark red",
            command=self.master.destroy
        )
        self.btn_close.pack(side="right", padx=5, pady=5)

        if show_submit:
            self.btn_submit = customtkinter.CTkButton(
                self.buttons_frame,
                text=f"SUBMIT {label_header}",
                fg_color="green",
                hover_color="dark green",
                command=submit_event
            )
            self.btn_submit.pack(side="right", padx=5, pady=5)

        if show_search_bar:
            self.search_bar_frame = customtkinter.CTkFrame(
                master=self.buttons_frame,
                fg_color="transparent")
            self.search_bar_frame.pack(side="right", padx=5, pady=0)

            self.optionmenu = customtkinter. \
                CTkOptionMenu(self.search_bar_frame,
                              values=[
                                  "Code", "Date", "Type"],
                              command=self.option_menu_callback)
            self.optionmenu.set("Code")
            self.optionmenu.grid(row=0, column=0, padx=2, pady=0)

            self.entry_frame = customtkinter.CTkFrame(
                master=self.search_bar_frame,
                fg_color="transparent"
            )
            self.entry_frame.grid(row=0, column=1, padx=2, pady=0)

            self.search_entry = customtkinter.CTkEntry(
                self.entry_frame,
                placeholder_text="Search code... (Ex: GLD001)",
                width=280)
            self.search_entry.grid(row=0, column=0, padx=2, pady=0)

            self.btn_submit_search = customtkinter.CTkButton(
                self.search_bar_frame,
                text=None,
                image=self.search_icon,
                width=30, height=30, command=submit_event)
            self.btn_submit_search.grid(row=0, column=2, padx=2, pady=0)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def option_menu_callback(self, choice):
        if self.entry_frame is not None:
            self.entry_frame.destroy()

        if choice == "Code":
            self.entry_frame = customtkinter.CTkFrame(
                master=self.search_bar_frame,
                fg_color="transparent"
            )
            self.entry_frame.grid(row=0, column=1, padx=2, pady=0)

            self.search_entry = customtkinter.CTkEntry(
                self.entry_frame,
                placeholder_text="Search code... (Ex: GLD001)",
                width=280)
            self.search_entry.grid(row=0, column=1, padx=2, pady=0)
        elif choice == "Date":
            if hasattr(self, "date_frame"):
                self.date_frame.destroy()

            self.entry_frame = customtkinter.CTkFrame(
                master=self.search_bar_frame,
                fg_color="transparent"
            )
            self.entry_frame.grid(row=0, column=1, padx=2, pady=0)

            date_frame = customtkinter.CTkFrame(
                master=self.entry_frame,
                fg_color="transparent"
            )
            date_frame.grid(row=0, column=1, padx=5, pady=0)

            self.entry_day = customtkinter.CTkEntry(
                master=date_frame, placeholder_text="Day", width=80)
            self.entry_day.grid(row=0, column=0, padx=5, pady=0)

            separator_day_month = ttk.Separator(
                date_frame, orient="horizontal", style="Separator.TSeparator")
            separator_day_month.grid(row=0, column=1,
                                     padx=0, pady=0, sticky="ew")

            self._entry_month = customtkinter.CTkEntry(
                master=date_frame, placeholder_text="Month", width=80)
            self._entry_month.grid(row=0, column=2, padx=5, pady=0)

            separator_month_year = ttk.Separator(
                date_frame, orient="horizontal", style="Separator.TSeparator")
            separator_month_year.grid(
                row=0, column=3, padx=0, pady=0, sticky="ew")

            self.entry_year = customtkinter.CTkEntry(
                master=date_frame, placeholder_text="Year", width=80)
            self.entry_year.grid(row=0, column=4, padx=5, pady=0)
        elif choice == "Type":
            self.entry_frame = customtkinter.CTkFrame(
                master=self.search_bar_frame,
                fg_color="transparent"
            )
            self.entry_frame.grid(row=0, column=1, padx=2, pady=0)

            self.search_entry = customtkinter.CTkEntry(
                self.entry_frame, placeholder_text="Search type... (Ex: Gold)",
                width=280)
            self.search_entry.grid(row=0, column=1, padx=2, pady=0)
