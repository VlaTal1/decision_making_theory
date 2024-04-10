import tkinter as tk
from tkinter import ttk
from typing import List, Literal
import numpy as np

from OrdinalClassification import OrdinalClassification

criteria = {
    "K1": np.array(['k11', 'k12', 'k13', 'k14']),
    "K2": np.array(['k21', 'k22', 'k23', 'k24']),
    "K3": np.array(['k31', 'k32', 'k33', 'k34'])
}

chosen_alternative_index = 22


class App:
    def __init__(self, root: tk.Tk):
        self.ord_class = OrdinalClassification(criteria, chosen_alternative_index)
        self.ord_class.process()

        self.root = root
        self.root.title("Порядкова класифікація альтернатив")
        self.init_window()

    def create_header(self):
        hypothetical_amount = self.ord_class.hypothetical_amount()
        best_alternative = self.ord_class.get_best_alternative()
        worst_alternative = self.ord_class.get_worst_alternative()

        self.pack_label(f"Кількість гіпотетично можливих альтернатив: {hypothetical_amount}", 5, 0, tk.W)
        self.pack_label(f"Кількість сформованих альтернатив: {len(self.ord_class.alternatives)}", 5, 0, tk.W)
        self.pack_label(f"Найкраща альтернатива: {best_alternative}", 5, 0, tk.W)
        self.pack_label(f"Найгірша альтернатива: {worst_alternative}", 5, 0, tk.W)

    def create_tab(self, notebook: ttk.Notebook, tab_name: str, data: list[np.ndarray[int, np.dtype]]):
        tab = ttk.Frame(notebook)
        self.create_table(tab, data)
        notebook.add(tab, text=tab_name)

    def create_tabs(self):
        notebook = ttk.Notebook(self.root)

        self.create_tab(notebook, "All Alternatives", self.ord_class.alternatives)
        self.create_tab(notebook, "Better Alternatives", self.ord_class.better)
        self.create_tab(notebook, "Worse Alternatives", self.ord_class.worse)
        self.create_tab(notebook, "Incomparable Alternatives", self.ord_class.incomparable)

        notebook.pack(expand=True, fill=tk.BOTH)

    def create_table(self, tab: ttk.Frame, data: list[np.ndarray[int, np.dtype]]):
        columns = self.ord_class.get_criteria_keys()
        tree = ttk.Treeview(tab, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for row in data:
            values = self.ord_class.criteria_values_by_indices(row)
            tree.insert('', 'end', values=values)

        vsb = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        tree.pack(expand=True, fill=tk.BOTH)

    def create_footer(self):
        recalculated_amount = self.ord_class.calculate_all_alternatives()
        recalculated_amount_text = (f"Сума альтернатив: "
                                    f"{len(self.ord_class.better)} + "
                                    f"{len(self.ord_class.worse)} + "
                                    f"{len(self.ord_class.incomparable)} + 1 = "
                                    f"{recalculated_amount}")

        self.pack_label(f"Кількість кращих альтернатив: {len(self.ord_class.better)}", 5, 0, tk.W)
        self.pack_label(f"Кількість гірших альтернатив: {len(self.ord_class.worse)}", 5, 0, tk.W)
        self.pack_label(f"Кількість непорівняних альтернатив: {len(self.ord_class.incomparable)}", 5, 0, tk.W)
        self.pack_label(recalculated_amount_text, 5, 0, tk.W)

    def pack_label(self, text: str, pady: int, padx: int,
                   anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]):
        label = tk.Label(self.root, text=text)
        label.pack(pady=pady, padx=padx, anchor=anchor)

    def init_window(self):
        self.create_header()
        self.create_tabs()
        self.create_footer()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
