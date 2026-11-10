
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")

STT_URL = "https://api.vachana.ai/stt/v3"
TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"

st.set_page_config(
    page_title="English AI Voice Assistant",
    page_icon="🎓"
)

st.title("🎓 English AI Voice Assistant")
st.write("Your personal voice assistant for students.")

def get_answer(question):
    q = question.lower()

    if "python" in q:
        return "Python is a beginner friendly programming language. Learn variables, loops, functions and build small projects."

    elif "machine learning" in q:
        return "Machine learning helps computers learn patterns from data. Start with Python, NumPy, Pandas and Scikit learn."

    elif "exam" in q or "study" in q:
        return "Create a daily study timetable, understand important concepts and practise previous examination questions."

    elif "placement" in q or "job" in q:
        return "Prepare data structures, algorithms, Python, communication skills and practical projects."

    elif "internship" in q:
        return "Build two or three projects, prepare your resume and apply regularly for internships."

    else:
        return "Thank you for your question. I can help you with Python, machine learning, exams, placements and internships."

if not API_KEY:
    st.error("API key missing. Check your .env file.")
    st.stop()

audio = st.audio_input("🎤 Record your question in English")

if audio is not None:

    if st.button("Ask AI Assistant", type="primary"):

        try:
            with st.spinner("Recognizing your speech..."):

                headers = {
                    "X-API-Key-ID": API_KEY
                }

                files = {
                    "audio_file": (
                        "question.wav",
                        audio.getvalue(),
                        "audio/wav"
                    )
                }

                data = {
                    "language_code": "en-IN",
                    "preferred_language": "en-IN",
                    "format": "transcribe"
                }

                response = requests.post(
                    STT_URL,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=60
                )

                response.raise_for_status()

                result = response.json()
                question = result.get("transcript", "").strip()

            if not question:
                st.error("No speech recognized. Please record again.")
                st.stop()

            st.success("Speech recognized!")
            st.write("### Your question")
            st.write(question)

            answer = get_answer(question)

            st.write("### 🤖 AI Answer")
            st.write(answer)

            with st.spinner("Generating voice response..."):

                tts_headers = {
                    "X-API-Key-ID": API_KEY,
                    "Content-Type": "application/json"
                }

                payload = {
                    "text": answer,
                    "voice": "Yashvi",
                    "model": "timbre-v2.5",
                    "language": "en-IN",
                    "speed": 1.0,
                    "audio_config": {
                        "sample_rate": 48000,
                        "num_channels": 1,
                        "sample_width": 2,
                        "encoding": "linear_pcm",
                        "container": "wav"
                    }
                }

                tts_response = requests.post(
                    TTS_URL,
                    headers=tts_headers,
                    json=payload,
                    timeout=90
                )

                tts_response.raise_for_status()

            st.success("Voice response generated!")
            st.audio(
                tts_response.content,
                format="audio/wav"
            )

        except requests.exceptions.RequestException as e:
            st.error("Gnani API request failed.")
            st.code(str(e))

        except Exception as e:
            st.error("Unexpected error.")
            st.code(str(e))

st.divider()
st.caption("Powered by Gnani Prisma v2.5 and Timbre v2.5")
