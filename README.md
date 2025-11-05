# 🎮 The Last Message  
> 인공지능이 마지막 메시지를 복원하고 들려주는 감정형 대화 복원기

---

## 🧠 프로젝트 소개
이 프로젝트는 **Streamlit**, **Ollama (EEVE 모델)**, **OpenAI API**, 그리고 **RunPod GPU 클라우드**를 기반으로,
손상된 음성을 AI가 분석하고 복원하여 사용자가 다시 들을 수 있도록 만든 웹 애플리케이션입니다.

---

## ⚙️ 주요 기능
| 기능명 | 설명 |
|--------|------|
| 🎧 음성 업로드 | 사용자가 음성 파일을 업로드하면 내부적으로 분석을 시작합니다. |
| 🧩 음성 복원 | Ollama EEVE 모델을 이용해 손상된 부분의 의미를 추정 및 재구성합니다. |
| 💬 텍스트 분석 | 복원된 내용을 SentenceTransformer로 임베딩하고 유사도 기반으로 정제합니다. |
| 🔊 음성 재생 | gTTS와 pydub을 이용해 AI가 복원한 메시지를 음성으로 재생합니다. |
| ⚙️ 노이즈 및 이펙트 처리 | WhiteNoise + pitch + speed 조절을 통한 디지털 톤 합성 |
| ☁️ 클라우드 실행 | RunPod GPU 환경에서 Streamlit으로 웹 인터페이스 제공 |

---

## 🧰 기술 스택
| 분류 | 사용 기술 |
|------|------------|
| Backend | Python 3.12, Ollama, OpenAI API, Hugging Face Transformers |
| Frontend | Streamlit |
| Audio | pydub, gTTS |
| NLP | SentenceTransformer, scikit-learn |
| Infra | RunPod (GPU), dotenv, requirements.txt |

---

## 🖼️ 화면 구성
### 🏠 메인 페이지
- 간단한 소개 및 음성 업로드 버튼  
- 배경 BGM과 함께 감정적인 분위기 구성  

### 🎵 복원 결과 페이지
- AI가 생성한 “마지막 메시지” 텍스트 출력  
- 복원된 음성 재생 버튼 제공  
- Streamlit의 `st.audio()` 및 `st.video()`로 인터랙션 구현  

### ⚙️ 예시 화면
| 화면 | 설명 |
|------|------|
| ![upload](images/upload.png) | 음성 파일 업로드 화면 |
| ![result](images/result.png) | 복원 결과와 음성 재생 화면 |

---

## 🚀 실행 방법
### 1️⃣ 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
