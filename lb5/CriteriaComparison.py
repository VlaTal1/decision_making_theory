from tkinter import ttk

import numpy as np

from _consts import CRITERIA, SCALE_TO_STR


class CriteriaComparison:
    def __init__(self):
        self.criteria_comparisons = np.zeros((len(CRITERIA), len(CRITERIA)))
        self.self_vector = []
        self.criteria_weight = []

    def create_table(self, parent):
        table = ttk.Treeview(parent)

        # Define columns
        table["columns"] = CRITERIA + ["Власний вектор", "Вага альтернатив"]

        # Format columns
        table.column("#0", width=100, minwidth=100)
        for column in table["columns"]:
            table.column(column, width=100, minwidth=100)
            table.heading(column, text=column)

        # Insert data
        for i, criteria in enumerate(CRITERIA):
            criteria_comparison_str = []
            for comparison in self.criteria_comparisons[i]:
                criteria_comparison_str.append(SCALE_TO_STR[str(comparison)])
            table.insert("", i, text=criteria, values=list(
                criteria_comparison_str) + [round(self.self_vector[i], 2), round(self.criteria_weight[i], 2)])

        return table
