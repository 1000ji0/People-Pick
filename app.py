import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_sortables import sort_items

from people_pick.methods import borda, bentham, nash, condorcet

# ── 페이지 설정 ─────────────────────────────────────────────
st.set_page_config(
    page_title="PeoplePick",
    page_icon="🗳️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Outfit', 'Noto Sans KR', sans-serif;
}

/* 전체 배경 */
.stApp { background: #faf9f7 !important; color: #1a1a1a !important; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { display: none; }

/* 스텝 인디케이터 */
.step-bar {
    display: flex; justify-content: center;
    align-items: center; margin: 1.5rem 0 2.5rem;
}
.step-item {
    display: flex; flex-direction: column;
    align-items: center; gap: 6px;
    flex: 1; position: relative;
}
.step-item:not(:last-child)::after {
    content: ''; position: absolute;
    top: 18px; left: 60%; width: 80%; height: 2px;
    background: #e8e4df; z-index: 0;
}
.step-item.done:not(:last-child)::after { background: #FF6B35; }
.step-circle {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem;
    background: #f0ede8; color: #bbb;
    border: 2px solid #e8e4df;
    position: relative; z-index: 1; transition: all 0.3s;
}
.step-item.active .step-circle {
    background: #FF6B35; color: white; border-color: #FF6B35;
    box-shadow: 0 0 16px rgba(255,107,53,0.3);
}
.step-item.done .step-circle {
    background: #FF6B35; color: white; border-color: #FF6B35;
}
.step-label { font-size: 0.7rem; color: #bbb; white-space: nowrap; }
.step-item.active .step-label { color: #FF6B35; font-weight: 600; }
.step-item.done .step-label { color: #FF6B35; }

/* 히어로 */
.hero { text-align: center; padding: 3rem 0 1rem; }
.hero-logo {
    font-size: 4rem; font-weight: 800;
    background: linear-gradient(135deg, #FF6B35, #FF4500);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -2px; line-height: 1; margin-bottom: 0.5rem;
}
.hero-sub {
    color: #aaa; font-size: 0.9rem; font-weight: 300;
    letter-spacing: 3px; text-transform: uppercase;
}

/* 섹션 레이블 */
.section-label {
    font-size: 0.7rem; font-weight: 700; color: #FF6B35;
    letter-spacing: 2px; text-transform: uppercase;
    margin-bottom: 1.2rem;
}

/* 방식 그리드 (홈) */
.method-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 0.8rem; margin: 1.5rem 0;
}
.method-card {
    background: white; border: 1px solid #ece9e4;
    border-radius: 14px; padding: 1.2rem;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.method-card:hover {
    border-color: #FF6B35;
    box-shadow: 0 4px 16px rgba(255,107,53,0.1);
}
.method-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.method-name { font-size: 0.9rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.3rem; }
.method-desc { font-size: 0.75rem; color: #888; line-height: 1.6; }

/* 버튼 */
div[data-testid="stButton"] > button {
    background: #FF6B35 !important; color: white !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; font-family: 'Outfit', sans-serif !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    background: #e55a25 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(255,107,53,0.25) !important;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: white !important; border: 1px solid #e0dbd4 !important;
    color: #888 !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    border-color: #FF6B35 !important; color: #FF6B35 !important;
    transform: none !important; box-shadow: none !important;
}

/* 입력 필드 */
div[data-testid="stTextInput"] input {
    background: white !important; border: 1.5px solid #e8e4df !important;
    color: #1a1a1a !important; border-radius: 10px !important;
    font-size: 0.95rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.1) !important;
}
div[data-testid="stTextInput"] label { color: #666 !important; }

/* 셀렉트박스 */
div[data-testid="stSelectbox"] > div { border-color: #e8e4df !important; }

/* 슬라이더 */
div[data-testid="stSlider"] > div > div > div { background: #FF6B35 !important; }

/* 구분선 */
hr { border-color: #ece9e4 !important; margin: 1.5rem 0 !important; }

/* 결과 페이지 전용 */
.result-winner-banner {
    background: linear-gradient(135deg, #FF6B35, #FF4500);
    border-radius: 20px; padding: 2rem 1.5rem;
    text-align: center; margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(255,107,53,0.2);
}
.result-winner-banner .label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(255,255,255,0.75);
    margin-bottom: 0.5rem;
}
.result-winner-banner .name {
    font-size: 2.5rem; font-weight: 800;
    color: white; letter-spacing: -1px;
}

.compare-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 0.6rem; margin-bottom: 2rem;
}
.compare-card {
    background: white; border: 1.5px solid #ece9e4;
    border-radius: 12px; padding: 1rem 0.8rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.compare-card .method-tag {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: #FF6B35;
    margin-bottom: 0.5rem;
}
.compare-card .winner-name {
    font-size: 1rem; font-weight: 700; color: #1a1a1a;
}

.result-block {
    background: white; border: 1.5px solid #ece9e4;
    border-radius: 16px; padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.result-block-header {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 1.2rem;
    padding-bottom: 1rem; border-bottom: 1px solid #f0ede8;
}
.result-block-method {
    font-size: 1rem; font-weight: 700; color: #1a1a1a;
}
.result-block-method span {
    font-size: 0.65rem; font-weight: 600; color: #FF6B35;
    letter-spacing: 1.5px; text-transform: uppercase;
    display: block; margin-bottom: 2px;
}
.result-block-winner {
    background: #fff5f0; border: 1.5px solid #ffd4c2;
    color: #FF6B35; padding: 0.4rem 1rem;
    border-radius: 20px; font-size: 0.9rem; font-weight: 700;
}

/* 모바일 */
@media (max-width: 640px) {
    .method-grid { grid-template-columns: 1fr; }
    .compare-grid { grid-template-columns: repeat(2, 1fr); }
    .hero-logo { font-size: 2.8rem; }
    .step-label { display: none; }
}
</style>
""", unsafe_allow_html=True)


# ── 세션 초기화 ──────────────────────────────────────────────
def init_session():
    defaults = {
        "stage": "home", "title": "",
        "candidates": [], "voters": [],
        "votes": {}, "completed": {}, "current_voter": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── 스텝 인디케이터 ──────────────────────────────────────────
STEPS = ["설정", "투표", "순위", "점수", "결과"]
STAGE_TO_STEP = {
    "setup": 0, "vote_select": 1,
    "vote_input": 2, "score_input": 3, "result": 4,
}

def render_steps(stage):
    current = STAGE_TO_STEP.get(stage, -1)
    if current < 0:
        return
    items = ""
    for i, label in enumerate(STEPS):
        if i < current:
            cls, icon = "step-item done", "✓"
        elif i == current:
            cls, icon = "step-item active", str(i + 1)
        else:
            cls, icon = "step-item", str(i + 1)
        items += f"""<div class="{cls}">
            <div class="step-circle">{icon}</div>
            <div class="step-label">{label}</div>
        </div>"""
    st.markdown(f'<div class="step-bar">{items}</div>', unsafe_allow_html=True)


# ── 계산 ─────────────────────────────────────────────────────
def run_all(candidates, votes):
    rankings = {
        voter: [(rank, opt) for opt, rank in vd["rank"].items()]
        for voter, vd in votes.items()
    }
    scores_dict = {voter: vd["score"] for voter, vd in votes.items()}
    b  = borda.calculate(candidates, rankings)
    bt = bentham.calculate(candidates, scores_dict)
    n  = nash.calculate(candidates, scores_dict)
    c  = condorcet.calculate(candidates, rankings)
    return {
        "보르다":   {"result": b,  "score_key": "scores", "ascending": True,  "desc": "순위 합 (낮을수록 유리)"},
        "벤담":     {"result": bt, "score_key": "scores", "ascending": False, "desc": "점수 합 (높을수록 유리)"},
        "내쉬":     {"result": n,  "score_key": "scores", "ascending": False, "desc": "점수 곱 (높을수록 유리)"},
        "콩도르세": {"result": c,  "score_key": "wins",   "ascending": False, "desc": "1대1 승리 횟수"},
    }


# ── 차트 ─────────────────────────────────────────────────────
def bar_chart(scores: dict, ascending: bool, winner: str):
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=not ascending)
    labels = [i[0] for i in sorted_items]
    values = [i[1] for i in sorted_items]
    colors = ["#FF6B35" if lbl == winner else "#f0ede8" for lbl in labels]
    text_colors = ["white" if lbl == winner else "#aaa" for lbl in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors, marker_line_width=0,
        text=[f"{v:.2f}" for v in values],
        textposition="outside",
        textfont=dict(size=12),
    ))
    fig.update_traces(textfont_color=text_colors)
    fig.update_layout(
        showlegend=False, height=260,
        margin=dict(t=20, b=10, l=10, r=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(
            gridcolor="#f5f2ee",
            tickfont=dict(color="#555", size=13, family="Outfit, Noto Sans KR"),
            linecolor="#ece9e4",
        ),
        yaxis=dict(
            gridcolor="#f5f2ee",
            tickfont=dict(color="#bbb", size=11),
            linecolor="#ece9e4",
        ),
    )
    return fig


# ── ① 홈 ────────────────────────────────────────────────────
if st.session_state.stage == "home":
    st.markdown("""
    <div class="hero">
        <div class="hero-logo">PeoplePick</div>
        <div class="hero-sub">Social Choice Voting System</div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("투표 시작하기 →", use_container_width=True):
            st.session_state.stage = "setup"
            st.rerun()

    st.markdown("""
    <div class="method-grid">
        <div class="method-card">
            <div class="method-icon">🏆</div>
            <div class="method-name">보르다</div>
            <div class="method-desc">순위 합이 가장 낮은 후보가 승자. 모든 순위를 반영하는 서수적 방식.</div>
        </div>
        <div class="method-card">
            <div class="method-icon">💯</div>
            <div class="method-name">벤담</div>
            <div class="method-desc">선호도 점수 총합이 가장 높은 후보가 승자. 선호의 강도를 반영.</div>
        </div>
        <div class="method-card">
            <div class="method-icon">⚖️</div>
            <div class="method-name">내쉬</div>
            <div class="method-desc">점수 곱이 가장 큰 후보가 승자. 사회 효용의 기하평균 최대화.</div>
        </div>
        <div class="method-card">
            <div class="method-icon">🥊</div>
            <div class="method-name">콩도르세</div>
            <div class="method-desc">1대1 전체 순위 기반 pairwise 비교. 가장 많이 이긴 후보 승자.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("주의사항"):
        st.markdown("""
- 교육·학습 목적으로 제작되었습니다.
- 정확한 비교를 위해 후보 3명 이상, 투표자 3명 이상을 권장합니다.
- 콩도르세 패러독스 발생 시 승리 횟수 기준으로 처리됩니다.
""")


# ── ② 설정 ──────────────────────────────────────────────────
elif st.session_state.stage == "setup":
    render_steps("setup")
    st.markdown('<div class="section-label">투표 설정</div>', unsafe_allow_html=True)

    st.session_state.title = st.text_input(
        "투표 주제", value=st.session_state.title,
        placeholder="예: 팀 점심 메뉴 선택",
    )
    candidate_input = st.text_input(
        "후보 목록 (쉼표로 구분, 3명 이상 권장)",
        value=",".join(st.session_state.candidates),
        placeholder="예: 피자, 햄버거, 파스타",
    )
    voter_input = st.text_input(
        "투표자 목록 (쉼표로 구분, 3명 이상 권장)",
        value=",".join(st.session_state.voters),
        placeholder="예: 홍길동, 김영희, 이철수",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 홈으로", use_container_width=True, type="secondary"):
            st.session_state.stage = "home"
            st.rerun()
    with col2:
        if st.button("투표 시작 →", use_container_width=True):
            candidates = [x.strip() for x in candidate_input.split(",") if x.strip()]
            voters     = [x.strip() for x in voter_input.split(",") if x.strip()]
            errors = []
            if not st.session_state.title.strip(): errors.append("투표 주제를 입력하세요.")
            if len(candidates) < 2: errors.append("후보는 최소 2명 이상이어야 합니다.")
            if len(set(candidates)) != len(candidates): errors.append("후보 이름이 중복됩니다.")
            if len(voters) < 1: errors.append("투표자는 최소 1명 이상이어야 합니다.")
            if len(set(voters)) != len(voters): errors.append("투표자 이름이 중복됩니다.")
            if errors:
                for e in errors: st.error(e)
            else:
                st.session_state.candidates = candidates
                st.session_state.voters = voters
                st.session_state.votes = {
                    v: {"rank": {c: i+1 for i, c in enumerate(candidates)},
                        "score": {c: 5 for c in candidates}}
                    for v in voters
                }
                st.session_state.completed = {v: False for v in voters}
                st.session_state.stage = "vote_select"
                st.rerun()


# ── ③ 투표자 선택 ────────────────────────────────────────────
elif st.session_state.stage == "vote_select":
    render_steps("vote_select")
    done  = sum(1 for v in st.session_state.completed.values() if v)
    total = len(st.session_state.voters)

    st.markdown(f'<div class="section-label">{st.session_state.title}</div>',
                unsafe_allow_html=True)
    st.progress(done / total if total else 0)
    st.caption(f"{done} / {total}명 완료")
    st.markdown("")

    completed_voters = [v for v in st.session_state.voters if st.session_state.completed.get(v)]
    remaining        = [v for v in st.session_state.voters if not st.session_state.completed.get(v)]

    for v in completed_voters:
        st.markdown(f"✅ &nbsp;{v}", unsafe_allow_html=True)

    if not remaining:
        st.success("모든 투표자의 입력이 완료되었습니다!")
        if st.button("결과 보기 →", use_container_width=True):
            st.session_state.stage = "result"
            st.rerun()
    else:
        st.markdown("")
        voter = st.selectbox("투표할 사람 선택", remaining)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 설정으로", use_container_width=True, type="secondary"):
                st.session_state.stage = "setup"
                st.rerun()
        with col2:
            if st.button(f"{voter}님 투표 시작 →", use_container_width=True):
                st.session_state.current_voter = voter
                st.session_state.stage = "vote_input"
                st.rerun()


# ── ④ 순위 입력 ──────────────────────────────────────────────
elif st.session_state.stage == "vote_input":
    voter = st.session_state.current_voter
    if not voter:
        st.session_state.stage = "vote_select"
        st.rerun()

    render_steps("vote_input")
    st.markdown(f'<div class="section-label">{voter}님의 순위 입력</div>',
                unsafe_allow_html=True)
    st.caption("드래그해서 선호 순서를 정해주세요. 위가 1순위입니다.")

    current_order = sorted(
        st.session_state.candidates,
        key=lambda c: st.session_state.votes[voter]["rank"].get(c, 99)
    )
    sorted_candidates = sort_items(current_order, direction="vertical")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 투표자 선택으로", use_container_width=True, type="secondary"):
            st.session_state.stage = "vote_select"
            st.rerun()
    with col2:
        if st.button("다음: 점수 입력 →", use_container_width=True):
            st.session_state.votes[voter]["rank"] = {
                c: i+1 for i, c in enumerate(sorted_candidates)
            }
            st.session_state.stage = "score_input"
            st.rerun()


# ── ⑤ 점수 입력 ──────────────────────────────────────────────
elif st.session_state.stage == "score_input":
    voter = st.session_state.current_voter
    if not voter:
        st.session_state.stage = "vote_select"
        st.rerun()

    render_steps("score_input")
    st.markdown(f'<div class="section-label">{voter}님의 선호 점수 입력</div>',
                unsafe_allow_html=True)
    st.caption("각 후보에 0~10점으로 선호도를 표현해주세요. (벤담·내쉬 방식에 사용됩니다)")

    ranks = st.session_state.votes[voter]["rank"]
    sorted_candidates = sorted(st.session_state.candidates, key=lambda c: ranks.get(c, 99))
    scores_data = st.session_state.votes[voter]["score"]
    current_scores = {}

    for c in sorted_candidates:
        col_l, col_r = st.columns([3, 1])
        with col_l:
            st.markdown(f"**{c}** &nbsp;<span style='color:#bbb;font-size:0.8rem'>{ranks.get(c,'?')}순위</span>",
                        unsafe_allow_html=True)
            current_scores[c] = st.slider(
                f"s_{c}", min_value=0, max_value=10,
                value=int(scores_data.get(c, 5)),
                key=f"score_{c}_{voter}",
                label_visibility="collapsed",
            )
        with col_r:
            st.markdown(f"<div style='font-size:2rem;font-weight:800;color:#FF6B35;"
                        f"text-align:center;padding-top:0.5rem'>"
                        f"{int(scores_data.get(c,5))}</div>",
                        unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 순위 다시 입력", use_container_width=True, type="secondary"):
            st.session_state.votes[voter]["score"] = current_scores
            st.session_state.stage = "vote_input"
            st.rerun()
    with col2:
        if st.button("투표 제출 ✓", use_container_width=True):
            st.session_state.votes[voter]["score"] = current_scores
            st.session_state.completed[voter] = True
            st.session_state.current_voter = None
            st.session_state.stage = "vote_select"
            st.rerun()


# ── ⑥ 결과 ──────────────────────────────────────────────────
elif st.session_state.stage == "result":
    render_steps("result")

    all_results = run_all(st.session_state.candidates, st.session_state.votes)
    winners = [res["result"]["winner"] for res in all_results.values()]

    # 타이틀
    st.markdown(f"""
    <div style="margin-bottom:1.5rem">
        <div style="font-size:0.7rem;font-weight:700;color:#FF6B35;
        letter-spacing:2px;text-transform:uppercase;margin-bottom:0.3rem">
            투표 결과
        </div>
        <div style="font-size:1.6rem;font-weight:800;color:#1a1a1a;letter-spacing:-0.5px">
            {st.session_state.title}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 만장일치 vs 방식별 상이
    if len(set(winners)) == 1:
        st.markdown(f"""
        <div class="result-winner-banner">
            <div class="label">🎉 전 방식 만장일치 승자</div>
            <div class="name">{winners[0]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="compare-grid">', unsafe_allow_html=True)
        for method, res in all_results.items():
            st.markdown(f"""
            <div class="compare-card">
                <div class="method-tag">{method}</div>
                <div class="winner-name">{res['result']['winner']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.warning("투표 방식에 따라 승자가 다릅니다. 각 방식의 결과를 비교해보세요.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 방식별 상세 블록
    for method, res in all_results.items():
        scores = res["result"][res["score_key"]]
        winner = res["result"]["winner"]

        st.markdown(f"""
        <div class="result-block">
            <div class="result-block-header">
                <div class="result-block-method">
                    <span>{method}</span>
                    {res['desc']}
                </div>
                <div class="result-block-winner">🏆 {winner}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 차트
        fig = bar_chart(scores, res["ascending"], winner)
        st.plotly_chart(fig, use_container_width=True)

        # 점수 테이블
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=not res["ascending"])
        df = pd.DataFrame(
            [{"순위": i+1, "후보": c, res["desc"]: round(s, 3)}
             for i, (c, s) in enumerate(sorted_scores)]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 콩도르세 1대1
        if method == "콩도르세" and "pairwise" in res["result"]:
            with st.expander("1대1 대결 전체 결과 보기"):
                pair_df = pd.DataFrame(
                    [{"대결": k, "승자": v}
                     for k, v in res["result"]["pairwise"].items()]
                )
                st.dataframe(pair_df, use_container_width=True, hide_index=True)

        st.markdown("")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 투표 다시 입력", use_container_width=True, type="secondary"):
            st.session_state.completed = {v: False for v in st.session_state.voters}
            st.session_state.stage = "vote_select"
            st.rerun()
    with col2:
        if st.button("🔄 처음부터 다시", use_container_width=True, type="secondary"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state.stage = "home"
            st.rerun()