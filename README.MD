# 🗳️ PeoplePick
### 사회적 선택 이론 기반 투표 시스템

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://peoplepick.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

#### **url 바로가기**
> **https://people-pick-qlabdahgaaksgchfppas6f.streamlit.app/**
---

## 📌 프로젝트 소개

PeoplePick은 사회적 선택 이론(Social Choice Theory)에 기반한 투표 시스템입니다.

단순 다수결로는 모든 사람의 의견을 제대로 반영하지 못할 수 있습니다. PeoplePick은 **4가지 투표 방식**의 결과를 동시에 비교하여, 투표 방식에 따라 승자가 어떻게 달라지는지 직접 경험할 수 있도록 합니다.

점심 메뉴 정하기, 팀장 선출, 장소 결정 등 일상의 크고 작은 의사결정 상황에서 활용할 수 있습니다.

---

## 🔬 4가지 투표 방식

| 방식 | 설명 | 특징 |
|------|------|------|
| 🏆 **보르다** | 순위 합이 가장 낮은 후보가 승자 | 서수적(ordinal) 방식, 모든 순위 반영 |
| 💯 **벤담** | 선호도 점수 총합이 가장 높은 후보가 승자 | 기수적(cardinal) 방식, 선호 강도 반영 |
| ⚖️ **내쉬** | 선호도 점수 곱이 가장 큰 후보가 승자 | 사회 전체 효용의 기하평균 최대화 |
| 🥊 **콩도르세** | 1대1 전체 순위 기반 pairwise 비교 | 정통 콩도르세 방식 |

---

## 🖥️ 주요 기능

- **비밀 투표** — 투표자별 순서대로 입력, 타인의 투표 결과를 볼 수 없음
- **드래그 앤 드롭 순위 입력** — 직관적인 순서 설정
- **4가지 방식 동시 비교** — 방식에 따른 승자 차이를 한눈에 확인
- **시각화** — 방식별 막대 차트 + 점수 테이블
- **콩도르세 1대1 대결 상세** — pairwise 결과 전체 확인 가능
- **모바일 대응** — 반응형 레이아웃

---

## 🚀 실행 방법

### uv 사용 (권장)

```bash
git clone https://github.com/1000ji0/People-Pick.git
cd People-Pick
uv sync
uv run streamlit run app.py
```

### pip 사용

```bash
pip install -e .
streamlit run app.py
```

---

## 📁 프로젝트 구조

```
People-Pick/
├── app.py                      # Streamlit 메인 앱
├── people_pick/
│   ├── __init__.py
│   ├── voting.py               # 공통 입출력 처리
│   └── methods/
│       ├── __init__.py
│       ├── borda.py            # 보르다 방식
│       ├── bentham.py          # 벤담 방식
│       ├── nash.py             # 내쉬 방식
│       └── condorcet.py        # 콩도르세 방식 (전체 순위 기반 pairwise)
├── docs/                       # 기획 문서
├── pyproject.toml
└── README.md
```

---

## 🛠️ 기술 스택

- **Language:** Python 3.11+
- **Framework:** Streamlit
- **시각화:** Plotly
- **UI:** streamlit-sortables (드래그 앤 드롭)
- **패키지 관리:** uv

---

## ⚠️ 주의사항

- 이 서비스는 교육·학습 목적으로 제작되었습니다.
- 정확한 비교를 위해 후보 3명 이상, 투표자 3명 이상을 권장합니다.
- 콩도르세 패러독스(순환) 발생 시 승리 횟수 기준으로 처리됩니다.

---

## 📄 라이선스

MIT License © 2026 [Ji-Yeong Cheon](https://github.com/1000ji0)

이 프로젝트는 MIT 라이선스 하에 공개됩니다.
사용·수정·배포 시 출처를 표시해주세요.
