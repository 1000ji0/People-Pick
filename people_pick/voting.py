# people-pick/voting.py

def get_options() -> tuple[str, list[str]]:
    """투표 주제와 옵션 목록 입력"""
    title = input("투표 주제를 입력하세요: ")
    options_str = input("투표 옵션을 입력하세요 (쉼표로 구분): ")
    options = [opt.strip() for opt in options_str.split(",")]
    print(f"\n투표 주제: {title}")
    print(f"투표 옵션: {options}")
    return title, options


def get_voters() -> list[str]:
    """투표자 목록 입력"""
    voters_str = input("\n투표자 목록을 입력하세요 (쉼표로 구분): ")
    voters = [v.strip() for v in voters_str.split(",")]
    print(f"투표자 목록: {voters}")
    return voters


def get_rankings(voters: list[str], options: list[str]) -> dict:
    """투표자별 순위 입력"""
    rankings = {}
    for voter in voters:
        print(f"\n{voter}님, 옵션에 대한 순위를 입력하세요.")
        rankings[voter] = []
        used_ranks = set()
        for option in options:
            while True:
                rank = input(f"  {option}의 순위 (1~{len(options)}): ")
                if rank.isdigit() and 1 <= int(rank) <= len(options):
                    if int(rank) not in used_ranks:
                        used_ranks.add(int(rank))
                        rankings[voter].append((int(rank), option))
                        break
                    else:
                        print("  이미 사용된 순위입니다.")
                else:
                    print("  올바른 숫자를 입력하세요.")
    return rankings


def get_scores(voters: list[str], options: list[str], rankings: dict) -> dict:
    """투표자별 선호도 점수 입력"""
    sorted_rankings = {
        voter: [opt for _, opt in sorted(rankings[voter])]
        for voter in rankings
    }

    print("\n--- 정렬된 순위 ---")
    for voter, order in sorted_rankings.items():
        print(f"  {voter}: {order}")

    scores = {}
    for voter in voters:
        print(f"\n{voter}님, 각 옵션에 점수를 입력하세요. (1~10)")
        scores[voter] = {}
        for option in options:
            while True:
                try:
                    val = float(input(f"  {option}의 점수: "))
                    if 1 <= val <= 10:
                        scores[voter][option] = val
                        break
                    else:
                        print("  1~10 사이 숫자를 입력하세요.")
                except ValueError:
                    print("  올바른 숫자를 입력하세요.")
    return scores


def print_result(method: str, result: dict):
    """결과 출력"""
    print(f"\n{'='*40}")
    print(f"[{method}] 승자: {result['winner']}")
    if "scores" in result:
        print("점수:")
        for opt, score in result["scores"].items():
            print(f"  {opt}: {score}")
    if "wins" in result:
        print("1대1 승리 횟수:")
        for opt, win in result["wins"].items():
            print(f"  {opt}: {win}승")
    if "pairwise" in result:
        print("1대1 대결 결과:")
        for pair, winner in result["pairwise"].items():
            print(f"  {pair} → {winner}")
    print('='*40)