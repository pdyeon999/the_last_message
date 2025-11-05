import streamlit as st
# import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from get_files import get_text_and_mp3, get_last_message, get_mp3
import time


# runpod에서 해보기... hugging face key랑 openai key 등록, streamlit 실행
# 리드미;;;


# 세션 상태 초기화
# '다시 시작'할 때마다 EEVE가 네 개의 메세지를 생성해야함
if 'messages' not in st.session_state:
    st.session_state.messages = False

# 시도 횟수 저장
if 'attempt' not in st.session_state:
    st.session_state.attempt = 0

# 노이즈 수정값
if 'vol' not in st.session_state:
    st.session_state.vol = 10

# 게임이 종료되었는지 여부
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# 게임이 시작 전 예시 음성 들려주기 위함
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# 유사도 검색 위한 임베딩 모델 저장
if 'model' not in st.session_state:
    st.session_state.model = SentenceTransformer('BM-K/KoSimCSE-roberta-multitask')

if 'last_message_embed' not in st.session_state:
    st.session_state.last_message_embed = 0

# 페이지 설정
st.set_page_config(page_title="음성 복원", page_icon="🎵")
st.title("🎵 음성 기록 복원")
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


path = 'log_4.mp3'
example_path = '_noise_log_'

# 게임 시작 전 or 다시 시작 시 EEVE text 받기, last_message 저장
if not st.session_state.messages:
    get_text_and_mp3()
    
    # 노이즈 낀 example 음성 세 개 생성
    for i in range(1, 4):
        get_mp3(f'log_{i}.mp3', '')

    last_message = get_last_message()
    print(last_message)
    st.session_state.last_message_embed = st.session_state.model.encode(last_message)

    st.session_state.messages = True
    
# 게임 시작 전 - 예시 음성 소개
if not st.session_state.game_started:
    st.header("👋 게임 소개")
    st.write("음성 로그를 듣고 내용을 맞춰보세요.")
    st.write("먼저 몇 가지 복원된 음성을 들어보겠습니다.")
    
    st.markdown("---")
    
    # 예시 음성 1
    st.subheader("📼 복원 음성 1")
    example_audio_1 = example_path+str(1)+'.mp3'  # 실제 파일 경로로 변경
    try:
        audio_file = open(example_audio_1, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    except FileNotFoundError:
        st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {example_audio_1}")
    
    st.markdown("---")
    
    # 예시 음성 2
    st.subheader("📼 복원 음성 2")
    example_audio_2 = example_path+str(2)+'.mp3'  # 실제 파일 경로로 변경
    try:
        audio_file = open(example_audio_2, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    except FileNotFoundError:
        st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {example_audio_2}")
    
    st.markdown("---")
    
    # 예시 음성 3
    st.subheader("📼 복원 음성 3")
    example_audio_3 = example_path+str(3)+'.mp3'  # 실제 파일 경로로 변경
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
                
        audio_file_path = get_mp3(path, str(st.session_state.attempt), st.session_state.vol)

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
        
        audio_file_path = get_mp3(path, str(st.session_state.attempt), st.session_state.vol)

        try:
            audio_file = open(audio_file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
        except FileNotFoundError:
            st.warning(f"⚠️ 오디오 파일을 찾을 수 없습니다: {audio_file_path}")
    
    elif st.session_state.attempt == 2:
        st.header("🎯 마지막 기회")
        st.info("다음은 2차 복원된 음성입니다.")
        
        audio_file_path = get_mp3(path, str(st.session_state.attempt), st.session_state.vol)

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
            sim = cosine_similarity([response_embed], [st.session_state.last_message_embed])
            similarity_score = sim[0][0]
            
            st.session_state.vol += similarity_score*10
            print('바뀐 vol:', st.session_state.vol)

            st.markdown("---")
            st.write(f"**유사도 점수:** {similarity_score:.3f}")
            
            # 피드백 제공
            if similarity_score < 0.3:
                st.error('❌ 너무 낮습니다. 노이즈가 거의 걷어지지 않습니다...')
                st.session_state.attempt += 1
            elif similarity_score < 0.7:
                st.warning('⚠️ 한 걸음 다가갔습니다. 노이즈가 조금 걷힙니다...')
                st.session_state.attempt += 1
            else:
                st.success('🎉 맞췄습니다!')
               
                st.session_state.game_over = True
            
            time.sleep(2)
            st.rerun()

# 게임 win
elif st.session_state.game_over == True:
    st.success('🎉 복원에 성공한 음성을 재생하겠습니다.')
                
    # 원본 음성 재생
    original_audio_path = get_mp3(path, str(st.session_state.attempt))  # 실제 파일 경로로 변경
    
    try:
        original_file = open(original_audio_path, 'rb')
        original_bytes = original_file.read()
        st.audio(original_bytes, format='audio/mp3')
    except FileNotFoundError:
        st.info(f"원본 오디오 파일: {original_audio_path}")

    if st.button("다시 하기"):
        st.session_state.attempt = 0
        st.session_state.vol = 10
        st.session_state.game_over = False
        st.session_state.game_started = False
        st.session_state.messages = False
        st.rerun()

# 게임 lose
elif st.session_state.attempt >= 3:
    st.error("😢 모든 기회를 사용했습니다!")
    # st.write("**정답:**", last_message)
    st.write("복원에 실패했습니다.")
    st.write("**게임 종료**")

    if st.button("다시 하기"):
        st.session_state.attempt = 0
        st.session_state.vol = 10
        st.session_state.game_over = False
        st.session_state.game_started = False
        st.session_state.messages = False
        st.rerun()


# elif st.session_state.game_over:
#     # 원본 음성 재생
#     original_audio_path =str(st.session_state.attempt)+'_noise_'+path
#     st.write("**마지막 음성을 듣겠습니다.**")

#     try:
#         original_file = open(original_audio_path, 'rb')
#         original_bytes = original_file.read()
#         st.audio(original_bytes, format='audio/mp3')
#     except FileNotFoundError:
#         st.info(f"원본 오디오 파일: {original_audio_path}")
#     time.sleep(3)
    
#     if st.button("다시 시작"):
#         st.session_state.attempt = 0
#         st.session_state.game_over = False
#         st.session_state.game_started = False
#         st.rerun()
