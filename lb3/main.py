import tkinter as tk
from tkinter import ttk
from typing import Literal
import numpy as np
from MultiCriteria import MultiCriteria
from utils import *
from _consts import *
from Comparison import Comparison

default_font = ("Helvetica", 10)

class App:
    def __init__(self, root: tk.Tk):
        self.mc = MultiCriteria(CRITERIA, ALTERNATIVES)
        self.is_compared_var = tk.BooleanVar(value=False)
        self.comparisons: Comparison = []

        self.root = root
        self.root.title("Впорядкування багатокритеріальних альтернатив")

        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.init_window()

    def pack_label(self, text: str, pady: int, padx: int, 
                   anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]):
        label = tk.Label(self.root, text=text)
        label.pack(pady=pady, padx=padx, anchor=anchor)
        return label

    def compare(self):
        comparisons = list(self.mc.criterion_pairs)

        for comparison in comparisons:
            first_ref1 = self.mc.get_first_ref_by_key(comparison[0])
            first_ref2 = self.mc.get_first_ref_by_key(comparison[1])
            dict_refs = array_to_index_dict(np.vstack((first_ref1, first_ref2)))
            dict_refs_no_zeros = {key: value for key, value in dict_refs.items() if not all(v == 0 for v in value)}
            ref1_no_zeros, ref2_no_zeros = split_dictionary(dict_refs_no_zeros)
            comparison_combinations = combinations(list(ref1_no_zeros.keys()), list(ref2_no_zeros.keys()))
            comparison_dict = array_to_none_dict(comparison_combinations)
            comparison_text = f'{comparison[0]} : {comparison[1]}'
            comparison_label = tk.Label(self.root, text=comparison_text, font=default_font)
            comparison_label.pack(anchor=tk.W)
            
            for comb in comparison_dict.keys():
                comparison_list = comparison_dict_to_sting_list(comparison_dict, dict_refs)
                print(comparison_dict)
                if comparison_dict[comb] == None:
                    ref1 = dict_refs[comb[0]]
                    ref2 = dict_refs[comb[1]]
                    label_ref1 = tk.Label(self.root, text=str(ref_to_str(ref1)), font=default_font)
                    label_ref2 = tk.Label(self.root, text=str(ref_to_str(ref2)), font=default_font)
                    
                    button_greater = tk.Button(self.root, text=">", font=default_font)
                    button_lesser = tk.Button(self.root, text="<", font=default_font)
                    
                    label_ref1.pack(side=tk.LEFT, anchor=tk.NW)
                    button_greater.pack(side=tk.LEFT, anchor=tk.NW)
                    button_lesser.pack(side=tk.LEFT, anchor=tk.NW)
                    label_ref2.pack(side=tk.LEFT, anchor=tk.NW)

                    comparison_list_lables = []
                    for comp in comparison_list:
                        comp_label = tk.Label(self.root, text=comp, font=default_font)
                        comp_label.pack(side=tk.TOP)
                        comparison_list_lables.append(comp_label)

                    button_greater.bind("<Button-1>", lambda event=None, comb=comb: self.handle_greater(comb, comparison_dict, dict_refs))
                    button_lesser.bind("<Button-1>", lambda event=None, comb=comb: self.handle_lesser(comb, comparison_dict, dict_refs))

                    self.root.wait_variable(self.is_compared_var)
                    label_ref1.destroy()
                    label_ref2.destroy()
                    button_greater.destroy()
                    button_lesser.destroy()
                    for comp_label in comparison_list_lables:
                        comp_label.destroy()

            comparison_graph = create_graph(dict_refs, comparison_dict)
            longest_path = find_longest_path(comparison_graph)
            comparison = Comparison(comparison, dict_refs, comparison_dict, comparison_graph, longest_path)
            print(comparison)
            self.comparisons.append(comparison)
            
            self.update_history(comparison_text, ("Helvetica", 12, "bold"))
            comparison_list = comparison_dict_to_sting_list(comparison_dict, dict_refs)
            for comp in comparison_list:
                self.update_history(comp)

            self.update_history(f'Найдовший шлях: {path_to_string_dict(longest_path, dict_refs)}')

            comparison_label.destroy()

        # self.comparisons = [COMPARISON1, COMPARISON2, COMPARISON3]
        
        longest_paths = [comparison.get_longest_path_refs_str() for comparison in self.comparisons]
        final_graph = compose_arrays_to_graph(longest_paths)
        final_path = find_longest_path(final_graph)

        self.update_history(f'ЄПШ: {path_to_string(final_path)}', font=("Helvetica", 12, "bold"))
        final_table = self.mc.calculate_final_table(final_path)
        self.init_table(final_table)

    def init_table(self, final_table):
        columns = ["Альтернатива", "Векторна початкова оцінка", "Векторна оцінка за ЄПШ", "Векторна оцінка за зростанням"]

        table = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            table.heading(col, text=col)

        for alt, values in final_table.items():
            table.insert("", "end", values=(alt, *values))

        table.pack(expand=True, fill="both")

    def update_history(self, text, font=default_font):
        history_label = tk.Label(self.history_frame, text=text, font=font)
        history_label.pack(anchor=tk.W)

    def handle_greater(self, comb, comparison_dict, dict_refs):
        comparison_dict[comb] = '>'
        recalculate_comparison_dict(comparison_dict, comb, '>')
        self.is_compared_var.set(True)

    def handle_lesser(self, comb, comparison_dict, dict_refs):
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
