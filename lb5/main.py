import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
from HierarchyAnalysis import HierarchyAnalysis
from CriteriaComparison import CriteriaComparison
from utils import *
from _consts import *

default_font = ("Helvetica", 10)


class App:
    def __init__(self, root: tk.Tk):
        self.mc = HierarchyAnalysis(CRITERIA, ALTERNATIVES)
        self.cc = CriteriaComparison()

        self.root = root
        self.root.title("Метод аналізу ієрархій")

        self.init_window()

    def compare_criteria(self):
        # Create a frame to contain the table
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack()

        calculate_button = tk.Button(
            self.root, text="Порахувати", font=default_font)
        next_step = tk.Button(
            self.root, text="Наступний крок", font=default_font)

        calculate_button.pack(side=tk.LEFT, anchor=tk.NW)
        next_step.pack(side=tk.LEFT, anchor=tk.NW)

        calculate_button.bind("<Button-1>", self.calculate_criteria_comparison)

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
                    self.cc.criteria_comparisons[i, j] = 1
                # If above the diagonal, just display a label
                else:
                    label = tk.Label(self.table_frame, text="")
                    label.grid(row=i+1, column=j+1)

        self_vector_label = tk.Label(self.table_frame, text="Власний вектор")
        alt_weight_label = tk.Label(self.table_frame, text="Вага альтернатив")
        self_vector_label.grid(row=0, column=len(
            CRITERIA) + 2, pady=5, padx=10, sticky="w")
        alt_weight_label.grid(row=0, column=len(
            CRITERIA) + 3, pady=5, padx=10, sticky="w")

    def handle_dropdown(self, event, row, column):
        # Get the selected value from the dropdown
        selected_value = event.widget.get()
        # Update the corresponding cell below the diagonal with the value from SCALE
        self.cc.criteria_comparisons[row,
                                     column] = STR_TO_SCALE[selected_value]
        # Update the corresponding cell above the diagonal as reciprocal
        self.cc.criteria_comparisons[column, row] = float(
            INVERTED_SCALE[STR_TO_SCALE[selected_value]])

        self.draw_comparison_label(column, row, selected_value)

    def calculate_criteria_comparison(self, event):
        self.cc.self_vector = []
        self.cc.criteria_weight = []
        if not check_for_zeros(self.cc.criteria_comparisons):
            for values in self.cc.criteria_comparisons:
                self_vector = np.power(np.prod(values), 1 / len(CRITERIA))
                self.cc.self_vector.append(self_vector)

            for value in self.cc.self_vector:
                weight = value / np.sum(self.cc.self_vector)
                self.cc.criteria_weight.append(weight)

            self.draw_criteria_calculation()

            print(self.cc.self_vector)
            print(self.cc.criteria_weight)
        else:
            messagebox.showwarning("Помилка", "Заповніть усі значення")

    def draw_comparison_label(self, column, row, selected_value):
        # Remove the previous label if it exists
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) == column+1 and int(widget.grid_info()["column"]) == row+1:
                widget.grid_forget()

        # Add the new label below the diagonal with the new value
        label = tk.Label(
            self.table_frame, text=SCALE_TO_STR[INVERTED_SCALE[STR_TO_SCALE[selected_value]]])
        label.grid(row=column+1, column=row+1, pady=5, padx=10)

    def draw_criteria_calculation(self):
        # Удаление существующих меток в колонке "Власний вектор"
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) == 1 and int(widget.grid_info()["column"]) == len(CRITERIA) + 2:
                widget.grid_forget()

        # Удаление существующих меток в колонке "Вага альтернатив"
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) == 1 and int(widget.grid_info()["column"]) == len(CRITERIA) + 3:
                widget.grid_forget()

        # Добавление новых меток в колонке "Власний вектор" с обновленными значениями
        for i, value in enumerate(self.cc.self_vector):
            label = tk.Label(self.table_frame, text="{:.4f}".format(value))
            label.grid(row=i+1, column=len(CRITERIA) + 2, pady=5, padx=10)

        # Добавление новых меток в колонке "Вага альтернатив" с обновленными значениями
        for i, weight in enumerate(self.cc.criteria_weight):
            label = tk.Label(self.table_frame, text="{:.4f}".format(weight))
            label.grid(row=i+1, column=len(CRITERIA) + 3, pady=5, padx=10)

    def init_window(self):
        self.compare_criteria()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
