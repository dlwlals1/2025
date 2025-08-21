MBTI_LIST = list(MBTI_BASE.keys())

MBTI_TIPS = {
    "INTJ": "🗺️ 전략 세우기 + OKR로 장기 목표를 쪼개 보세요.",
    "INTP": "🧩 탐구/실험 프로젝트(PBL)로 호기심을 구조화!",
    "ENTJ": "👑 리더십·실행력 살려 팀 목표와 역할 명확히.",
    "ENTP": "⚡ 해커톤/피치로 아이디어를 빠르게 검증!",
    "INFJ": "🤝 의미 중심 봉사/멘토링 활동이 동기 부여에 좋아요.",
    "INFP": "🎒 자신의 가치 스토리를 포트폴리오로 표현해요.",
    "ENFJ": "🌱 협업 기반 과제에서 조직/코칭 스킬을 키워요.",
    "ENFP": "🎉 자유로운 탐색과 네트워킹으로 기회를 만드세요.",
    "ISTJ": "📏 체계적 커리큘럼·체크리스트로 꾸준함을!",
    "ISFJ": "💞 돌봄/지원 역할에서 강점 발휘. 서비스러닝 추천.",
    "ESTJ": "🧱 표준화·프로세스 개선 과제에 강점!",
    "ESFJ": "🤗 커뮤니티 운영/행사 기획으로 협업력 업!",
    "ISTP": "🔧 만들면서 배우는 Tinkering, 메이킹 프로젝트",
    "ISFP": "🎨 크리에이티브 포트폴리오로 감수성을 보여줘요.",
    "ESTP": "🏃 실전 판매/홍보 등 액션 위주 과제에 몰입!",
    "ESFP": "🌟 공연/콘텐츠 제작으로 에너지를 표현!",
}

# =========================================
# 🧮 유틸 함수
# =========================================

def score_career(weights: Dict[str, float], attrs: Dict[str, float]) -> float:
    v = np.array([attrs[a] for a in ATTRS], dtype=float)
    w = np.array([weights[a] for a in ATTRS], dtype=float)
    raw = float((v * w).sum())
    # normalize to 0-100 (max 10 * sum(weights))
    max_score = 10 * w.sum() if w.sum() else 1
    return round((raw / max_score) * 100, 2)


def normalize_weights(w: Dict[str, float]) -> Dict[str, float]:
    s = sum(w.values())
    return {k: (v / s if s else 0) for k, v in w.items()}


# =========================================
# 🎉 헤더
# =========================================
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("<div class='glass floaty'>🧭</div>", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <h1 class='title-glow'>MBTI 기반 진로 추천 💼✨</h1>
    <div class='muted'>나의 성향에 어울리는 커리어를 탐험해요 — *교육용 진로 탐색 툴*</div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =========================================
# 🧰 사이드바: MBTI & 선호 조절
# =========================================
with st.sidebar:
    st.markdown("### 🎯 내 성향 설정")
    mbti = st.selectbox("MBTI를 선택하세요", MBTI_LIST, index=MBTI_LIST.index("ENFP"))

    st.markdown("#### 🔧 가중치 미세 조정")
    base_w = MBTI_BASE[mbti].copy()
    a = st.slider("분석적 사고 🧠 (analysis)", 0.0, 1.5, float(base_w["analysis"]), 0.05)
    c = st.slider("창의성 🎨 (creativity)", 0.0, 1.5, float(base_w["creativity"]), 0.05)
    s = st.slider("구조/체계 📏 (structure)", 0.0, 1.5, float(base_w["structure"]), 0.05)
    co = st.slider("협업 🤝 (collab)", 0.0, 1.5, float(base_w["collab"]), 0.05)
    e = st.slider("공감/대인 🫶 (empathy)", 0.0, 1.5, float(base_w["empathy"]), 0.05)

    weights = {"analysis": a, "creativity": c, "structure": s, "collab": co, "empathy": e}

    st.markdown("#### 💡 관심 분야")
    interests = st.multiselect(
        "선호 카테고리를 고르면 보너스가 적용돼요 ✨",
        sorted(list({c["category"] for c in CAREERS})),
        default=["IT/데이터", "디자인"],
    )

    bonus = st.slider("카테고리 보너스 (점수 %) 🎁", 0, 20, 8, 1)

    st.markdown("#### 📊 상위 추천 개수")
    topk = st.slider("몇 개 보여줄까요?", 3, 10, 6)

# =========================================
# 🧠 매칭 계산
# =========================================
CAREER_DF = pd.DataFrame([{**{"career": c["career"], "category": c["category"], "emoji": c["emoji"]}, **c["attrs"]} for c in CAREERS])

normalized_w = normalize_weights(weights)

scores = []
for row in CAREERS:
    base = score_career(normalized_w, row["attrs"])  # 0~100
    cat_bonus = bonus if row["category"] in interests else 0
    final = min(100.0, round(base + cat_bonus, 2))
    scores.append({
        "career": row["career"],
        "category": row["category"],
        "emoji": row["emoji"],
        "score": final,
        **row["attrs"],
    })

result_df = pd.DataFrame(scores).sort_values("score", ascending=False).reset_index(drop=True)

# =========================================
# 🏆 추천 카드 그리드
# =========================================
st.markdown("## 🏆 나와 잘 맞는 커리어 Top ✨")
cols = st.columns(topk)
for i in range(topk):
    if i >= len(result_df):
        break
    r = result_df.iloc[i]
    with cols[i]:
        st.markdown("""
        <div class='glass'>
          <div class='card-title'>%s %s</div>
          <div class='muted'>%s</div>
          <div style='height:8px'></div>
          <div class='scorebar'><span style='width:%s%%'></span></div>
          <div style='display:flex;justify-content:space-between;align-items:center;margin-top:8px;'>
            <div class='metric'>%s 점</div>
            <div>
              <span class='chip'>🧠 %s</span>
              <span class='chip'>🎨 %s</span>
              <span class='chip'>📏 %s</span>
              <span class='chip'>🤝 %s</span>
              <span class='chip'>🫶 %s</span>
            </div>
          </div>
        </div>
        """ % (
            r["emoji"], r["career"], r["category"],
            r["score"], int(r["score"]),
            int(r["analysis"]), int(r["creativity"]), int(r["structure"]), int(r["collab"]), int(r["empathy"]) 
        ), unsafe_allow_html=True)

# =========================================
# 📈 레이더 차트 (Top 1 상세 비교)
# =========================================
if len(result_df) > 0:
    top1 = result_df.iloc[0]
    user_vec = [normalized_w[a] for a in ATTRS]
    career_vec = [top1[a]/10 for a in ATTRS]  # 0~1 스케일 비교

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=user_vec + [user_vec[0]], theta=ATTRS + [ATTRS[0]], fill='toself', name='나의 선호', opacity=0.6))
    fig.add_trace(go.Scatterpolar(r=career_vec + [career_vec[0]], theta=ATTRS + [ATTRS[0]], fill='toself', name=f"{top1['career']} 특성", opacity=0.6))
    fig.update_layout(title=f"🔎 Top 1 상세 비교 — {top1['emoji']} {top1['career']}", polar=dict(radialaxis=dict(visible=True, range=[0,1])), legend=dict(orientation='h'))
    st.plotly_chart(fig, use_container_width=True)

# =========================================
# 🧾 전체 표 & 다운로드
# =========================================
st.markdown("## 📚 전체 추천 목록")
st.dataframe(result_df[["emoji","career","category","score"] + ATTRS], use_container_width=True, hide_index=True)

csv = result_df.to_csv(index=False).encode('utf-8-sig')
st.download_button("📥 결과 CSV 다운로드", data=csv, file_name="mbti_recommendations.csv", mime="text/csv")

# =========================================
# 💡 MBTI별 학습 팁
# =========================================
st.markdown("## 💡 MBTI별 학습/진로 팁")
st.info(MBTI_TIPS.get(mbti, "나만의 학습 전략을 만들어 보세요!"))

# =========================================
# 🧯 주의 & 윤리 문구
# =========================================
st.markdown("""
> ⚠️ **주의**: MBTI는 *진단 도구*가 아니라 **자기 성찰 가이드**에 더 가깝습니다. 이 결과만으로 진로를 단정하지 말고,
> 흥미, 가치관, 역량(경험), 직무 정보 탐색을 함께 고려하세요. 🙌
""")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =========================================
# 🔧 팁: 배포/사용법
# =========================================
st.markdown(
    """
    <div class='footer'>
      ▶ 로컬 실행: <code>pip install streamlit plotly pandas numpy</code> → <code>streamlit run app.py</code><br/>
      ▶ 배포: Streamlit Community Cloud 또는 Hugging Face Spaces에 업로드 후 공유 링크 배포 🌐
    </div>
    """, unsafe_allow_html=True
)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==============================
# 🌟 앱 설정
# ==============================
st.set_page_config(
    page_title="MBTI 기반 진로 추천 💫✨🌈🔥",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
# 💅 초-화려한(✨🪩) 스타일
# ==============================
CUSTOM_CSS = """
<style>
.stApp {
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 40%, #fad0c4 60%, #fbc2eb 100%);
  color: #1e293b;
}

h1, h2, h3, h4 { 
  text-shadow: 0 0 20px rgba(255,255,255,.7), 0 0 40px rgba(255,182,193,.6);
}

.block-card {
  background: rgba(255, 255, 255, .75);
  border: 2px solid rgba(255,255,255,.6);
  box-shadow: 0 15px 40px rgba(0,0,0,.25);
  backdrop-filter: blur(12px);
  border-radius: 24px;
  padding: 24px 20px;
}

.badge { 
  display:inline-block; padding:8px 14px; border-radius:999px; 
  background: linear-gradient(90deg,#ff7eb3,#ff758c,#ff6a88);
  color:#fff; font-weight:700; font-size:1rem;
  margin-right:8px;
}

.scorebar { height: 12px; border-radius: 999px; background: rgba(0,0,0,.08); overflow:hidden;}
.scorebar > span { display:block; height:100%; background: linear-gradient(90deg,#ff9a9e,#fad0c4,#fbc2eb); }

@keyframes shimmer { 0%{opacity:.7} 50%{opacity:1} 100%{opacity:.7} }
.shine { animation: shimmer 2.2s ease-in-out infinite; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================
# 📦 데이터 정의 (이모지 MAX🌈🔥✨)
# ==============================
CAREERS = [
    {"career": "소프트웨어 엔지니어 💻⚡🤖", "category": "IT/개발 🚀", "attrs": {"analysis": 9, "creativity": 6, "structure": 8, "collab": 6, "empathy": 4}},
    {"career": "데이터 분석가 📊🔍✨", "category": "IT/데이터 💾", "attrs": {"analysis": 9, "creativity": 5, "structure": 8, "collab": 6, "empathy": 4}},
    {"career": "데이터 사이언티스트 🧪📈🧠", "category": "AI/데이터 🤖", "attrs": {"analysis": 10, "creativity": 7, "structure": 7, "collab": 5, "empathy": 4}},
    {"career": "프로덕트 매니저 🧭📱✨", "category": "IT/기획 🎯", "attrs": {"analysis": 7, "creativity": 7, "structure": 6, "collab": 8, "empathy": 6}},
    {"career": "UX/UI 디자이너 🎨🖌️💡", "category": "디자인 🌈", "attrs": {"analysis": 5, "creativity": 9, "structure": 5, "collab": 7, "empathy": 7}},
    {"career": "그래픽 디자이너 🖍️🌟✨", "category": "디자인 🎨", "attrs": {"analysis": 4, "creativity": 9, "structure": 5, "collab": 6, "empathy": 6}},
    {"career": "마케팅 매니저 📣🔥💎", "category": "마케팅/광고 🌟", "attrs": {"analysis": 6, "creativity": 8, "structure": 5, "collab": 8, "empathy": 7}},
    {"career": "브랜드 매니저 🏷️💖✨", "category": "마케팅 💎", "attrs": {"analysis": 6, "creativity": 7, "structure": 6, "c
