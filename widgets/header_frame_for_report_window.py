import customtkinter


class HeaderFrameForReportWindow(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#dbdbdb", bg_color="#f2f2f2")

        self.label_report = customtkinter.CTkLabel(
            self, text="Overview", text_color="black",
            font=("TkDefaultFont", 24, "bold"))
        self.label_report.grid(
            row=0, column=0, sticky="w", padx=12, pady=5)

        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.grid(row=0, column=1, sticky="e", padx=12, pady=5)
        self.buttons_frame.configure(fg_color="transparent")

        self.btn_close = customtkinter.CTkButton(
            self.buttons_frame,
            text="CLOSE REPORT",
            fg_color="#d93547",
            hover_color="dark red",
            command=self.master.destroy
        )
        self.btn_close.pack(side="right", padx=5, pady=5)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
