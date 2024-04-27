import tkinter as tk
from tkinter import ttk
import numpy as np
from _consts import CRITERIA


class CriteriaComparison:
    def __init__(self):
        self.criteria_comparisons = np.zeros((len(CRITERIA), len(CRITERIA)))
        self.self_vector = []
        self.criteria_weight = []

    def create_table(self, parent):
        table = ttk.Treeview(parent)

        # Define columns
        table["columns"] = CRITERIA + \
            ["Власний вектор", "Вага альтернатив"]

        # Format columns
        table.column("#0", width=100, minwidth=100)
        for column in table["columns"]:
            table.column(column, width=100, minwidth=100)
            table.heading(column, text=column)

        # Insert data
        for i, criteria in enumerate(CRITERIA):
            table.insert("", i, text=criteria, values=list(
                self.criteria_comparisons[i]) + [self.self_vector[i], self.criteria_weight[i]])

        return table
