# people_pick/methods/condorcet.py

def calculate(options: list[str], rankings: dict) -> dict:
    """
    Condorcet 방식: 전체 순위 기반 pairwise 비교.
    rankings: {voter: [(rank, option), ...]}
    """
    wins = {option: 0 for option in options}
    pairwise = {}

    pairs = [
        (options[i], options[j])
        for i in range(len(options))
        for j in range(i + 1, len(options))
    ]

    for a, b in pairs:
        a_wins, b_wins = 0, 0
        for ranking in rankings.values():
            order = {opt: rank for rank, opt in ranking}
            ra = order.get(a, float("inf"))
            rb = order.get(b, float("inf"))
            if ra < rb:
                a_wins += 1
            elif rb < ra:
                b_wins += 1

        if a_wins > b_wins:
            wins[a] += 1
            pairwise[f"{a} vs {b}"] = a
        elif b_wins > a_wins:
            wins[b] += 1
            pairwise[f"{a} vs {b}"] = b
        else:
            pairwise[f"{a} vs {b}"] = "무승부"

    winner = max(wins, key=wins.get)
    return {"winner": winner, "wins": wins, "pairwise": pairwise}