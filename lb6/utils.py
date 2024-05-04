from itertools import combinations


def sort_scores_desc(scores: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def init_alternatives_scores(vote: tuple):
    alts = {}
    for value in vote:
        alts[value] = 0
    return alts


def execute_round(voting_profile: dict[tuple, int]):
    scores = init_alternatives_scores(list(voting_profile.keys())[0])
    for vote, amount in voting_profile.items():
        alt = vote[0]
        scores[alt] += amount

    sorted_scores = sort_scores_desc(scores)

    return scores, sorted_scores


def filter_votes(voting_profile: dict[tuple, int], alternatives: list[str]) -> dict[tuple, int]:
    filtered_voting_profile = {}

    for vote, amount in voting_profile.items():
        new_vote = []
        for value in vote:
            if value in alternatives:
                new_vote.append(value)

        if tuple(new_vote) in filtered_voting_profile.keys():
            filtered_voting_profile[tuple(new_vote)] += amount
        else:
            filtered_voting_profile[tuple(new_vote)] = amount

    return filtered_voting_profile


def create_combinations(arr):
    result = list(combinations(arr, 2))
    return result
