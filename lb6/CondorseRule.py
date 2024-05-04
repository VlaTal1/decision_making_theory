from pprint import pprint as pp

from lb6.utils import init_alternatives_scores, create_combinations, filter_votes, execute_round, sort_scores_desc


class CondorseRule:
    def __init__(self, voting_profile):
        self.voting_profile = voting_profile
        self.alternatives_scores = {}
        self.comparison_tables = {}
        self.comparison_results = {}
        self.winner = None

        self.find_winner()

    def find_winner(self):
        print("========================== Condorse Rule ==========================")
        alternatives_scores = init_alternatives_scores(list(self.voting_profile.keys())[0])
        comparisons = create_combinations(list(alternatives_scores.keys()))
        for combination in comparisons:
            filtered_votes = filter_votes(self.voting_profile, list(combination))
            scores, sorted_scores = execute_round(filtered_votes)
            print(combination, sorted_scores)
            if combination == ('GPT-4 Turbo', 'GPT-3.5 Turbo'):
                pass
            alternatives_scores[sorted_scores[0][0]] += 1
            if sorted_scores[0][1] == sorted_scores[1][1]:
                alternatives_scores[sorted_scores[1][0]] += 1

        sorted_scores = sort_scores_desc(alternatives_scores)
        self.alternatives_scores = sorted_scores
        self.winner = sorted_scores[0][0]
        print("Scores:")
        pp(self.alternatives_scores)
        print("Winner:")
        print(self.winner)
