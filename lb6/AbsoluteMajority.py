import tkinter as tk
from pprint import pprint as pp

from _consts import H1, H2, DEF_FONT
from utils import init_alternatives_scores, execute_round, filter_votes, get_winners_text


class AbsoluteMajority:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.first_round_scores = init_alternatives_scores(list(voting_profile.keys())[0])
        self.first_round_winners = []
        self.first_round_winners_dict = {}
        self.second_round_scores = init_alternatives_scores(list(voting_profile.keys())[0])
        self.second_round_profile = {}
        self.second_round_winner = None
        self.second_round_winners_dict = {}

        self.find_winner()

    def get_method_name(self):
        return 'Абсолютна більшість'

    def find_winner(self):
        self.first_round()
        self.second_round()

    def first_round(self):
        scores, sorted_scores = execute_round(self.voting_profile)
        self.first_round_scores = sorted_scores
        self.first_round_winners = [sorted_scores[0][0], sorted_scores[1][0]]

        winner_score = sorted_scores[0][1]

        for alternative, score in sorted_scores:
            if score == winner_score:
                self.first_round_winners_dict[alternative] = score

        print("========================== Absolute Majority ==========================")
        print("First round:")
        print("Scores:")
        pp(self.first_round_scores)
        print("Winners:")
        print(self.first_round_winners)

    def second_round(self):
        filtered_voting_profile = filter_votes(self.voting_profile, self.first_round_winners)

        scores, sorted_scores = execute_round(filtered_voting_profile)

        self.second_round_scores = sorted_scores
        self.second_round_profile = filtered_voting_profile
        self.second_round_winner = sorted_scores[0][0]

        winner_score = sorted_scores[0][1]

        for alternative, score in sorted_scores:
            if score == winner_score:
                self.second_round_winners_dict[alternative] = score

        print("Second round:")
        print("Scores:")
        pp(self.second_round_scores)
        print("Second round profile:")
        pp(self.second_round_profile)
        print("Winner:")
        pp(self.second_round_winner)

    def get_frame(self, root):
        absolute_frame = tk.Frame(root)
        comparison_label = tk.Label(absolute_frame, text="Правило абсолютної більшості", font=H1)
        comparison_label.pack(anchor=tk.W, padx=10, pady=(20, 5))

        first_round_label = tk.Label(absolute_frame, text="Результати першого туру", font=H2)
        first_round_label.pack(anchor=tk.NW, padx=10, pady=5)
        for alternative, score in self.first_round_scores:
            label = tk.Label(absolute_frame, text=f"{alternative} = {score}", font=DEF_FONT)
            label.pack(anchor=tk.W, padx=10, pady=5)

        first_round_winner_label = tk.Label(absolute_frame, text=get_winners_text(self.first_round_winners_dict), font=DEF_FONT)
        first_round_winner_label.pack(anchor=tk.W, padx=10, pady=5)

        second_round_label = tk.Label(absolute_frame, text="Результати другого туру", font=H2)
        second_round_label.pack(anchor=tk.W, padx=10, pady=5)
        for alternative, score in self.second_round_scores:
            label = tk.Label(absolute_frame, text=f"{alternative} = {score}", font=DEF_FONT)
            label.pack(anchor=tk.W, padx=10, pady=5)

        second_round_winner_label = tk.Label(absolute_frame, text=get_winners_text(self.second_round_winners_dict), font=DEF_FONT)
        second_round_winner_label.pack(anchor=tk.W, padx=10, pady=5)

        return absolute_frame
