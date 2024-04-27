import tkinter as tk
from tkinter import ttk

import numpy as np

from _consts import ALTERNATIVES, SCALE_TO_STR


class AlternativeComparison:
    def __init__(self, criteria_name) -> None:
        self.criteria_name = criteria_name
        self.comparison_table = np.zeros((len(ALTERNATIVES), len(ALTERNATIVES)))
        self.self_vector = []
        self.weight_vector = []
        self.quality_indicator = 0

    def create_table(self, parent):
        table = ttk.Treeview(parent)

        # Define columns
        table["columns"] = list(ALTERNATIVES.keys()) + ["Власний вектор", "Вага альтернатив"]

        # Format columns
        table.column("#0", width=100, minwidth=100, stretch=tk.NO)
        for column in table["columns"]:
            table.column(column, width=100, minwidth=100, stretch=tk.NO)
            table.heading(column, text=column)

        # Insert data
        for i, alternative in enumerate(ALTERNATIVES):
            comparison_table_str = []
            for comparison in self.comparison_table[i]:
                comparison_table_str.append(SCALE_TO_STR[str(comparison)])
            table.insert("", i, text=alternative,
                         values=list(comparison_table_str) + [round(self.self_vector[i], 2),
                                                              round(self.weight_vector[i], 2)])

        return table
