# people-pick/methods/nash.py

def calculate(options: list[str], scores: dict) -> dict:
    """
    Nash 방식: 각 투표자의 점수를 곱해서 가장 높은 옵션이 승자.
    scores: {voter: {option: score}}
    """
    totals = {option: 1 for option in options}

    for voter_scores in scores.values():
        for option, score in voter_scores.items():
            totals[option] *= score

    winner = max(totals, key=totals.get)
    return {"winner": winner, "scores": totals}