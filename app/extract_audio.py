import os
import shutil
import subprocess
import requests

# Path to the output folder outside of the app
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
EXTRACT_DIR = os.path.join(BASE_DIR, "output", "extracted_audio")

def ensure_output_dir():
    """Ensures the output directory exists. Creates it if not."""
    if not os.path.exists(EXTRACT_DIR):
        os.makedirs(EXTRACT_DIR)

def is_url(path):
    """Checks if the provided path is a URL."""
    return path.startswith("http://") or path.startswith("https://")

def download_video(url, save_path):
    """Downloads a video from a URL and saves it to the given path."""
    print(f"[⬇️] Downloading from {url}")
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception(f"❌ Failed to download video. Status: {response.status_code}")
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    print(f"[✔️] Video saved to {save_path}")

def extract_audio(video_path, audio_path):
    """Extracts audio from a video file and saves it to the specified path."""
    print("[🎧] Extracting audio...")
    command = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
    ]
    print(">>", " ".join(command))
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[✅] Audio saved to {audio_path}")

def process_video(input_path_or_url, output_filename="audio.wav"):
    """Process a video from either a URL or local file to extract audio."""
    ensure_output_dir()
    video_tmp_path = os.path.join(EXTRACT_DIR, "temp_video.mp4")
    audio_out_path = os.path.join(EXTRACT_DIR, output_filename)

    if is_url(input_path_or_url):
        download_video(input_path_or_url, video_tmp_path)
    else:
        if not os.path.exists(input_path_or_url):
            raise FileNotFoundError("❌ Local video file not found.")
        shutil.copy(input_path_or_url, video_tmp_path)
        print(f"[📁] Using local file: {input_path_or_url}")

    extract_audio(video_tmp_path, audio_out_path)
    os.remove(video_tmp_path)  # Remove the temporary video file
    return audio_out_path

# Test
if __name__ == "__main__":
    test_input = "123.mp4"  # Example local file for testing
    try:
        result = process_video(test_input)
        print(f"[🎯] Final audio path: {result}")
    except Exception as e:
        print("💥 Error:", e)
