import customtkinter
from sys import platform

from widgets.header_frame_for_report_window import HeaderFrameForReportWindow
from widgets.tab_report import TabReport


class ReportWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Report")
        self.iconbitmap(default='./resources/images/logo.ico')
        self.minsize(1700, 990)
        self.configure(fg_color="#eaeaea")

        self.create_widget()

        if platform.startswith("win"):
            self.after(200,
                       lambda: self.iconbitmap("./resources/images/logo.ico"))

    def create_widget(self):
        self.header_frame = HeaderFrameForReportWindow(master=self)
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.tab_report = TabReport(master=self)
        self.tab_report.grid(row=1, column=0, padx=10,
                             pady=(0, 10), sticky="ew")

        self.grid_columnconfigure(0, weight=1)
