# Accent & Language Detector

This project uses machine learning to detect English accents and languages from video or audio files. It allows users to upload video files or provide a YouTube link, extract the audio, and then classify the accent and language using pre-trained models. The app is built with **Streamlit** for the front-end and **SpeechBrain** for accent detection.

## Project Structure

- **models/**: Contains the pre-trained models for accent detection.
- **app/**: Contains the main app code for accent detection and user interaction.
- **output/**: Directory for saving extracted audio and video files.
- **extract_audio.py**: Handles video downloading and audio extraction.
- **accent_predictor.py**: Contains the model for accent prediction.

## Features

- Upload video or provide a YouTube link to detect the accent.
- Extract audio from the video and predict the accent.
- Display the predicted accent with a confidence score.

## Installation

### 1. Clone the repository

Clone the project to your local machine:

```bash
git clone https://github.com/mahankh80/accent.git
cd accent
2. Set up a virtual environment (optional)
3. Install dependencies
pip install -r requirements.txt

Usage:

******run as adminstrator*****
Run the Streamlit app:
streamlit run app/app.py
The app will prompt you to upload a video or provide a YouTube link.
The video’s audio will be extracted, and the accent prediction will be displayed along with the confidence score.

Dependencies:

speechbrain: For accent detection.
streamlit: For the web interface.
yt-dlp: For downloading videos from YouTube.
requests: For handling HTTP requests.
ffmpeg: For extracting audio from video files.


