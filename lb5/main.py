import tkinter as tk
from tkinter import ttk
from typing import Literal
import numpy as np
from HierarchyAnalysis import HierarchyAnalysis
# from utils import *
from _consts import *

default_font = ("Helvetica", 10)


class App:
    def __init__(self, root: tk.Tk):
        self.mc = HierarchyAnalysis(CRITERIA, ALTERNATIVES)

        self.root = root
        self.root.title("Метод аналізу ієрархій")

        self.init_window()

    def pack_label(self, text: str, pady: int, padx: int,
                   anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]):
        label = tk.Label(self.root, text=text)
        label.pack(pady=pady, padx=padx, anchor=anchor)
        return label

    def compare_criteria(self):
        # Create a frame to contain the table
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack()

        # Create a NumPy array to hold the values
        self.criteria_array = np.zeros((len(CRITERIA), len(CRITERIA)))

        # Loop through criteria to create rows and columns
        for i, crit in enumerate(CRITERIA):
            # Create labels for criteria names
            label_row = tk.Label(self.table_frame, text=crit)
            label_row.grid(row=i+1, column=0, pady=5, padx=10, sticky="w")

            label_column = tk.Label(self.table_frame, text=crit)
            label_column.grid(row=0, column=i+1, pady=5, padx=10)

            for j, _ in enumerate(CRITERIA):
                # If below the diagonal, create dropdowns
                if i < j:
                    var = tk.StringVar()
                    dropdown = ttk.Combobox(
                        self.table_frame, textvariable=var, values=list(STR_TO_SCALE.keys()))
                    dropdown.grid(row=i+1, column=j+1)
                    dropdown.bind("<<ComboboxSelected>>", lambda event, row=i,
                                  column=j: self.handle_dropdown(event, row, column))
                # If on the diagonal, set value to 1 and update the NumPy array
                elif i == j:
                    label = tk.Label(self.table_frame, text="1")
                    label.grid(row=i+1, column=j+1, pady=5, padx=10)
                    self.criteria_array[i, j] = 1
                # If above the diagonal, just display a label
                else:
                    label = tk.Label(self.table_frame, text="")
                    label.grid(row=i+1, column=j+1)

    def handle_dropdown(self, event, row, column):
        # Get the selected value from the dropdown
        selected_value = event.widget.get()
        # Update the corresponding cell below the diagonal with the value from SCALE
        self.criteria_array[row, column] = STR_TO_SCALE[selected_value]
        # Update the corresponding cell above the diagonal as reciprocal
        self.criteria_array[column, row] = float(
            INVERTED_SCALE[STR_TO_SCALE[selected_value]])

        # Remove the previous label if it exists
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) == column+1 and int(widget.grid_info()["column"]) == row+1:
                widget.grid_forget()

        # Add the new label below the diagonal with the new value
        label = tk.Label(
            self.table_frame, text=SCALE_TO_STR[INVERTED_SCALE[STR_TO_SCALE[selected_value]]])
        label.grid(row=column+1, column=row+1, pady=5, padx=10)
        print(self.criteria_array)

    def init_window(self):
        self.compare_criteria()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
