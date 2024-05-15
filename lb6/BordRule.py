import tkinter as tk

from _consts import H1, H2, DEF_FONT
from lb6.utils import init_alternatives_scores, sort_scores_desc, get_winners_text


class BordRule:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.winner = None
        self.winners = {}

        self.find_winner()

    def get_method_name(self):
        return 'Правило борда'

    def find_winner(self):
        alternatives_scores = init_alternatives_scores(list(self.voting_profile.keys())[0])
        alternatives = list(alternatives_scores.keys())
        for alternative in alternatives:
            for vote, amount in self.voting_profile.items():
                for i, value in enumerate(vote):
                    if value == alternative:
                        alternatives_scores[alternative] += amount * (len(vote) - i - 1)

        sorted_scores = sort_scores_desc(alternatives_scores)
        self.alternatives_scores = sorted_scores
        self.winner = sorted_scores[0][0]

        winner_score = sorted_scores[0][1]
        for alternative, score in sorted_scores:
            if score == winner_score:
                self.winners[alternative] = score

        print("========================== Bord Rule ==========================")
        print("Scores:")
        print(alternatives_scores)
        print("Winner:")
        print(self.winner)

    def get_frame(self, root):
        bord_frame = tk.Frame(root)
        comparison_label = tk.Label(bord_frame, text="Правило Борда", font=H1)
        comparison_label.pack(anchor=tk.W, padx=10, pady=(20, 5))

        results_label = tk.Label(bord_frame, text="Результати", font=H2)
        results_label.pack(anchor=tk.W, padx=10, pady=5)
        for alternative, score in self.alternatives_scores:
            label = tk.Label(bord_frame, text=f"{alternative} = {score}", font=DEF_FONT)
            label.pack(anchor=tk.W, padx=10, pady=5)

        winner_label = tk.Label(bord_frame, text=get_winners_text(self.winners), font=DEF_FONT)
        winner_label.pack(anchor=tk.W, padx=10, pady=5)

        return bord_frame
