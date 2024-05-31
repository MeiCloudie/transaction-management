from tkinter import ttk
import customtkinter
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

from enums.month_label_enum import MonthLabel
from enums.gold_type_enum import GoldType
from enums.currency_type_enum import CurrencyType
from models.gold_transaction_model import GoldTransaction
from models.currency_transaction_model import CurrencyTransaction
from widgets.total_details_window import TotalDetailsWindow
from widgets.statistics_details_month_window \
    import StatisticsDetailsMonthWindow
from widgets.statistics_details_week_window \
    import StatisticsDetailsWeekWindow


class TabReport(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.total_details_window = None
        self.configure(fg_color="#dbdbdb", bg_color="#eaeaea",
                       border_width=1, border_color="#989DA1")

        self.tab_week = self.add("WEEK")
        self.tab_month = self.add("MONTH")

        self.set("MONTH")
        self.configure(corner_radius=5)

        self.all_transactions = \
            self.master.master.master.transaction_list.get_transactions()

        self.create_tab_report_widgets()

    def create_tab_report_widgets(self):
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        current_week = now.isocalendar()[1]

        transactions_this_month = [
            txn for txn in self.all_transactions
            if txn._year == current_year and txn._month == current_month
        ]

        transactions_this_week = [
            txn for txn in self.all_transactions
            if txn._year ==
            current_year and datetime.date(txn._year,
                                           txn._month,
                                           txn._day).isocalendar()[1]
            == current_week
        ]

        # Month
        month_scroll_frame = customtkinter.CTkScrollableFrame(
            self.tab_month, fg_color="transparent",
            height=850)
        month_scroll_frame.pack(padx=0, pady=0, fill="x")

        frame_month_1 = customtkinter.CTkFrame(
            master=month_scroll_frame,
            fg_color="transparent",
        )
        frame_month_1.pack(padx=5, pady=5, fill="x")

        frame_month_1.grid_columnconfigure(0, weight=1)
        frame_month_1.grid_columnconfigure(1, weight=2)

        month_total_chart = \
            self.create_total_chart_frame(frame_month_1,
                                          transactions_this_month,
                                          btn_details_status=True)
        month_total_chart.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        month_recent_transaction = \
            self.create_recent_transaction_frame(frame_month_1,
                                                 transactions_this_month)
        month_recent_transaction.grid(row=0, column=1, columnspan=2,
                                      padx=5, pady=5, sticky="ew")

        frame_month_2 = customtkinter.CTkFrame(
            master=month_scroll_frame,
            fg_color="transparent",
        )
        frame_month_2.pack(padx=5, pady=(0, 5), fill="x")

        month_statistics_chart = \
            self.create_statistics_chart_frame(frame_month_2,
                                               transactions_this_month,
                                               self.tab_month,
                                               btn_details_status=True)
        month_statistics_chart.pack(padx=5, pady=(2, 5), fill="x")

        # Week
        week_scroll_frame = customtkinter.CTkScrollableFrame(
            self.tab_week, fg_color="transparent",
            height=850)
        week_scroll_frame.pack(padx=0, pady=0, fill="x")

        frame_week_1 = customtkinter.CTkFrame(
            master=week_scroll_frame,
            fg_color="transparent",
        )
        frame_week_1.pack(padx=5, pady=5, fill="x")

        frame_week_1.grid_columnconfigure(0, weight=1)
        frame_week_1.grid_columnconfigure(1, weight=2)

        week_total_chart = \
            self.create_total_chart_frame(frame_week_1,
                                          transactions_this_week,
                                          btn_details_status=True)
        week_total_chart.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        week_recent_transaction = \
            self.create_recent_transaction_frame(frame_week_1,
                                                 transactions_this_week)
        week_recent_transaction.grid(row=0, column=1, columnspan=2,
                                     padx=5, pady=5, sticky="ew")

        frame_week_2 = customtkinter.CTkFrame(
            master=week_scroll_frame,
            fg_color="transparent",
        )
        frame_week_2.pack(padx=5, pady=(0, 5), fill="x")

        week_statistics_chart = \
            self.create_statistics_chart_frame(frame_week_2,
                                               transactions_this_week,
                                               self.tab_week,
                                               btn_details_status=True)
        week_statistics_chart.pack(padx=5, pady=(2, 5), fill="x")

    def create_total_chart_frame(self, parent, transactions,
                                 btn_details_status):
        total_chart_frame = customtkinter.CTkFrame(
            master=parent, fg_color="#ffffff",
            border_width=2, border_color="#989DA1",
            corner_radius=5)

        frame_title_and_button = customtkinter.CTkFrame(
            master=total_chart_frame, fg_color="transparent")
        frame_title_and_button.pack(padx=10, pady=(20, 0), fill="x")

        frame_title_and_button.columnconfigure(0, weight=0)
        frame_title_and_button.columnconfigure(1, weight=1)

        total_chart_title = customtkinter.CTkLabel(
            master=frame_title_and_button,
            text="Total",
            font=("Arial", 20, "bold"),
            text_color="black",
        )
        total_chart_title.grid(
            row=0, column=0, sticky="w", padx=12, pady=0)

        if btn_details_status:
            btn_details_report = customtkinter.CTkButton(
                frame_title_and_button,
                text="See Details",
                fg_color="transparent",
                hover_color="#dae6f2",
                text_color="#5C8ECB",
                font=("Arial", 14, "bold"),
                width=30,
                command=lambda: self.open_total_details_window(transactions)
            )
            btn_details_report.grid(
                row=0, column=1, sticky="e", padx=12, pady=0)

        self.total_details_window = None

        if not transactions:
            no_data_label = customtkinter.CTkLabel(
                master=total_chart_frame,
                text="No data available this month!",
                font=("Arial", 20, "bold")
            )
            no_data_label.pack(padx=25, pady=110, fill="x")

            return total_chart_frame

        # total_amount_transaction = 0
        # gold_total_amount_transaction = 0
        # currency_total_amount_transaction = 0
        # total_amount_quantity_transaction = 0
        # gold_total_amount_quantity_transaction = 0
        # currency_total_amount_quantity_transaction = 0
        # for transaction in transactions:
        #     total_amount_transaction += transaction._total_amount
        #     total_amount_quantity_transaction += 1
        #     if isinstance(transaction, GoldTransaction):
        #         gold_total_amount_transaction += transaction._total_amount
        #         gold_total_amount_quantity_transaction += 1
        #     if isinstance(transaction, CurrencyTransaction):
        #         currency_total_amount_transaction += \
        #             transaction._total_amount
        #         currency_total_amount_quantity_transaction += 1

        total_amounts = np.array([txn._total_amount for txn in transactions])
        total_amount_transaction = np.sum(total_amounts)
        total_amount_quantity_transaction = len(transactions)

        gold_transactions = [
            txn for txn in transactions if isinstance(txn, GoldTransaction)]
        currency_transactions = [
            txn for txn in transactions if isinstance(txn,
                                                      CurrencyTransaction)]

        # gold_total_amount_transaction = np.sum(
        #     [txn._total_amount for txn in gold_transactions])
        # currency_total_amount_transaction = np.sum(
        #     [txn._total_amount for txn in currency_transactions])

        gold_total_amount_quantity_transaction = len(gold_transactions)
        currency_total_amount_quantity_transaction = len(currency_transactions)

        formatted_total_amount = self.format_price_number(
            total_amount_transaction)

        total_value = customtkinter.CTkLabel(
            master=total_chart_frame,
            text=f"{formatted_total_amount} VND ({
                total_amount_quantity_transaction})",
            anchor="w"
        )
        total_value.pack(padx=25, pady=0, fill="x")

        gold_percentage = (gold_total_amount_quantity_transaction
                           / total_amount_quantity_transaction) * 100 \
            if total_amount_quantity_transaction != 0 else 0
        currency_percentage = (currency_total_amount_quantity_transaction /
                               total_amount_quantity_transaction) * 100 \
            if total_amount_quantity_transaction != 0 else 0

        piechart_values = [gold_percentage, currency_percentage]
        piechart_labels = ["Gold", "Currency"]
        piechart_colors = ["#f5d45f", "#2ea64d"]

        fig, ax = plt.subplots()
        ax.pie(piechart_values, labels=piechart_labels, autopct='%1.1f%%',
               colors=piechart_colors)
        ax.legend(title="Category", loc='center left',
                  bbox_to_anchor=(-0.55, 0.5))

        fig.set_size_inches(3, 3)

        canvas = FigureCanvasTkAgg(fig, master=total_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

        return total_chart_frame

    def create_recent_transaction_frame(self, parent, transactions):
        recent_transaction_frame = customtkinter.CTkFrame(
            master=parent, fg_color="#ffffff",
            border_width=2, border_color="#989DA1",
            corner_radius=5)

        recent_transaction_title = customtkinter.CTkLabel(
            master=recent_transaction_frame,
            text="Recent Transaction",
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="w"
        )
        recent_transaction_title.pack(padx=20, pady=(20, 5), fill="x")

        gold_transaction_title = customtkinter.CTkLabel(
            master=recent_transaction_frame,
            text="GOLD TRANSACTION",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w"
        )
        gold_transaction_title.pack(padx=20, pady=0, fill="x")

        gold_treeview = \
            self.create_gold_transaction_treeview(recent_transaction_frame)
        self.populate_treeview_with_gold_transactions(
            gold_treeview, transactions)
        gold_treeview.pack(padx=20, pady=5, fill="x")

        currency_transaction_title = customtkinter.CTkLabel(
            master=recent_transaction_frame,
            text="CURRENCY TRANSACTION",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w"
        )
        currency_transaction_title.pack(padx=20, pady=0, fill="x")

        currency_treeview = \
            self.create_currency_transaction_treeview(recent_transaction_frame)
        self.populate_treeview_with_currency_transactions(
            currency_treeview, transactions)
        currency_treeview.pack(padx=20, pady=(5, 20), fill="x")

        return recent_transaction_frame

    def create_statistics_chart_frame(self, parent, transactions,
                                      tab_type, btn_details_status):
        statistics_chart_frame = customtkinter.CTkFrame(
            master=parent, fg_color="#ffffff",
            border_width=2, border_color="#989DA1",
            corner_radius=5)

        frame_title_and_button = customtkinter.CTkFrame(
            master=statistics_chart_frame, fg_color="transparent")
        frame_title_and_button.pack(padx=10, pady=(20, 0), fill="x")

        frame_title_and_button.columnconfigure(0, weight=0)
        frame_title_and_button.columnconfigure(1, weight=1)

        statistics_chart_title = customtkinter.CTkLabel(
            master=frame_title_and_button,
            text="Statistics",
            font=("Arial", 20, "bold"),
            text_color="black",
        )
        statistics_chart_title.grid(
            row=0, column=0, sticky="w", padx=12, pady=0)

        if btn_details_status and tab_type == self.tab_month:
            btn_statistics_report = customtkinter.CTkButton(
                frame_title_and_button,
                text="See Details",
                fg_color="transparent",
                hover_color="#dae6f2",
                text_color="#5C8ECB",
                font=("Arial", 14, "bold"),
                width=30,
                command=lambda: self.open_statistics_details_month_window(
                    transactions)
            )
            btn_statistics_report.grid(row=0, column=1,
                                       sticky="e", padx=12, pady=0)

        self.statistics_details_month_window = None

        if btn_details_status and tab_type == self.tab_week:
            btn_statistics_report = customtkinter.CTkButton(
                frame_title_and_button,
                text="See Details",
                fg_color="transparent",
                hover_color="#dae6f2",
                text_color="#5C8ECB",
                font=("Arial", 14, "bold"),
                width=30,
                command=lambda: self.open_statistics_details_week_window(
                    transactions)
            )
            btn_statistics_report.grid(row=0, column=1,
                                       sticky="e", padx=12, pady=0)

        self.statistics_details_week_window = None

        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        month_name = str(MonthLabel(current_month))

        statistics_value = customtkinter.CTkLabel(
            master=statistics_chart_frame,
            text=f"{month_name} {current_year}",
            font=("Arial", 14),
            anchor="w"
        )
        statistics_value.pack(padx=22, pady=0, fill="x")

        if not transactions:
            no_data_label = customtkinter.CTkLabel(
                master=statistics_chart_frame,
                text="No data available this month!",
                font=("Arial", 20, "bold")
            )
            no_data_label.pack(padx=25, pady=110, fill="x")

            return statistics_chart_frame

        if tab_type == self.tab_month:
            weeks = self.get_weeks_of_month(current_year, current_month)
            totals = self.get_total_amount_per_week(transactions, weeks)

            self.plot_bar_chart_for_this_month(statistics_chart_frame,
                                               weeks, totals)
            self.plot_markers_chart_for_this_month(statistics_chart_frame,
                                                   weeks, totals)
            self.plot_gold_bar_chart_for_this_month(statistics_chart_frame,
                                                    weeks, transactions)
            self.plot_gold_markers_chart_for_this_month(statistics_chart_frame,
                                                        weeks, transactions)
            self.plot_currency_bar_chart_for_this_month(statistics_chart_frame,
                                                        weeks, transactions)
            self.plot_currency_markers_chart_for_this_month(
                statistics_chart_frame, weeks, transactions)

        elif tab_type == self.tab_week:
            self.plot_bar_chart_for_this_week(statistics_chart_frame,
                                              transactions)
            self.plot_markers_chart_for_this_week(statistics_chart_frame,
                                                  transactions)
            self.plot_gold_bar_chart_for_this_week(statistics_chart_frame,
                                                   transactions)
            self.plot_gold_markers_chart_for_this_week(statistics_chart_frame,
                                                       transactions)
            self.plot_currency_bar_chart_for_this_week(statistics_chart_frame,
                                                       transactions)
            self.plot_currency_markers_chart_for_this_week(
                statistics_chart_frame, transactions)

        return statistics_chart_frame

    def get_weeks_of_month(self, year, month):
        weeks = []
        first_day_of_month = datetime.date(year, month, 1)
        first_day_of_week = first_day_of_month - \
            datetime.timedelta(days=first_day_of_month.weekday())

        i = 0
        while True:
            start_of_week = first_day_of_week + datetime.timedelta(weeks=i)
            end_of_week = start_of_week + datetime.timedelta(days=6)

            if start_of_week.month != month:
                start_of_week = datetime.date(year, month, 1)
            if end_of_week.month != month:
                last_day_of_month = datetime.date(year, month + 1, 1) \
                    - datetime.timedelta(days=1) \
                    if month < 12 else datetime.date(year, 12, 31)
                end_of_week = last_day_of_month

            weeks.append((start_of_week, end_of_week))
            i += 1

            if end_of_week == datetime.date(year, month, 1) \
                + datetime.timedelta(days=(datetime.date(year, month + 1, 1)
                                           - datetime.date(
                                               year, month, 1)).days - 1):
                break

        return weeks

    def plot_bar_chart_for_this_month(self, parent, weeks, totals):
        week_labels = [
            f"Week {i+1}\n{start.strftime('%d/%m/%Y')
                           } - {end.strftime('%d/%m/%Y')}"
            for i, (start, end) in enumerate(weeks)
        ]

        gold_totals = [0] * len(weeks)
        currency_totals = [0] * len(weeks)
        for i, (start, end) in enumerate(weeks):
            for txn in self.all_transactions:
                txn_date = datetime.date(txn._year, txn._month, txn._day)
                if start <= txn_date <= end:
                    if isinstance(txn, GoldTransaction):
                        gold_totals[i] += txn._total_amount
                    elif isinstance(txn, CurrencyTransaction):
                        currency_totals[i] += txn._total_amount

        fig, ax = plt.subplots()
        bar_width = 0.2
        x = np.arange(len(weeks))

        ax.bar(x - bar_width, gold_totals,
               width=bar_width, label='Gold', color='#f5d45f')
        ax.bar(
            x, currency_totals, width=bar_width,
            label='Currency', color='#2ea64d')
        ax.bar(x + bar_width, totals,
               width=bar_width, label='Total')

        ax.set_xlabel('Weeks')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Weekly Total Amount for Current Month')
        ax.set_xticks(x)
        ax.set_xticklabels(week_labels, ha='center')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_total = max(totals, default=0)
        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(gold_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i - bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#f5d45f')

        for i, v in enumerate(currency_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#2ea64d')

        for i, v in enumerate(totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i + bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 2), fill="x")

    def plot_markers_chart_for_this_month(self, parent, weeks, totals):
        week_labels = [
            f"Week {i+1}\n{start.strftime('%d/%m/%Y')
                           } - {end.strftime('%d/%m/%Y')}"
            for i, (start, end) in enumerate(weeks)
        ]

        gold_totals = [0] * len(weeks)
        currency_totals = [0] * len(weeks)
        for i, (start, end) in enumerate(weeks):
            for txn in self.all_transactions:
                txn_date = datetime.date(txn._year, txn._month, txn._day)
                if start <= txn_date <= end:
                    if isinstance(txn, GoldTransaction):
                        gold_totals[i] += txn._total_amount
                    elif isinstance(txn, CurrencyTransaction):
                        currency_totals[i] += txn._total_amount

        fig, ax = plt.subplots()

        ax.plot(week_labels, gold_totals, marker='o', linestyle='-',
                label='Gold', color='#f5d45f')
        ax.plot(week_labels, currency_totals, marker='o', linestyle='-',
                label='Currency', color='#2ea64d')
        ax.plot(week_labels, totals, marker='o', linestyle='-',
                label='Total')

        ax.set_xlabel('Weeks')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Weekly Total Amount for Current Month')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_total = max(totals, default=0)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))

        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M'
        )

        for i, v in enumerate(totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center',
                    va='bottom')

        for i, v in enumerate(gold_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center', va='bottom',
                    color='#f5d45f')

        for i, v in enumerate(currency_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center', va='bottom',
                    color='#2ea64d')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 2), fill="x")

    def plot_gold_bar_chart_for_this_month(self, parent, weeks, transactions):
        week_labels = [
            f"Week {i+1}\n{start.strftime('%d/%m/%Y')
                           } - {end.strftime('%d/%m/%Y')}"
            for i, (start, end) in enumerate(weeks)
        ]

        sjc_totals = [0] * len(weeks)
        pnj_totals = [0] * len(weeks)
        doji_totals = [0] * len(weeks)

        for i, (start, end) in enumerate(weeks):
            for txn in transactions:
                if isinstance(txn, GoldTransaction):
                    txn_date = datetime.date(txn._year, txn._month, txn._day)
                    if start <= txn_date <= end:
                        if txn._gold_type == GoldType.SJC:
                            sjc_totals[i] += txn._total_amount
                        elif txn._gold_type == GoldType.PNJ:
                            pnj_totals[i] += txn._total_amount
                        elif txn._gold_type == GoldType.DOJI:
                            doji_totals[i] += txn._total_amount

        fig, ax = plt.subplots()
        bar_width = 0.2
        x = np.arange(len(weeks))

        ax.bar(x - bar_width, sjc_totals,
               width=bar_width, label='SJC', color='#f5d45f')
        ax.bar(x, pnj_totals, width=bar_width, label='PNJ', color='#df760b')
        ax.bar(x + bar_width, doji_totals,
               width=bar_width, label='DOJI', color='#743c08')

        ax.set_xlabel('Weeks')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Gold Transactions by Type for Current Month')
        ax.set_xticks(x)
        ax.set_xticklabels(week_labels, ha='center')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_sjc = max(sjc_totals, default=0)
        max_pnj = max(pnj_totals, default=0)
        max_doji = max(doji_totals, default=0)
        max_total = max(max_sjc, max_pnj, max_doji)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}' if x < 1_000_000 else f'{
                int(x // 1_000_000)}M'
        )

        for i, v in enumerate(sjc_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i - bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#f5d45f')

        for i, v in enumerate(pnj_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#df760b')

        for i, v in enumerate(doji_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i + bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#743c08')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 2), fill="x")

    def plot_gold_markers_chart_for_this_month(self, parent,
                                               weeks, transactions):
        week_labels = [
            f"Week {i+1}\n{start.strftime('%d/%m/%Y')
                           } - {end.strftime('%d/%m/%Y')}"
            for i, (start, end) in enumerate(weeks)
        ]

        sjc_totals = [0] * len(weeks)
        pnj_totals = [0] * len(weeks)
        doji_totals = [0] * len(weeks)

        for i, (start, end) in enumerate(weeks):
            for txn in transactions:
                if isinstance(txn, GoldTransaction):
                    txn_date = datetime.date(txn._year, txn._month, txn._day)
                    if start <= txn_date <= end:
                        if txn._gold_type == GoldType.SJC:
                            sjc_totals[i] += txn._total_amount
                        elif txn._gold_type == GoldType.PNJ:
                            pnj_totals[i] += txn._total_amount
                        elif txn._gold_type == GoldType.DOJI:
                            doji_totals[i] += txn._total_amount

        fig, ax = plt.subplots()

        ax.plot(week_labels, sjc_totals, marker='o',
                linestyle='-', label='SJC', color='#f5d45f')
        ax.plot(week_labels, pnj_totals, marker='o',
                linestyle='-', label='PNJ', color='#df760b')
        ax.plot(week_labels, doji_totals, marker='o',
                linestyle='-', label='DOJI', color='#743c08')

        ax.set_xlabel('Weeks')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Gold Transactions by Type for Current Month')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_sjc = max(sjc_totals, default=0)
        max_pnj = max(pnj_totals, default=0)
        max_doji = max(doji_totals, default=0)
        max_total = max(max_sjc, max_pnj, max_doji)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(sjc_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#f5d45f')

        for i, v in enumerate(pnj_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#df760b')

        for i, v in enumerate(doji_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#743c08')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 2), fill="x")

    def plot_currency_bar_chart_for_this_month(self, parent,
                                               weeks, transactions):
        week_labels = [
            f"Week {i+1}\n{start.strftime('%d/%m/%Y')
                           } - {end.strftime('%d/%m/%Y')}"
            for i, (start, end) in enumerate(weeks)
        ]

        vnd_totals = [0] * len(weeks)
        usd_totals = [0] * len(weeks)
        eur_totals = [0] * len(weeks)

        for i, (start, end) in enumerate(weeks):
            for txn in transactions:
                if isinstance(txn, CurrencyTransaction):
                    txn_date = datetime.date(txn._year, txn._month, txn._day)
                    if start <= txn_date <= end:
                        if txn._currency_type == CurrencyType.VND:
                            vnd_totals[i] += txn._total_amount
                        elif txn._currency_type == CurrencyType.USD:
                            usd_totals[i] += txn._total_amount
                        elif txn._currency_type == CurrencyType.EUR:
                            eur_totals[i] += txn._total_amount

        fig, ax = plt.subplots()
        bar_width = 0.2
        x = np.arange(len(weeks))

        ax.bar(x - bar_width, vnd_totals, width=bar_width,
               label='VND', color='#006769')
        ax.bar(x, usd_totals, width=bar_width,
               label='USD', color='#2ea64d')
        ax.bar(x + bar_width, eur_totals, width=bar_width,
               label='EUR', color='#9dde8b')

        ax.set_xlabel('Weeks')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Currency Transactions by Type for Current Month')
        ax.set_xticks(x)
        ax.set_xticklabels(week_labels, ha='center')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_vnd = max(vnd_totals, default=0)
        max_usd = max(usd_totals, default=0)
        max_eur = max(eur_totals, default=0)
        max_total = max(max_vnd, max_usd, max_eur)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(lambda x, pos: f'{x:,.0f}'
                                     if x < 1_000_000
                                     else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(vnd_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i - bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#006769')

        for i, v in enumerate(usd_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center',
                    va='bottom', color='#2ea64d')

        for i, v in enumerate(eur_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i + bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#9dde8b')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 2), fill="x")

    def plot_currency_markers_chart_for_this_month(self, parent,
                                                   weeks, transactions):
        week_labels = [
            f"Week {i+1}\n{start.strftime('%d/%m/%Y')
                           } - {end.strftime('%d/%m/%Y')}"
            for i, (start, end) in enumerate(weeks)
        ]

        vnd_totals = [0] * len(weeks)
        usd_totals = [0] * len(weeks)
        eur_totals = [0] * len(weeks)

        for i, (start, end) in enumerate(weeks):
            for txn in transactions:
                if isinstance(txn, CurrencyTransaction):
                    txn_date = datetime.date(txn._year, txn._month, txn._day)
                    if start <= txn_date <= end:
                        if txn._currency_type == CurrencyType.VND:
                            vnd_totals[i] += txn._total_amount
                        elif txn._currency_type == CurrencyType.USD:
                            usd_totals[i] += txn._total_amount
                        elif txn._currency_type == CurrencyType.EUR:
                            eur_totals[i] += txn._total_amount

        fig, ax = plt.subplots()

        ax.plot(week_labels, vnd_totals, marker='o',
                linestyle='-', label='VND', color='#006769')
        ax.plot(week_labels, usd_totals, marker='o',
                linestyle='-', label='USD', color='#2ea64d')
        ax.plot(week_labels, eur_totals, marker='o',
                linestyle='-', label='EUR', color='#9dde8b')

        ax.set_xlabel('Weeks')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Currency Transactions by Type for Current Month')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_vnd = max(vnd_totals, default=0)
        max_usd = max(usd_totals, default=0)
        max_eur = max(eur_totals, default=0)
        max_total = max(max_vnd, max_usd, max_eur)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(vnd_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#006769')

        for i, v in enumerate(usd_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#2ea64d')

        for i, v in enumerate(eur_totals):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#9dde8b')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 2), fill="x")

    # WEEK

    def plot_bar_chart_for_this_week(self, parent, transactions):
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        date_labels = [(start_of_week + datetime.timedelta(days=i)
                        ).strftime("%A\n%d/%m/%Y") for i in range(7)]

        totals = {day: 0 for day in days}
        gold_totals = {day: 0 for day in days}
        currency_totals = {day: 0 for day in days}

        for transaction in transactions:
            transaction_date = datetime.date(
                transaction._year, transaction._month, transaction._day)
            day_of_week = transaction_date.strftime('%A')
            if day_of_week in totals:
                totals[day_of_week] += transaction._total_amount
                if isinstance(transaction, GoldTransaction):
                    gold_totals[day_of_week] += transaction._total_amount
                elif isinstance(transaction, CurrencyTransaction):
                    currency_totals[day_of_week] += transaction._total_amount

        total_amounts = [totals[day] for day in days]
        gold_amounts = [gold_totals[day] for day in days]
        currency_amounts = [currency_totals[day] for day in days]

        fig, ax = plt.subplots()
        bar_width = 0.2
        x = np.arange(len(days))

        ax.bar(x - bar_width, gold_amounts, width=bar_width,
               label='Gold', color='#f5d45f')
        ax.bar(x, currency_amounts, width=bar_width,
               label='Currency', color='#2ea64d')
        ax.bar(x + bar_width, total_amounts, width=bar_width,
               label='Total')

        ax.set_xlabel('Days of the Week')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Total Amounts for Each Day of the Week')
        ax.set_xticks(x)
        ax.set_xticklabels(date_labels, ha='center')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_total = max(total_amounts, default=0)
        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(lambda x, pos: f'{x:,.0f}'
                                     if x < 1_000_000
                                     else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(gold_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i - bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#f5d45f')

        for i, v in enumerate(currency_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center',
                    va='bottom', color='#2ea64d')

        for i, v in enumerate(total_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i + bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

    def plot_markers_chart_for_this_week(self, parent, transactions):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        date_labels = [(start_of_week
                        + datetime.timedelta(days=i)).strftime("%A\n%d/%m/%Y")
                       for i in range(7)]

        totals = {day: 0 for day in days}
        gold_totals = {day: 0 for day in days}
        currency_totals = {day: 0 for day in days}

        for transaction in transactions:
            transaction_date = datetime.date(
                transaction._year, transaction._month, transaction._day)
            day_of_week = transaction_date.strftime('%A')
            if day_of_week in totals:
                totals[day_of_week] += transaction._total_amount
                if isinstance(transaction, GoldTransaction):
                    gold_totals[day_of_week] += transaction._total_amount
                elif isinstance(transaction, CurrencyTransaction):
                    currency_totals[day_of_week] += transaction._total_amount

        total_amounts = [totals[day] for day in days]
        gold_amounts = [gold_totals[day] for day in days]
        currency_amounts = [currency_totals[day] for day in days]

        fig, ax = plt.subplots()

        ax.plot(date_labels, gold_amounts, marker='o',
                linestyle='-', label='Gold', color='#f5d45f')
        ax.plot(date_labels, currency_amounts, marker='o',
                linestyle='-', label='Currency', color='#2ea64d')
        ax.plot(date_labels, total_amounts, marker='o',
                linestyle='-', label='Total')

        ax.set_xlabel('Days of the Week')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Total Amounts for Each Day of the Week')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_total = max(total_amounts, default=0)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))

        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M'
        )

        for i, v in enumerate(total_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom')

        for i, v in enumerate(gold_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#f5d45f')

        for i, v in enumerate(currency_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#2ea64d')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

    def plot_gold_bar_chart_for_this_week(self, parent, transactions):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        date_labels = [(start_of_week
                        + datetime.timedelta(days=i)).strftime("%A\n%d/%m/%Y")
                       for i in range(7)]

        sjc_totals = {day: 0 for day in days}
        pnj_totals = {day: 0 for day in days}
        doji_totals = {day: 0 for day in days}

        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                transaction_date = datetime.date(transaction._year,
                                                 transaction._month,
                                                 transaction._day)
                day_of_week = transaction_date.strftime('%A')
                if day_of_week in sjc_totals:
                    if transaction._gold_type == GoldType.SJC:
                        sjc_totals[day_of_week] += transaction._total_amount
                    elif transaction._gold_type == GoldType.PNJ:
                        pnj_totals[day_of_week] += transaction._total_amount
                    elif transaction._gold_type == GoldType.DOJI:
                        doji_totals[day_of_week] += transaction._total_amount

        sjc_amounts = [sjc_totals[day] for day in days]
        pnj_amounts = [pnj_totals[day] for day in days]
        doji_amounts = [doji_totals[day] for day in days]

        fig, ax = plt.subplots()
        bar_width = 0.2
        x = np.arange(len(days))

        ax.bar(x - bar_width, sjc_amounts, width=bar_width,
               label='SJC', color='#f5d45f')
        ax.bar(x, pnj_amounts, width=bar_width,
               label='PNJ', color='#df760b')
        ax.bar(x + bar_width, doji_amounts, width=bar_width,
               label='DOJI', color='#743c08')

        ax.set_xlabel('Days of the Week')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Gold Transactions by Type for Current Week')
        ax.set_xticks(x)
        ax.set_xticklabels(date_labels, ha='center')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_sjc = max(sjc_amounts, default=0)
        max_pnj = max(pnj_amounts, default=0)
        max_doji = max(doji_amounts, default=0)
        max_total = max(max_sjc, max_pnj, max_doji)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(lambda x, pos: f'{x:,.0f}'
                                     if x < 1_000_000
                                     else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(sjc_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i - bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#f5d45f')

        for i, v in enumerate(pnj_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount, ha='center',
                    va='bottom', color='#df760b')

        for i, v in enumerate(doji_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i + bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#743c08')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

    def plot_gold_markers_chart_for_this_week(self, parent, transactions):
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        date_labels = [(start_of_week + datetime.timedelta(days=i)
                        ).strftime("%A\n%d/%m/%Y") for i in range(7)]

        sjc_totals = {day: 0 for day in days}
        pnj_totals = {day: 0 for day in days}
        doji_totals = {day: 0 for day in days}

        for transaction in transactions:
            if isinstance(transaction, GoldTransaction):
                transaction_date = datetime.date(
                    transaction._year, transaction._month, transaction._day)
                day_of_week = transaction_date.strftime('%A')
                if day_of_week in sjc_totals:
                    if transaction._gold_type == GoldType.SJC:
                        sjc_totals[day_of_week] += transaction._total_amount
                    elif transaction._gold_type == GoldType.PNJ:
                        pnj_totals[day_of_week] += transaction._total_amount
                    elif transaction._gold_type == GoldType.DOJI:
                        doji_totals[day_of_week] += transaction._total_amount

        sjc_amounts = [sjc_totals[day] for day in days]
        pnj_amounts = [pnj_totals[day] for day in days]
        doji_amounts = [doji_totals[day] for day in days]

        fig, ax = plt.subplots()

        ax.plot(date_labels, sjc_amounts, marker='o',
                linestyle='-', label='SJC', color='#f5d45f')
        ax.plot(date_labels, pnj_amounts, marker='o',
                linestyle='-', label='PNJ', color='#df760b')
        ax.plot(date_labels, doji_amounts, marker='o',
                linestyle='-', label='DOJI', color='#743c08')

        ax.set_xlabel('Days of the Week')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Gold Transactions by Type for Current Week')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_sjc = max(sjc_amounts, default=0)
        max_pnj = max(pnj_amounts, default=0)
        max_doji = max(doji_amounts, default=0)
        max_total = max(max_sjc, max_pnj, max_doji)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(sjc_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#f5d45f')

        for i, v in enumerate(pnj_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#df760b')

        for i, v in enumerate(doji_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#743c08')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

    def plot_currency_bar_chart_for_this_week(self, parent, transactions):
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        date_labels = [(start_of_week + datetime.timedelta(days=i)
                        ).strftime("%A\n%d/%m/%Y") for i in range(7)]

        vnd_totals = {day: 0 for day in days}
        usd_totals = {day: 0 for day in days}
        eur_totals = {day: 0 for day in days}

        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                transaction_date = datetime.date(
                    transaction._year, transaction._month, transaction._day)
                day_of_week = transaction_date.strftime('%A')
                if day_of_week in vnd_totals:
                    if transaction._currency_type == CurrencyType.VND:
                        vnd_totals[day_of_week] += transaction._total_amount
                    elif transaction._currency_type == CurrencyType.USD:
                        usd_totals[day_of_week] += transaction._total_amount
                    elif transaction._currency_type == CurrencyType.EUR:
                        eur_totals[day_of_week] += transaction._total_amount

        vnd_amounts = [vnd_totals[day] for day in days]
        usd_amounts = [usd_totals[day] for day in days]
        eur_amounts = [eur_totals[day] for day in days]

        fig, ax = plt.subplots()
        bar_width = 0.2
        x = np.arange(len(days))

        ax.bar(x - bar_width, vnd_amounts, width=bar_width,
               label='VND', color='#006769')
        ax.bar(x, usd_amounts, width=bar_width, label='USD', color='#2ea64d')
        ax.bar(x + bar_width, eur_amounts, width=bar_width,
               label='EUR', color='#9dde8b')

        ax.set_xlabel('Days of the Week')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Currency Transactions by Type for Current Week')
        ax.set_xticks(x)
        ax.set_xticklabels(date_labels, ha='center')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_vnd = max(vnd_amounts, default=0)
        max_usd = max(usd_amounts, default=0)
        max_eur = max(eur_amounts, default=0)
        max_total = max(max_vnd, max_usd, max_eur)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(vnd_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i - bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#006769')

        for i, v in enumerate(usd_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#2ea64d')

        for i, v in enumerate(eur_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i + bar_width, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#9dde8b')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

    def plot_currency_markers_chart_for_this_week(self, parent, transactions):
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        date_labels = [(start_of_week + datetime.timedelta(days=i)
                        ).strftime("%A\n%d/%m/%Y") for i in range(7)]

        vnd_totals = {day: 0 for day in days}
        usd_totals = {day: 0 for day in days}
        eur_totals = {day: 0 for day in days}

        for transaction in transactions:
            if isinstance(transaction, CurrencyTransaction):
                transaction_date = datetime.date(
                    transaction._year, transaction._month, transaction._day)
                day_of_week = transaction_date.strftime('%A')
                if day_of_week in vnd_totals:
                    if transaction._currency_type == CurrencyType.VND:
                        vnd_totals[day_of_week] += transaction._total_amount
                    elif transaction._currency_type == CurrencyType.USD:
                        usd_totals[day_of_week] += transaction._total_amount
                    elif transaction._currency_type == CurrencyType.EUR:
                        eur_totals[day_of_week] += transaction._total_amount

        vnd_amounts = [vnd_totals[day] for day in days]
        usd_amounts = [usd_totals[day] for day in days]
        eur_amounts = [eur_totals[day] for day in days]

        fig, ax = plt.subplots()

        ax.plot(date_labels, vnd_amounts, marker='o',
                linestyle='-', label='VND', color='#006769')
        ax.plot(date_labels, usd_amounts, marker='o',
                linestyle='-', label='USD', color='#2ea64d')
        ax.plot(date_labels, eur_amounts, marker='o',
                linestyle='-', label='EUR', color='#9dde8b')

        ax.set_xlabel('Days of the Week')
        ax.set_ylabel('Total Amount (VND)')
        ax.set_title('Currency Transactions by Type for Current Week')

        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        max_vnd = max(vnd_amounts, default=0)
        max_usd = max(usd_amounts, default=0)
        max_eur = max(eur_amounts, default=0)
        max_total = max(max_vnd, max_usd, max_eur)

        if max_total > 0:
            max_ticks = min(5, max(2, int(max_total // 1_000_000) + 1))
        else:
            max_ticks = 2

        ax.yaxis.set_major_locator(MaxNLocator(nbins=max_ticks, integer=True))
        ax.yaxis.set_major_formatter(
            lambda x, pos: f'{x:,.0f}'
            if x < 1_000_000 else f'{int(x // 1_000_000)}M')

        for i, v in enumerate(vnd_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#006769')

        for i, v in enumerate(usd_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#2ea64d')

        for i, v in enumerate(eur_amounts):
            formatted_amount = self.format_price_number(v)
            ax.text(i, v + 0.01, formatted_amount,
                    ha='center', va='bottom', color='#9dde8b')

        fig.subplots_adjust(bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=(0, 20), fill="x")

    def get_total_amount_per_week(self, transactions, weeks):
        totals = np.zeros(len(weeks))
        transaction_dates = np.array(
            [datetime.date(txn._year, txn._month, txn._day)
             for txn in transactions])
        transaction_amounts = np.array(
            [txn._total_amount for txn in transactions])

        for i, (start, end) in enumerate(weeks):
            mask = (transaction_dates >= start) & (transaction_dates <= end)
            totals[i] = np.sum(transaction_amounts[mask])

        return totals.tolist()

    def create_gold_transaction_treeview(self, frame):
        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Unit Price (VND/tael)",
            "Quantity (tael)", "Gold Type", "Total Amount (VND)"
        ), show="headings", height=4)

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

        treeview.column("Transaction Code", width=100)
        treeview.column("Transaction Date", width=100)
        treeview.column("Unit Price (VND/tael)", width=100)
        treeview.column("Quantity (tael)", width=100)
        treeview.column("Gold Type", width=100)
        treeview.column("Total Amount (VND)", width=100)

        return treeview

    def create_currency_transaction_treeview(self, frame):
        treeview_style = ttk.Style()
        treeview_style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"))
        treeview_style.configure("Treeview", rowheight=25)

        treeview = ttk.Treeview(frame, columns=(
            "Transaction Code",
            "Transaction Date",
            "Quantity",
            "Currency Type", "Exchange Rate (VND)", "Total Amount (VND)"
        ), show="headings", height=4)

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

        treeview.column("Transaction Code", width=100)
        treeview.column("Transaction Date", width=100)
        treeview.column("Quantity", width=100)
        treeview.column("Currency Type", width=100)
        treeview.column("Exchange Rate (VND)", width=100)
        treeview.column("Total Amount (VND)", width=100)

        return treeview

    def populate_treeview_with_gold_transactions(self, treeview,
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

    def populate_treeview_with_currency_transactions(self, treeview,
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

    def format_price_number(self, total_amount):
        if '.' in str(total_amount):
            integer_part, decimal_part = str(total_amount).split(".")
        else:
            integer_part, decimal_part = str(total_amount), '00'
        formatted_integer_part = "{:,.0f}".format(float(integer_part))
        formatted_total_amount = "{}.{}".format(
            formatted_integer_part, decimal_part)
        return formatted_total_amount

    def open_total_details_window(self, transactions):
        if self.total_details_window is None \
            or not self.total_details_window \
                .winfo_exists():
            self.total_details_window \
                = TotalDetailsWindow(
                    self, transactions=transactions)
            self.total_details_window.after(
                10, self.total_details_window.lift)
        else:
            self.total_details_window.focus()

    def open_statistics_details_month_window(self, transactions):
        if self.statistics_details_month_window is None \
            or not self.statistics_details_month_window \
                .winfo_exists():
            self.statistics_details_month_window \
                = StatisticsDetailsMonthWindow(
                    self, transactions=transactions)
            self.statistics_details_month_window.after(
                10, self.statistics_details_month_window.lift)
        else:
            self.statistics_details_month_window.focus()

    def open_statistics_details_week_window(self, transactions):
        if self.statistics_details_week_window is None \
            or not self.statistics_details_week_window \
                .winfo_exists():
            self.statistics_details_week_window \
                = StatisticsDetailsWeekWindow(
                    self, transactions=transactions)
            self.statistics_details_week_window.after(
                10, self.statistics_details_week_window.lift)
        else:
            self.statistics_details_week_window.focus()
