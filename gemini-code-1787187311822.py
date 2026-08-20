import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="우리 반 친퀴즈!", page_icon="🧩", layout="centered")

st.title("🧩 우리 반 친퀴즈!")
st.caption("질문과 답변을 보고 주인공이 누구인지 맞춰보세요!")

# 세션 상태 초기화
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "filtered_quiz" not in st.session_state:
    st.session_state.filtered_quiz = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# 사이드바: 엑셀 파일 업로드 및 반 선택
with st.sidebar:
    st.header("⚙️ 퀴즈 데이터 설정")
    uploaded_file = st.file_uploader("엑셀 파일 업로드 (.xlsx)", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            # 엑셀 파일 읽기
            df = pd.read_excel(uploaded_file)
            
            # '반' 컬럼이 있는 경우 학급 선택 필터 제공
            if "반" in df.columns:
                classes = sorted(df["반"].dropna().unique())
                selected_class = st.selectbox("🎯 학급 선택", classes)
                
                # 선택한 반의 데이터만 추출
                filtered_df = df[df["반"] == selected_class]
            else:
                filtered_df = df
            
            # 퀴즈 데이터 변환
            st.session_state.filtered_quiz = filtered_df.to_dict("records")
            st.success(f"총 {len(st.session_state.filtered_quiz)}명의 데이터를 불러왔습니다!")
            
        except Exception as e:
            st.error("파일을 읽는 중 오류가 발생했습니다. 열 이름이 정확한지 확인해 주세요.")

    st.divider()
    if st.button("🔀 퀴즈 순서 섞기", use_container_width=True):
        if st.session_state.filtered_quiz:
            random.shuffle(st.session_state.filtered_quiz)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()

# 메인 화면 영역
if st.session_state.filtered_quiz:
    current_quiz = st.session_state.filtered_quiz[st.session_state.current_index]

    # 진행 상황 표시
    st.progress((st.session_state.current_index + 1) / len(st.session_state.filtered_quiz))
    st.write(f"**문제 {st.session_state.current_index + 1} / {len(st.session_state.filtered_quiz)}**")

    # 퀴즈 카드 표시
    with st.container(border=True):
        st.subheader(f"Q. {current_quiz.get('질문', '질문 없음')}")
        st.info(f"💬 \"{current_quiz.get('답변', '답변 없음')}\"")
        
        if st.session_state.show_answer:
            st.success(f"🎉 **정답: {current_quiz.get('이름', '이름 없음')}**")
        else:
            st.warning("❓ **이 답변의 주인공은 누구일까요?**")

    # 버튼 제어 영역
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👀 정답 공개", use_container_width=True, type="primary"):
            st.session_state.show_answer = True
            st.balloons()
            st.rerun()

    with col2:
        if st.button("➡️ 다음 문제", use_container_width=True):
            if st.session_state.current_index < len(st.session_state.filtered_quiz) - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()

    with col3:
        if st.button("🔄 처음부터 다시", use_container_width=True):
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()

else:
    st.info("👈 왼쪽 사이드바에서 엑셀(.xlsx) 파일을 업로드해 주세요!")
