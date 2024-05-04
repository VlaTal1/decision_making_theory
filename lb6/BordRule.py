from lb6.utils import init_alternatives_scores, sort_scores_desc


class BordRule:
    def __init__(self, voting_profile: dict[tuple, int]):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.winner = None

        self.find_winner()

    def find_winner(self):
        alternatives_scores = init_alternatives_scores(list(self.voting_profile.keys())[0])
        alternatives = list(alternatives_scores.keys())
        for alternative in alternatives:
            for vote, amount in self.voting_profile.items():
                for i, value in enumerate(vote):
                    if value == alternative:
                        alternatives_scores[alternative] += amount * (len(vote) - i - 1)

        self.alternatives_scores = alternatives_scores
        sorted_scores = sort_scores_desc(alternatives_scores)
        self.winner = sorted_scores[0][0]

        print("========================== Bord Rule ==========================")
        print("Scores:")
        print(alternatives_scores)
        print("Winner:")
        print(self.winner)
