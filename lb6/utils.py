def sort_scores_desc(scores: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def init_alternatives_scores(vote: tuple):
    alts = {}
    for value in vote:
        alts[value] = 0
    return alts
