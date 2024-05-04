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
    winner = sorted_scores[0][0]

    return scores, winner
