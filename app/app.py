import streamlit as st
from pathlib import Path
import os
import yt_dlp
from extract_audio import process_video
from accent_predictor import detect_accent
import subprocess
import sys

# === Function to Install Missing Packages ===
def install_requirements():
    try:
        # Check if pip is available and requirements.txt exists
        requirements_path = Path(__file__).parent / 'requirements.txt'
        if requirements_path.exists():
            st.text("📦 Installing missing packages from requirements.txt...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
            st.success("✅ Packages installed successfully.")
        else:
            st.warning("⚠️ No requirements.txt file found. Please ensure it's uploaded if needed.")
    except Exception as e:
        st.error(f"❌ Error installing packages: {e}")

# === General Settings ===
st.set_page_config(page_title="Accent Detector", layout="centered")
st.title("🧠🎙️ English Accent & Language Detector")

# === Install Requirements if needed ===
install_requirements()

# === Path Variables ===
OUTPUT_AUDIO_DIR = Path("output") / "audio"
OUTPUT_TEXT_DIR = Path("output") / "text"

# Ensure output directories exist
OUTPUT_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_TEXT_DIR.mkdir(parents=True, exist_ok=True)

# === UI ===
input_source = st.radio("📥 Choose video source:", ["Upload File", "Provide a Link"])

video_path = None
if input_source == "Upload File":
    uploaded_file = st.file_uploader("🎬 Upload your video (mp4, mkv)", type=["mp4", "mkv"])
    if uploaded_file:
        video_path = OUTPUT_AUDIO_DIR / "uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ File uploaded successfully")
else:
    video_url = st.text_input("🔗 Enter the video link")
    if video_url:
        try:
            with st.spinner("Downloading video from YouTube..."):
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': str(OUTPUT_AUDIO_DIR / "downloaded_video.mp4"),  # Path to save the video
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                video_path = OUTPUT_AUDIO_DIR / "downloaded_video.mp4"
                st.success("✅ Video downloaded successfully")
        except Exception as e:
            st.error(f"❌ Error downloading video: {e}")

if video_path and st.button("🚀 Start Analysis"):
    # Extract audio from video
    with st.spinner("Extracting audio from video..."):
        audio_path = process_video(str(video_path), output_filename="audio.wav")

    # Detect language and accent
    with st.spinner("Detecting language and accent..."):
        result = detect_accent(str(audio_path))  # Just detect accent now

    # === Show Results ===
    st.markdown("### 🧾 Final Results")
    st.markdown(f"**🗣️ English Accent:** `{result['accent']}`  ")
    st.markdown(f"**📈 Accent Confidence:** `{round(result['accent_score']*100, 2)}%`  ")

    st.markdown("---")
    with st.expander("📜 Show Full Transcript"):
        st.text("This is a placeholder for full transcript.")  # You can replace this with the actual transcript content

    st.balloons()
