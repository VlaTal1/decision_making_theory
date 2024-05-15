import tkinter as tk
from pprint import pprint as pp

from _consts import H1, H2, DEF_FONT
from utils import execute_round, get_winners_text


class RelativeMajority:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.winner = None
        self.winners = {}

        self.find_winner()

    def get_method_name(self):
        return 'Відносна більшість'

    def find_winner(self):
        scores, sorted_scores = execute_round(self.voting_profile)
        self.alternatives_scores = sorted_scores
        winner_score = sorted_scores[0][1]

        for alternative, score in sorted_scores:
            if score == winner_score:
                self.winners[alternative] = score

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

        winner_label = tk.Label(relative_frame, text=get_winners_text(self.winners), font=DEF_FONT)
        winner_label.pack(anchor=tk.W, padx=10, pady=5)

        return relative_frame
