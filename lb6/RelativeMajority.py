from utils import sort_scores_desc, init_alternatives_scores
from pprint import pprint as pp


class RelativeMajority:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.alternatives_scores = init_alternatives_scores(list(voting_profile.keys())[0])
        self.winner = None

        self.find_winner()

    def find_winner(self):
        for vote, amount in self.voting_profile.items():
            alt = vote[0]
            self.alternatives_scores[alt] += amount

        sorted_scores = sort_scores_desc(self.alternatives_scores)
        self.winner = sorted_scores[0][0]

        pp(self.alternatives_scores)
        print(self.winner)
