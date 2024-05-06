import tkinter as tk
from pprint import pprint as pp

from _consts import H1, H2, DEF_FONT
from utils import execute_round


class RelativeMajority:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.winner = None

        self.find_winner()

    def find_winner(self):
        scores, sorted_scores = execute_round(self.voting_profile)
        self.alternatives_scores = sorted_scores
        self.winner = sorted_scores[0][0]

        print("========================== Relative Majority ==========================")
        print("Scores:")
        pp(self.alternatives_scores)
        print("Winner:")
        print(self.winner)

    def get_frame(self, root):
        relative_frame = tk.Frame(root)
        comparison_label = tk.Label(relative_frame, text="Правило відносної більшості", font=H1)
        comparison_label.pack(anchor=tk.W, padx=10, pady=(20, 5))

        results_label = tk.Label(relative_frame, text="Результати", font=H2)
        results_label.pack(anchor=tk.W, padx=10, pady=5)
        for alternative, score in self.alternatives_scores:
            label = tk.Label(relative_frame, text=f"{alternative} = {score}", font=DEF_FONT)
            label.pack(anchor=tk.W, padx=10, pady=5)

        if self.alternatives_scores[0][1] == self.alternatives_scores[1][1]:
            winner_text = f"Альтернативи \"{self.alternatives_scores[0][0]}\" та \"{self.alternatives_scores[1][0]}\" виявились рівноцінно кращими"
        else:
            winner_text = f"Альтернатива \"{self.alternatives_scores[0][0]}\" виявилась кращою"

        winner_label = tk.Label(relative_frame, text=winner_text, font=DEF_FONT)
        winner_label.pack(anchor=tk.W, padx=10, pady=5)

        return relative_frame
