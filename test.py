import streamlit as st

# ----------------------------
# 앱 기본 설정
# ----------------------------
st.set_page_config(
    page_title="🎨 나에게 맞는 디자인 전공 찾기",
    page_icon="✨",
    layout="centered"
)

# ----------------------------
# 헤더
# ----------------------------
st.markdown("<h1 style='text-align: center;'>🎨 나에게 맞는 <span style='color:#FF4B4B'>디자인 전공</span> 찾기 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>당신의 성향과 관심사를 기반으로 <b>완벽한 전공</b>을 추천합니다! 🚀</p>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# Step 1. 작업 매체
# ----------------------------
st.subheader("🌐 Step 1. 선호하는 작업 매체")
medium = st.radio(
    "👉 어떤 작업 매체를 더 선호하나요?",
    ["💻 디지털 기반 (컴퓨터, 소프트웨어)", "✏️ 아날로그 기반 (드로잉, 수작업)"]
)

# ----------------------------
# Step 2. 작업 방식
# ----------------------------
st.subheader("💡 Step 2. 선호하는 작업 방식")
style = st.radio(
    "👉 작업할 때 어떤 방식을 더 즐기나요?",
    ["🎨 아이디어와 창의적인 발상 중심", "⚙️ 기술적·체계적인 실행 중심"]
)

# ----------------------------
# Step 3. 협업 스타일
# ----------------------------
st.subheader("🤝 Step 3. 협업 스타일")
teamwork = st.radio(
    "👉 작업할 때 선호하는 방식은?",
    ["👥 팀과 함께 협업하기", "🧑‍🎨 혼자 몰입하기"]
)

# ----------------------------
# 결과 출력
# ----------------------------
if st.button("✨ 결과 확인하기 ✨"):
    st.balloons()
    st.success("결과가 나왔습니다! 🎉")

    # 조건 분기
    if medium.startswith("💻"):
        if style.startswith("🎨"):
            major = "🎨 시각디자인 / 광고디자인"
        else:
            if teamwork.startswith("👥"):
                major = "🖥️ UX/UI 디자인"
            else:
                major = "🎞️ 모션그래픽 / 인터랙션 디자인"
    else:  # 아날로그 기반
        if style.startswith("🎨"):
            if teamwork.startswith("👥"):
                major = "👗 패션디자인 / 🏛️ 공간디자인"
            else:
                major = "🖌️ 순수미술 기반 일러스트레이션 디자인"
        else:
            major = "📦 제품디자인 / 공예디자인"

    # 결과 출력
    st.markdown(f"<h2 style='text-align:center;'>✅ 당신에게 어울리는 전공은 <span style='color:#FFB800'>{major}</span> 입니다!</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # 로드맵
    st.subheader("📌 추천 로드맵")
    if "UX/UI" in major:
        st.markdown("1️⃣ **Figma / Sketch 툴 학습** → 2️⃣ **UX 리서치 경험** → 3️⃣ **프로토타입 포트폴리오 제작**")
    elif "시각디자인" in major:
        st.markdown("1️⃣ **그래픽 툴 학습 (Photoshop/Illustrator)** → 2️⃣ **브랜딩 사례 분석** → 3️⃣ **패키지/편집 디자인 실습**")
    elif "패션디자인" in major:
        st.markdown("1️⃣ **패션 드로잉 학습** → 2️⃣ **의상 제작 실습** → 3️⃣ **패션 포트폴리오 완성**")
    else:
        st.markdown("1️⃣ **기초 드로잉/제작 기술** → 2️⃣ **실험적 프로젝트 수행** → 3️⃣ **포트폴리오 정리**")

# ----------------------------
# 푸터
# ----------------------------
st.markdown("---")
st.markdown("<p style='text-align:center; font-size:14px;'>© 2025 디자인 진로 추천 웹앱 | Made with ❤️ in Streamlit</p>", unsafe_allow_html=True)

