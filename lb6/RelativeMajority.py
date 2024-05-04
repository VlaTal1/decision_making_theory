from utils import sort_scores_desc, init_alternatives_scores, execute_round
from pprint import pprint as pp


class RelativeMajority:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.winner = None

        self.find_winner()

    def find_winner(self):
        scores, winner = execute_round(self.voting_profile)
        self.alternatives_scores = scores
        self.winner = winner

        print(self.alternatives_scores)
        print(self.winner)
