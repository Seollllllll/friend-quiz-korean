import streamlit as st
import pandas as pd
import random

# 페이지 기본 설정
st.set_page_config(page_title="우리 반 친퀴즈!", page_icon="🧩", layout="centered")

st.title("🧩 우리 반 친퀴즈!")
st.caption("질문과 답변을 보고 주인공이 누구인지 맞춰보세요!")

# 세션 상태 초기화 (퀴즈 데이터 및 진행 상태 저장)
if "quiz_data" not in st.session_state:
    # 기본 데이터 세트
    st.session_state.quiz_data = [
        {"질문": "내가 가장 좋아하는 주말 일과는?", "답변": "침대에서 12시간 동안 누워있기", "이름": "김철수"},
        {"질문": "무인도에 가져갈 한 가지는?", "답변": "무제한 와이파이 공유기", "이름": "이영희"},
        {"질문": "내 인생 최고의 음식은?", "답변": "학교 매점 떡볶이", "이름": "박민수"}
    ]

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# 사이드바: 파일 업로드 및 데이터 관리
with st.sidebar:
    st.header("⚙️ 퀴즈 데이터 설정")
    uploaded_file = st.file_uploader("CSV 파일 업로드 (열 이름: 질문, 답변, 이름)", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.quiz_data = df.to_dict("records")
            st.success(f"총 {len(df)}개의 퀴즈를 불러왔습니다!")
        except Exception as e:
            st.error("파일 형식에 문제가 있습니다. CSV 열 이름이 '질문', '답변', '이름'인지 확인하세요.")

    st.divider()
    if st.button("🔀 퀴즈 순서 섞기", use_container_width=True):
        random.shuffle(st.session_state.quiz_data)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.rerun()

# 메인 화면 영역
current_quiz = st.session_state.quiz_data[st.session_state.current_index]

# 진행 상황 표시
st.progress((st.session_state.current_index + 1) / len(st.session_state.quiz_data))
st.write(f"**문제 {st.session_state.current_index + 1} / {len(st.session_state.quiz_data)}**")

# 퀴즈 카드 표시
with st.container(border=True):
    st.subheader(f"Q. {current_quiz['질문']}")
    st.info(f"💬 \"{current_quiz['답변']}\"")
    
    # 정답 공개 상태 확인
    if st.session_state.show_answer:
        st.success(f"🎉 **정답: {current_quiz['이름']}**")
    else:
        st.warning("❓ **이 답변의 주인공은 누구일까요?**")

# 버튼 제어 영역
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👀 정답 공개", use_container_width=True, type="primary"):
        st.session_state.show_answer = True
        st.balloons()  # 폭죽 효과 연출
        st.rerun()

with col2:
    if st.button("➡️ 다음 문제", use_container_width=True):
        if st.session_state.current_index < len(st.session_state.quiz_data) - 1:
            st.session_state.current_index += 1
        else:
            st.session_state.current_index = 0  # 처음으로 돌아가기
        st.session_state.show_answer = False
        st.rerun()

with col3:
    if st.button("🔄 처음부터 다시", use_container_width=True):
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.rerun()