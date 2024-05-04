from pprint import pprint as pp

from utils import execute_round


class RelativeMajority:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.winner = None

        self.find_winner()

    def find_winner(self):
        scores, _, winner = execute_round(self.voting_profile)
        self.alternatives_scores = scores
        self.winner = winner

        pp(self.alternatives_scores)
        print(self.winner)
