from pprint import pprint as pp

from utils import execute_round


class RelativeMajority:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.winner = None

        self.find_winner()

    def find_winner(self):
        scores, sorted_scores = execute_round(self.voting_profile)
        self.alternatives_scores = scores
        self.winner = sorted_scores[0][0]

        print("========================== Relative Majority ==========================")
        print("Scores:")
        pp(self.alternatives_scores)
        print("Winner:")
        print(self.winner)
