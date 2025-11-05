# 🎮 The Last Message  
> 인공지능이 남긴 마지막 음성 메시지를 복원하는 게임

---

## 🧠 게임 소개
이 게임은 노이즈가 낀 음성을 듣고 맞추는 게임입니다.

## 🛎️ 게임 규칙
1. 먼저 복원된 세 개의 음성을 듣습니다.
2. 마지막 음성을 듣고 빠르게 타자를 쳐서 들린 내용을 입력합니다.
3. 기회는 세 번입니다.
4. 유사도가 0.7 이상 나오면 복원에 성공합니다.
5. 0.7을 못넘은 채 세 번의 기회가 끝나면 복원에 실패하고 게임이 종료됩니다.
---

## ⚙️ 주요 기능
| 기능명 | 설명 |
|--------|------|
| 🎧 음성 변환 | 게임 시작 시 EEVE가 생성한 텍스트를 기반으로 OpenAI의 tts-1모델을 사용해 음성 파일 네 개 생성 |
| 💬 유사도 분석 | 플레이어가 입력한 내용을 SentenceTransformer로 임베딩하여 코사인 유사도로 값 도출 |
| ⚙️ 노이즈 및 이펙트 처리 | pydub의 WhiteNoise + pitch + speed 조절을 통해 디지털 톤 합성 |
| ☁️ 클라우드 실행 | RunPod GPU 환경에서 Streamlit으로 웹 인터페이스 제공 |

---

## 🧰 기술 스택
| 분류 | 사용 기술 |
|------|------------|
| Backend | Python 3.12, Ollama, OpenAI API, Hugging Face Transformers |
| Frontend | Streamlit |
| Audio | pydub |
| NLP | SentenceTransformer |
| Infra | RunPod (GPU), dotenv, requirements.txt |

---

## 🖼️ 화면 구성
### ⚙️ 예시 화면
(사진 첨부)

---

## 🚀 실행 방법
### 1️⃣ 로컬 실행
```bash
streamlit run app.py
```

## 2️⃣ RunPod 클라우드 실행

1. RunPod Workspace 생성 (Port 7860 추가)

2. requirements.txt 설치

3. .env 파일에 API 키 추가

4. 실행
```bash
streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=false --server.port=7860 --server.address=0.0.0.0
```



## 💡 트러블슈팅 & 팁

* Ollama 연결 오류 → 모델 설치 후 ollama pull EEVE 확인, `pip install Ollama`

* OpenAI 키 인식 실패 → 환경변수 추가
```bash
echo 'export OPENAI_API_KEY=(키)' >> ~/.bashrc
source ~/.bashrc
```
* Streamlit 접속 실패 (502) → RunPod Port 7860 설정 확인, import 오류 확인


---

### 🙌 마무리
감사합니다.