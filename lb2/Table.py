import tkinter as tk
from tkinter import ttk
from typing import List

from Alternative import *


class Table:
    def __init__(self, alternatives: List[Alternative], better_center: List, worse_center: List):
        self.alternatives: List[Alternative] = alternatives
        self.better_center = better_center
        self.worse_center = worse_center
        self.d1 = []
        self.d2 = []
        self.p1 = []
        self.p2 = []
        self.g1 = []
        self.g2 = []
        self.F1 = []
        self.F2 = []
        self.F = []

    # TPr rename to is_done
    def is_all_alternatives_have_class(self):
        class_count = 0
        for a in self.alternatives:
            if a.is_has_class():
                class_count += 1
        if class_count == len(self.alternatives):
            return True

    def calculate_d(self, class_center: list):
        distances = []
        for alt in self.alternatives:
            distance = 0
            for alt_value, class_value in zip(alt.value, class_center):
                distance += abs(alt_value - class_value)
            distances.append(distance)

        return distances

    def calculate_p(self, first_d: int):
        max_d = max(self.d1 + self.d2)
        p = []
        for index, alt in enumerate(self.alternatives):
            d1 = self.d1[index]
            d2 = self.d2[index]
            if first_d == 1:
                if alt.class_number == str(1):
                    p.append(1.0)
                elif alt.class_number == str(2):
                    p.append(0.0)
                else:
                    p.append((max_d - d1) / (max_d - d1 + max_d - d2))
            elif first_d == 2:
                if alt.class_number == str(2):
                    p.append(1.0)
                elif alt.class_number == str(1):
                    p.append(0.0)
                else:
                    p.append((max_d - d2) / (max_d - d1 + max_d - d2))
            else:
                raise ValueError("first_d can only be 1 or 2")
        return p

    def calculate_additional_information(self, class_name: str):
        g = []
        for i, alternative in enumerate(self.alternatives):
            add_inf_count = 0
            if not alternative.is_has_class():
                alternative_np = alternative.get_np_value()
                if class_name == "better":
                    for j, alt in enumerate(self.alternatives):
                        if j == i:
                            break
                        if not alt.is_has_class():
                            np_comb = alt.get_np_value()
                            compare = np_comb <= alternative_np
                            if all(compare):
                                add_inf_count += 1
                elif class_name == "worse":
                    for j, alt in enumerate(self.alternatives[i+1:], start=i+1):
                        if not alt.is_has_class():
                            np_comb = alt.get_np_value()
                            compare = np_comb >= alternative_np
                            if all(compare):
                                add_inf_count += 1
                else:
                    raise ValueError("class_name can only be better or worse")

            g.append(add_inf_count)

        return g

    def calculate_f(self, class_name: str):
        f = []
        for index, alt in enumerate(self.alternatives):
            if class_name == "better":
                f.append(self.p1[index] * self.g1[index])
            elif class_name == "worse":
                f.append(self.p2[index] * self.g2[index])
            else:
                raise ValueError("class_name can only be better or worse")
        return f

    def calculate_informativeness(self):
        for index, alt in enumerate(self.alternatives):
            self.F.append(self.F1[index] + self.F2[index])

    def find_max_first_index(self) -> int:
        max_value = self.F[-1]
        index = len(self.F) - 1
        for i in range(len(self.F) - 1, 0, -1):
            if self.F[i] >= max_value:
                max_value = self.F[i]
                index = i
        return index

    def create_table(self, criteria_names, tab):
        criteria_names.extend(
            ["G", "d1", "d2", "p1", "p2", "g1", "g2", "F1", "F2", "F"])
        columns = criteria_names
        tree = ttk.Treeview(tab, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for index, alt in enumerate(self.alternatives):
            values = [value + 1 for value in alt.value]
            values.append(alt.class_number)
            values.append(round(self.d1[index], 2))
            values.append(round(self.d2[index], 2))
            values.append(round(self.p1[index], 2))
            values.append(round(self.p2[index], 2))
            values.append(round(self.g1[index], 2))
            values.append(round(self.g2[index], 2))
            values.append(round(self.F1[index], 2))
            values.append(round(self.F2[index], 2))
            values.append(round(self.F[index], 2))

            tree.insert('', 'end', values=values)

        vsb = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        tree.pack(expand=True, fill=tk.BOTH)

    def process(self):
        self.d1 = self.calculate_d(self.better_center)
        self.d2 = self.calculate_d(self.worse_center)
        self.p1 = self.calculate_p(1)
        self.p2 = self.calculate_p(2)
        self.g1 = self.calculate_additional_information("better")
        self.g2 = self.calculate_additional_information("worse")
        self.F1 = self.calculate_f("better")
        self.F2 = self.calculate_f("worse")
        self.calculate_informativeness()

        return all(value == 0 for value in self.F)
