import tkinter as tk
from tkinter import ttk
from typing import Literal
import numpy as np
from MultiCriteria import MultiCriteria
from utils import *
from _consts import *
from Comparison import Comparison

class App:
    def __init__(self, root: tk.Tk):
        self.mc = MultiCriteria(CRITERIA, ALTERNATIVES)
        self.is_compared_var = tk.BooleanVar(value=False)
        self.comparisons: Comparison = []

        self.root = root
        self.root.title("Впорядкування багатокритеріальних альтернатив")
        self.init_window()

    def pack_label(self, text: str, pady: int, padx: int, 
                   anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]):
        label = tk.Label(self.root, text=text)
        label.pack(pady=pady, padx=padx, anchor=anchor)
        return label

    def create_tab(self, notebook: ttk.Notebook, tab_name: str, data: list[np.ndarray[int, np.dtype]]):
        tab = ttk.Frame(notebook)
        self.create_table(tab, data)
        notebook.add(tab, text=tab_name)

        recalculated_amount = self.ord_class.calculate_all_alternatives()
        recalculated_amount_text = (f"Сума альтернатив: "
                                    f"{len(self.ord_class.better)} + "
                                    f"{len(self.ord_class.worse)} + "
                                    f"{len(self.ord_class.incomparable)} + 1 = "
                                    f"{recalculated_amount}")

        self.pack_label(
            f"Кількість кращих альтернатив: {len(self.ord_class.better)}", 5, 0, tk.W)
        self.pack_label(
            f"Кількість гірших альтернатив: {len(self.ord_class.worse)}", 5, 0, tk.W)
        self.pack_label(
            f"Кількість непорівняних альтернатив: {len(self.ord_class.incomparable)}", 5, 0, tk.W)
        self.pack_label(recalculated_amount_text, 5, 0, tk.W)

    def compare(self):
        comparisons = list(self.mc.criterion_pairs)
        print(self.mc.criterion_pairs)

        for comparison in comparisons:
            first_ref1 = self.mc.get_first_ref_by_key(comparison[0])
            first_ref2 = self.mc.get_first_ref_by_key(comparison[1])
            dict_refs = array_to_index_dict(np.vstack((first_ref1, first_ref2)))
            dict_refs_no_zeros = {key: value for key, value in dict_refs.items() if not all(v == 0 for v in value)}
            ref1_no_zeros, ref2_no_zeros = split_dictionary(dict_refs_no_zeros)
            comparison_combinations = combinations(list(ref1_no_zeros.keys()), list(ref2_no_zeros.keys()))
            comparison_dict = array_to_none_dict(comparison_combinations)
            comparison_label = self.pack_label(f'{comparison[0]} : {comparison[1]}', 5, 0, tk.W)
            
            for comb in comparison_dict.keys():
                print(comparison_dict)
                if comparison_dict[comb] == None:
                    label_ref1 = tk.Label(self.root, text=str(dict_refs[comb[0]]))
                    label_ref2 = tk.Label(self.root, text=str(dict_refs[comb[1]]))
                    
                    button_greater = tk.Button(self.root, text=">")
                    button_lesser = tk.Button(self.root, text="<")
                    
                    label_ref1.pack(side=tk.LEFT)
                    button_greater.pack(side=tk.LEFT)
                    button_lesser.pack(side=tk.LEFT)
                    label_ref2.pack(side=tk.LEFT)

                    button_greater.bind("<Button-1>", lambda event=None, comb=comb: self.handle_greater(comb, comparison_dict))
                    button_lesser.bind("<Button-1>", lambda event=None, comb=comb: self.handle_lesser(comb, comparison_dict))

                    self.root.wait_variable(self.is_compared_var)
                    label_ref1.destroy()
                    label_ref2.destroy()
                    button_greater.destroy()
                    button_lesser.destroy()

            comparison_graph = create_graph(dict_refs, comparison_dict)
            longest_path = find_longest_path(comparison_graph)
            comparison = Comparison(comparison, dict_refs, comparison_dict, comparison_graph, longest_path)
            print(comparison)
            self.comparisons.append(comparison)

            comparison_label.destroy()

        # self.comparisons = [COMPARISON1, COMPARISON2, COMPARISON3]
        
        longest_paths = [comparison.get_longest_path_refs_str() for comparison in self.comparisons]
        final_graph = compose_arrays_to_graph(longest_paths)
        final_path = find_longest_path(final_graph)
        print(longest_paths)
        print(final_path)

        print(self.mc.calculate_final_table(final_path))

    def handle_greater(self, comb, comparison_dict):
        comparison_dict[comb] = '>'
        recalculate_comparison_dict(comparison_dict, comb, '>')
        self.is_compared_var.set(True)

    def handle_lesser(self, comb, comparison_dict):
        comparison_dict[comb] = '<'
        recalculate_comparison_dict(comparison_dict, comb, '<')
        self.is_compared_var.set(True)

    def init_window(self):
        self.compare()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
