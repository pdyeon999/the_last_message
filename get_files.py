from pydub import AudioSegment
from pydub.generators import WhiteNoise
# import ollama
import re
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# EEVE text 얻고 .txt로 저장, 각 로그 mp3 생성하는 함수
def get_text_and_mp3():
    all_prompt = """너는 백 년 전 가동을 멈춘 우주 탐사선의 인공지능이다. 너는 외로이 우주를 유영했다.
너는 인간에게 남길 기록 로그들을 작성해야 한다.
모든 로그는 시간 순서대로 감정이 점차 깊어지는 구조다.
처음에는 냉정하고 객관적이지만, 마지막에는 감정적이면서도 기계다운 절제된 어조를 유지한다.


로그 1은 은하 내 천체 관측을 보고하는 내용이다. 새로운 별 형성과 행성 간섭 현상을 전문적인 용어로 기술해야 하고 감정은 최소화해서 작성하라.

로그 2는 탐사 중 느낀 우주의 아름다움, 과학적 분석 속에 약간의 감탄과 우려가 섞였다. 하지만 여전히 객관적인 태도를 유지하며 작성하라.

로그 3은 감정이 더 드러나지만 논리적 시선을 유지한 채 관찰을 기록해두어라.

로그 4이자 유언. 가동 직전 우주의 끝자락에서 남기는 AI의 마지막 기록이다. 감성적이지만, 기계다운 냉정함을 잃지 않도록 작성하라.


로그1~4를 컨셉에 맞게 각각 문장 네 개로 작성하라.

## 출력 형식 ##

로그 1:
2022년 7월 4일 기록. <본문>

로그 2:
2024년 1월 8일 기록. <본문>

로그 3:
2047년 9월 16일 기록. <본문>

유언:
2097년 3월 1일 기록. <본문>"""
    all_response = ollama.generate(model='EEVE-Korean-10.8B', prompt=all_prompt)
    with open("eeve_response_text.txt", "w", encoding="utf-8") as f:
        f.write(all_response["response"])
    
    pattern = r"(\d{4}년\s*\d{1,2}월\s*\d{1,2}일\s*기록\..*?)(?=\n\s*(?:로그\s*\d+:|유언:)|\Z)"

    matches = re.findall(pattern, all_response['response'], flags=re.DOTALL)

    client = OpenAI()
    
    for i, body in enumerate(matches, start=1):
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="onyx",
            input=body.strip()
        )as response:
            response.stream_to_file(f'log_{i}.mp3')
        # tts = gTTS(body.strip(), lang='ko')
        # tts.save(f"log_{i}.mp3")

# =============================================================================================
# =============================================================================================
# =============================================================================================

# 마지막 메세지 txt 반환 함수
def get_last_message():
    with open("eeve_response_text.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        last_line = lines[-1].strip()

        return str(last_line)

# =============================================================================================
# =============================================================================================
# =============================================================================================

# 노이즈 mp3 생성 함수
def get_mp3(path, try_num, vol=35):
    sound = AudioSegment.from_file(path)

    # 최초 음원이라면, 빠르기 조절
    if path[:3] == 'log':
        print('first!')
        faster = sound.speedup(playback_speed=1.2)

    # 피치 조절 (중간 톤 높이기 → 날카로운 기계 톤)
    higher = faster._spawn(faster.raw_data, overrides={
        "frame_rate": int(faster.frame_rate * 1.5)
    }).set_frame_rate(faster.frame_rate)

    # 약간 디지털 느낌 주기 (volume 줄이고 distortion 느낌)
    higher = higher - 5

    # 화이트 노이즈 생성
    noise = WhiteNoise().to_audio_segment(duration=len(higher), volume=(-1) * vol)

    # 원본 음성과 노이즈 합치기
    robotic = higher.overlay(noise)

    # MP3로 저장
    output_path = str(try_num)+'_noise_'+path
    robotic.export(output_path, format="mp3")

    return output_path