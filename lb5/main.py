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
        self.ac = init_alternative_comparisons()
        self.calculated_alternatives: List[AlternativeComparison] = []

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
        next_step.bind("<Button-1>", self.go_to_alternatives_comparison)

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
        
    def compare_alternatives(self):
        self.calculated_alternatives.append(self.ac[0])
        self.ac.pop(0)

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack()

        criterion_name = tk.Label(self.table_frame, text=self.calculated_alternatives[-1].criteria_name)
        criterion_name.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        calculate_alternative_button = tk.Button(
            self.root, text="Порахувати", font=default_font)
        next_alternative_button = tk.Button(
            self.root, text="Наступний крок", font=default_font)

        calculate_alternative_button.pack(side=tk.LEFT, anchor=tk.NW)
        next_alternative_button.pack(side=tk.LEFT, anchor=tk.NW)

        calculate_alternative_button.bind("<Button-1>", self.calculate_alternative_comparison)
        next_alternative_button.bind("<Button-1>", self.next_alternatives_comparison)

        for i, crit in enumerate(ALTERNATIVES):
            # Create labels for criteria names
            label_row = tk.Label(self.table_frame, text=crit)
            label_row.grid(row=i+1, column=0, pady=5, padx=10, sticky="w")

            label_column = tk.Label(self.table_frame, text=crit)
            label_column.grid(row=0, column=i+1, pady=5, padx=10)

            for j, _ in enumerate(ALTERNATIVES):
                # If below the diagonal, create dropdowns
                if i < j:
                    var = tk.StringVar()
                    dropdown = ttk.Combobox(
                        self.table_frame, textvariable=var, values=list(STR_TO_SCALE.keys()))
                    dropdown.grid(row=i+1, column=j+1)
                    dropdown.bind("<<ComboboxSelected>>", lambda event, row=i,
                                  column=j: self.handle_alternative_dropdown(event, row, column))
                # If on the diagonal, set value to 1 and update the NumPy array
                elif i == j:
                    label = tk.Label(self.table_frame, text="1")
                    label.grid(row=i+1, column=j+1, pady=5, padx=10)
                    self.calculated_alternatives[-1].comparison_table[i, j] = 1
                # If above the diagonal, just display a label
                else:
                    label = tk.Label(self.table_frame, text="")
                    label.grid(row=i+1, column=j+1)

        self_vector_label = tk.Label(self.table_frame, text="Власний вектор")
        alt_weight_label = tk.Label(self.table_frame, text="Вага альтернатив")
        self_vector_label.grid(row=0, column=len(
            ALTERNATIVES) + 2, pady=5, padx=10, sticky="w")
        alt_weight_label.grid(row=0, column=len(
            ALTERNATIVES) + 3, pady=5, padx=10, sticky="w")

    def handle_dropdown(self, event, row, column):
        # Get the selected value from the dropdown
        selected_value = event.widget.get()
        # Update the corresponding cell below the diagonal with the value from SCALE
        self.cc.criteria_comparisons[row, column] = STR_TO_SCALE[selected_value]
        # Update the corresponding cell above the diagonal as reciprocal
        self.cc.criteria_comparisons[column, row] = float(
            INVERTED_SCALE[STR_TO_SCALE[selected_value]])

        self.draw_comparison_label(column, row, selected_value)

    def handle_alternative_dropdown(self, event, row, column):
        # Get the selected value from the dropdown
        selected_value = event.widget.get()
        # Update the corresponding cell below the diagonal with the value from SCALE
        self.calculated_alternatives[-1].comparison_table[row, column] = STR_TO_SCALE[selected_value]
        # Update the corresponding cell above the diagonal as reciprocal
        self.calculated_alternatives[-1].comparison_table[column, row] = float(
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

    def draw_alternative_calculation(self):
        # Удаление существующих меток в колонке "Власний вектор"
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) == 1 and int(widget.grid_info()["column"]) == len(ALTERNATIVES) + 2:
                widget.grid_forget()

        # Удаление существующих меток в колонке "Вага альтернатив"
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) == 1 and int(widget.grid_info()["column"]) == len(ALTERNATIVES) + 3:
                widget.grid_forget()

        # Добавление новых меток в колонке "Власний вектор" с обновленными значениями
        for i, value in enumerate(self.calculated_alternatives[-1].self_vector):
            label = tk.Label(self.table_frame, text="{:.4f}".format(value))
            label.grid(row=i+1, column=len(ALTERNATIVES) + 2, pady=5, padx=10)

        # Добавление новых меток в колонке "Вага альтернатив" с обновленными значениями
        for i, weight in enumerate(self.calculated_alternatives[-1].weight_vector):
            label = tk.Label(self.table_frame, text="{:.4f}".format(weight))
            label.grid(row=i+1, column=len(ALTERNATIVES) + 3, pady=5, padx=10)

    def go_to_alternatives_comparison(self, event):
        print(len(self.cc.self_vector), len(self.cc.criteria_weight), len(CRITERIA))
        if check_for_zeros(self.cc.criteria_comparisons):
            messagebox.showwarning("Помилка", "Заповніть усі значення та натисніть кнопку порахувати перед тим, як перейти до наступного кроку")
        elif len(self.cc.self_vector) != len(CRITERIA) or len(self.cc.criteria_weight) != len(CRITERIA):
            messagebox.showwarning("Помилка", "Натисніть кнопку порахувати перед тим, як перейти до наступного кроку")
        else:
            self.clear_window()
            self.compare_alternatives()

    def next_alternatives_comparison(self, event):
        print(len(self.calculated_alternatives[-1].self_vector), len(self.calculated_alternatives[-1].weight_vector), len(ALTERNATIVES))
        if check_for_zeros(self.calculated_alternatives[-1].comparison_table):
            messagebox.showwarning("Помилка", "Заповніть усі значення та натисніть кнопку порахувати перед тим, як перейти до наступного кроку")
        elif len(self.calculated_alternatives[-1].comparison_table) != len(ALTERNATIVES) or len(self.calculated_alternatives[-1].weight_vector) != len(ALTERNATIVES):
            messagebox.showwarning("Помилка", "Натисніть кнопку порахувати перед тим, як перейти до наступного кроку")
        else:
            self.clear_window()
            # TODO add final output
            if len(self.ac) == 0:
                self.calculate_results()
                self.draw_results()
            else:
                self.compare_alternatives()

    def calculate_alternative_comparison(self, event):
        self.calculated_alternatives[-1].self_vector = []
        self.calculated_alternatives[-1].weight_vector = []
        if not check_for_zeros(self.calculated_alternatives[-1].comparison_table):
            for values in self.calculated_alternatives[-1].comparison_table:
                self_vector = np.power(np.prod(values), 1 / len(ALTERNATIVES))
                self.calculated_alternatives[-1].self_vector.append(self_vector)

            for value in self.calculated_alternatives[-1].self_vector:
                weight = value / np.sum(self.calculated_alternatives[-1].self_vector)
                self.calculated_alternatives[-1].weight_vector.append(weight)

            self.draw_alternative_calculation()

            print(self.calculated_alternatives[-1].self_vector)
            print(self.calculated_alternatives[-1].weight_vector)
        else:
            messagebox.showwarning("Помилка", "Заповніть усі значення")

    def calculate_results(self):
        criteria_weight = np.array(self.cc.criteria_weight)
        alternative_weights = []
        for ac in self.calculated_alternatives:
            alternative_weight = np.array(ac.weight_vector)
            alternative_weights.append(alternative_weight)

        print(np.dot(criteria_weight, np.array(alternative_weights)))

    def init_window(self):
        self.compare_criteria()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
