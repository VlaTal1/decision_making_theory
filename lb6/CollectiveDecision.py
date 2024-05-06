import tkinter as tk
from pprint import pprint as pp
from tkinter import ttk

from AbsoluteMajority import AbsoluteMajority
from BordRule import BordRule
from CondorseRule import CondorseRule
from RelativeMajority import RelativeMajority
from _consts import DEF_FONT, H1


class CollectiveDecision:
    def __init__(self):
        self.original_data = None
        self.voting_profile = {}

        self.rm = None
        self.am = None
        self.br = None
        self.cr = None

    def process_data(self, data):
        self.original_data = data

        for row in data:
            row_tuple = tuple(row)
            if row_tuple in self.voting_profile:
                self.voting_profile[row_tuple] += 1
            else:
                self.voting_profile[row_tuple] = 1

        print(len(self.voting_profile))
        pp(self.voting_profile)

        self.rm = RelativeMajority(self.voting_profile)
        self.am = AbsoluteMajority(self.voting_profile)
        self.br = BordRule(self.voting_profile)
        self.cr = CondorseRule(self.voting_profile)

    def get_frames(self, root):
        frames = [self.get_profile_frame(root), self.rm.get_frame(root), self.am.get_frame(root),
                  self.br.get_frame(root), self.cr.get_frame(root)]
        return frames

    def get_profile_frame(self, root):
        profile_frame = tk.Frame(root)
        comparison_label = tk.Label(profile_frame, text="Профіль голосування", font=H1)
        comparison_label.pack(anchor=tk.W, padx=10, pady=5)
        voting_profile_table = self.get_voting_profile_table(profile_frame)
        voting_profile_table.pack(side=tk.TOP, fill="both", expand=True, anchor=tk.NW)
        return profile_frame

    def get_voting_profile_table(self, frame):
        table_frame = tk.Frame(frame)
        table_frame.pack(padx=10, fill=tk.BOTH, expand=True)

        columns = ["Кількість голосів"]
        for i, _ in enumerate(list(self.voting_profile.keys())[0]):
            columns.append(f"Пріоритет №{i + 1}")

        table = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            table.heading(col, text=col)

        for vote, amount in self.voting_profile.items():
            table.insert("", "end", values=(amount, *vote))

        return table
