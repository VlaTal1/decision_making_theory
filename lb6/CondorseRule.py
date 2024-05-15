import tkinter as tk
from pprint import pprint as pp

from _consts import H1, H2, DEF_FONT
from lb6.utils import init_alternatives_scores, create_combinations, filter_votes, execute_round, sort_scores_desc


class CondorseRule:
    def __init__(self, voting_profile):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.comparisons_results = []
        self.winner = None
        self.winners = {}

        self.find_winner()

    def find_winner(self):
        print("========================== Condorse Rule ==========================")
        alternatives_scores = init_alternatives_scores(list(self.voting_profile.keys())[0])
        comparisons = create_combinations(list(alternatives_scores.keys()))
        for combination in comparisons:
            filtered_votes = filter_votes(self.voting_profile, list(combination))
            scores, sorted_scores = execute_round(filtered_votes)
            self.comparisons_results.append(sorted_scores)
            print(combination, sorted_scores)
            alternatives_scores[sorted_scores[0][0]] += 1
            if sorted_scores[0][1] == sorted_scores[1][1]:
                alternatives_scores[sorted_scores[1][0]] += 1

        sorted_scores = sort_scores_desc(alternatives_scores)
        self.alternatives_scores = sorted_scores
        self.winner = sorted_scores[0][0]

        winner_score = sorted_scores[0][1]
        for alternative, score in sorted_scores:
            if score == winner_score:
                self.winners[alternative] = score

        print("Scores:")
        pp(self.alternatives_scores)
        print("Winner:")
        print(self.winner)

    def get_frame(self, root):
        condorse_frame = tk.Frame(root)
        comparison_label = tk.Label(condorse_frame, text="Правило Кондорсе", font=H1)
        comparison_label.pack(anchor=tk.W, padx=10, pady=(20, 5))

        for res in self.comparisons_results:
            label = tk.Label(condorse_frame, text=f"{res[1][0]} : {res[0][0]}", font=H2)
            label.pack(anchor=tk.W, padx=10, pady=5)

            for alternative, score in res:
                label = tk.Label(condorse_frame, text=f"{alternative} = {score}", font=DEF_FONT)
                label.pack(anchor=tk.W, padx=10, pady=5)

            if res[0][1] == res[1][1]:
                duel_winner = f"Альтернативи \"{res[0][0]}\" та \"{res[1][0]}\" виявились рівноцінно кращими"
            else:
                duel_winner = f"Альтернатива \"{res[0][0]}\" виявилась кращою"

            duel_winne_label = tk.Label(condorse_frame, text=duel_winner, font=DEF_FONT)
            duel_winne_label.pack(anchor=tk.W, padx=10, pady=5)

        results_label = tk.Label(condorse_frame, text="Результати", font=H2)
        results_label.pack(anchor=tk.W, padx=10, pady=5)
        for alternative, score in self.alternatives_scores:
            label = tk.Label(condorse_frame, text=f"{alternative} = {score}", font=DEF_FONT)
            label.pack(anchor=tk.W, padx=10, pady=5)

        if len(list(self.winners.keys())) > 1:
            winner_text = 'Альтернативи ' + ', '.join(list(self.winners.keys())) + f' виявились рівносильними з кількістю очків {self.alternatives_scores[0][1]}'
        else:
            winner_text = f"Альтернатива \"{self.alternatives_scores[0][0]}\" виявилась кращою"

        winner_label = tk.Label(condorse_frame, text=winner_text, font=DEF_FONT)
        winner_label.pack(anchor=tk.W, padx=10, pady=5)

        return condorse_frame
