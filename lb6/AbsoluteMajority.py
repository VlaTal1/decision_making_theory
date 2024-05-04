from pprint import pprint as pp

from utils import init_alternatives_scores, execute_round, filter_votes


class AbsoluteMajority:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.first_round_scores = init_alternatives_scores(list(voting_profile.keys())[0])
        self.first_round_winners = []
        self.second_round_scores = init_alternatives_scores(list(voting_profile.keys())[0])
        self.second_round_profile = {}
        self.second_round_winner = None

        self.find_winner()

    def find_winner(self):
        self.first_round()
        self.second_round()

    def first_round(self):
        scores, sorted_scores = execute_round(self.voting_profile)
        self.first_round_scores = scores
        self.first_round_winners = [sorted_scores[0][0], sorted_scores[1][0]]

        print("========================== Absolute Majority ==========================")
        print("First round:")
        print("Scores:")
        pp(self.first_round_scores)
        print("Winners:")
        print(self.first_round_winners)

    def second_round(self):
        filtered_voting_profile = filter_votes(self.voting_profile, self.first_round_winners)

        scores, sorted_scores = execute_round(filtered_voting_profile)

        self.second_round_scores = scores
        self.second_round_profile = filtered_voting_profile
        self.second_round_winner = sorted_scores[0][0]

        print("Second round:")
        print("Scores:")
        pp(self.second_round_scores)
        print("Second round profile:")
        pp(self.second_round_profile)
        print("Winner:")
        pp(self.second_round_winner)
