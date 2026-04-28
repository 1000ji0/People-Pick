# people-pick/methods/borda.py

def calculate(options: list[str], rankings: dict) -> dict:
    """
    Borda 방식: 각 투표자의 순위 합이 가장 낮은 옵션이 승자.
    rankings: {voter: [(rank, option), ...]}
    """
    scores = {option: 0 for option in options}

    for ranking in rankings.values():
        for rank, option in ranking:
            scores[option] += rank

    winner = min(scores, key=scores.get)
    return {"winner": winner, "scores": scores}