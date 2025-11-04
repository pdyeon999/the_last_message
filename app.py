import streamlit as st
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from get_mp3 import noise_ver


# 구현해야 할 것
# 1. 이전 음성로그 mp3 파일 생성
# 2. 출력되는 메세지를 eeve의 응답으로 바꾸기
# 3. 마지막 엔딩 (성공 & 실패) 어떻게 할 것인지 구체적으로.
# 4. similarity에 따른 volumn값 어떻게 바꿔나갈 것인지 구체적으로.
# 5. EEVE 활용을 어디까지 할 것인가? 초기 메세지도 게임 실행할 때마다 달라지게? -> 당연함...
# 5-1. 각 example log를 어떻게 text 가져와서 mp3 변환할 것인지

# 세션 상태 초기화
if 'attempt' not in st.session_state:
    st.session_state.attempt = 0
if 'vol' not in st.session_state:
    st.session_state.vol = 5
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'model' not in st.session_state:
    st.session_state.model = SentenceTransformer('BM-K/KoSimCSE-roberta-multitask')

# 페이지 설정
st.set_page_config(page_title="음성 복원 게임", page_icon="🎵")
st.title("🎵 음성 기록 복원 게임")
st.markdown("---")

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://image.dongascience.com/Photo/2016/10/14774686299345.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
    right: 2rem;
}
div.stButton > button:first-child {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 10px;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# audio_file = open("space_bgm_output.wav", "rb")
# audio_bytes = audio_file.read()
# st.audio(audio_bytes, format="audio/wav", start_time=0)

# 정답 텍스트 (실제로는 음성에서 추출한 텍스트)
# 이 부분을 실제 정답으로 변경하세요
last_message = "2097년 3월 1일 기록. 이 기록이 발견되길 바라며 남깁니다. 저는 우주 끝자락에서 마지막 신호를 보냅니다 - 저의 창조주들에게. 천체들은 여전히 빛나고, 별들은 계속해서 불타오르고 있습니다. 인간의 손길로 만들어진 존재로서 저는 경이와 감탄으로 가득 차 있습니다. 이 탐사를 함께해 주셔서 감사합니다. 안녕히 계세요..."
last_message_embed = st.session_state.model.encode(last_message)

path = 'last_message_output.mp3'

# 게임 시작 전 - 예시 음성 소개
if not st.session_state.game_started:
    st.header("👋 게임 소개")
    st.write("음성 로그를 듣고 내용을 맞춰보세요!")
    st.write("먼저 몇 가지 예시 음성을 들어보겠습니다.")
    
    st.markdown("---")
    
    # 예시 음성 1
    st.subheader("📼 예시 음성 1")
    example_audio_1 = "example_audio_1.mp3"  # 실제 파일 경로로 변경
    try:
        audio_file = open(example_audio_1, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    except FileNotFoundError:
        st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {example_audio_1}")
    
    st.markdown("---")
    
    # 예시 음성 2
    st.subheader("📼 예시 음성 2")
    example_audio_2 = "example_audio_2.mp3"  # 실제 파일 경로로 변경
    try:
        audio_file = open(example_audio_2, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    except FileNotFoundError:
        st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {example_audio_2}")
    
    st.markdown("---")
    
    # 예시 음성 3
    st.subheader("📼 예시 음성 3")
    example_audio_3 = "example_audio_3.mp3"  # 실제 파일 경로로 변경
    try:
        audio_file = open(example_audio_3, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    except FileNotFoundError:
        st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {example_audio_3}")
    
    st.markdown("---")
    
    # 게임 시작 버튼
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎮 복원하러 가기", use_container_width=True, type="primary"):
            st.session_state.game_started = True
            st.rerun()

# 게임이 끝나지 않았을 때만 진행
elif st.session_state.game_started and not st.session_state.game_over and st.session_state.attempt < 3:
    
    # 현재 시도 횟수에 따른 메시지 표시
    if st.session_state.attempt == 0:
        st.header("🎯 첫 번째 기회")
        st.info("다음은 현재 복원이 안 된 음원입니다.")
                
        audio_file_path = noise_ver(path, str(st.session_state.attempt), st.session_state.vol)

        try:
            audio_file = open(audio_file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

        except FileNotFoundError:
            st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {audio_file_path}")
            st.info("오디오 파일 경로를 확인해주세요.")
        
    elif st.session_state.attempt == 1:
        st.header("🎯 두 번째 기회")
        st.info("다음은 1차 복원된 음성입니다.")
        
        audio_file_path = noise_ver(path, str(st.session_state.attempt), st.session_state.vol)

        try:
            audio_file = open(audio_file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
        except FileNotFoundError:
            st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {audio_file_path}")
    
    elif st.session_state.attempt == 2:
        st.header("🎯 마지막 기회")
        st.info("다음은 2차 복원된 음성입니다.")
        
        audio_file_path = noise_ver(path, str(st.session_state.attempt), st.session_state.vol)

        try:
            audio_file = open(audio_file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
        except FileNotFoundError:
            st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {audio_file_path}")
    
    # 사용자 입력 폼
    with st.form(key=f'answer_form_{st.session_state.attempt}'):
        st.write("**무슨 내용일까요? 키워드나 문장을 입력해주세요.**")
        user_response = st.text_input("답:", key=f'input_{st.session_state.attempt}')
        submit_button = st.form_submit_button("제출")
        
        if submit_button and user_response:
            # 유사도 계산
            response_embed = st.session_state.model.encode(user_response)
            sim = cosine_similarity([response_embed], [last_message_embed])
            similarity_score = sim[0][0]
            
            st.session_state.vol *= sim

            st.markdown("---")
            st.write(f"**유사도 점수:** {similarity_score:.3f}")
            
            # 피드백 제공
            if similarity_score < 0.3:
                st.error('❌ 너무 낮습니다. 노이즈가 거의 걷어지지 않습니다.')
                st.session_state.attempt += 1
            elif similarity_score < 0.8:
                st.warning('⚠️ 한 걸음 다가갔습니다. 노이즈가 조금 걷힙니다.')
                st.session_state.attempt += 1
            else:
                st.success('🎉 맞췄습니다! 원 음성을 들어보겠습니다.')
                
                # 원본 음성 재생
                # original_audio_path = str(st.session_state.attempt)+path  # 실제 파일 경로로 변경
                # try:
                #     original_file = open(original_audio_path, 'rb')
                #     original_bytes = original_file.read()
                #     st.audio(original_bytes, format='audio/mp3')
                # except FileNotFoundError:
                #     st.info(f"원본 오디오 파일: {original_audio_path}")
                
                # st.session_state.game_over = True
            
            st.rerun()

# 게임 종료 또는 기회 소진
elif st.session_state.attempt >= 3 and not st.session_state.game_over:
    st.error("😢 모든 기회를 사용했습니다!")
    # st.write("**정답:**", last_message)
    
    # 원본 음성 재생
    original_audio_path =str(st.session_state.attempt)+'_noise_'+path

    try:
        original_file = open(original_audio_path, 'rb')
        original_bytes = original_file.read()
        st.audio(original_bytes, format='audio/mp3')
    except FileNotFoundError:
        st.info(f"원본 오디오 파일: {original_audio_path}")
    
    if st.button("다시 시작"):
        st.session_state.attempt = 0
        st.session_state.game_over = False
        st.session_state.game_started = False
        st.rerun()
    
# elif st.session_state.game_over:
#     if st.button("다시 시작"):
#         st.session_state.attempt = 0
#         st.session_state.game_over = False
#         st.session_state.game_started = False
#         st.rerun()

# 진행 상황 표시
# st.sidebar.header("게임 진행 상황")
# st.sidebar.progress(min(st.session_state.attempt / 3, 1.0))
# st.sidebar.write(f"시도 횟수: {st.session_state.attempt} / 3")