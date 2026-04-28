# main.py

from people_pick.voting import (
    get_options,
    get_voters,
    get_rankings,
    get_scores,
    print_result,
)
from people_pick.methods import borda, bentham, nash, condorcet


def main():
    print("=" * 40)
    print("  PeoplePick — 사회적 선택 투표 시스템")
    print("=" * 40)

    # 입력
    title, options = get_options()
    voters = get_voters()
    rankings = get_rankings(voters, options)
    scores = get_scores(voters, options, rankings)

    # 모든 방식 계산
    results = {
        "Borda":      borda.calculate(options, rankings),
        "Bentham":    bentham.calculate(options, scores),
        "Nash":       nash.calculate(options, scores),
        "Condorcet":  condorcet.calculate(options, rankings),
    }

    # 방식 선택
    print("\n원하는 투표 방식을 선택하세요:")
    methods = list(results.keys())
    for i, method in enumerate(methods, 1):
        print(f"  {i}. {method}")
    print(f"  {len(methods) + 1}. 전체 비교")

    choice = input("\n번호를 입력하세요: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(methods):
        method = methods[int(choice) - 1]
        print_result(method, results[method])
    elif choice == str(len(methods) + 1):
        for method, result in results.items():
            print_result(method, result)
    else:
        print("올바른 번호를 입력하세요.")


if __name__ == "__main__":
    main()