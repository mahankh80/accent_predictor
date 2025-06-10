import os
import shutil
from speechbrain.pretrained import EncoderClassifier
import streamlit as st

# === Load Accent Detection Model ===
def load_accent_model():
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "accent-id-commonaccent_ecapa")  # Path to accent model
    hyperparams_path = os.path.join(model_path, "hyperparams.yaml")
    if not os.path.exists(hyperparams_path):
        print(f"❌ Hyperparameters file not found at: {hyperparams_path}")
        return None  # Handle the case where the model is not found

    model = EncoderClassifier.from_hparams(
        source=model_path,  # Path to model
        savedir=model_path,  # Save the model in the same directory
    )
    return model

# === Predict Accent from Audio File ===
def detect_accent_from_audio(audio_path: str):
    print(f"Checking audio file at path: {audio_path}")
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found at: {audio_path}")
        return None, None
    
    model = load_accent_model()  # Load the accent model
    if model is None:
        return None, None
    
    try:
        temp_audio_dir = os.path.join(os.path.dirname(__file__), "temp_audio")
        if not os.path.exists(temp_audio_dir):
            os.makedirs(temp_audio_dir)  # Create folder if not existing
        
        audio_copy_path = os.path.join(temp_audio_dir, "audio.wav")
        print(f"Copying audio to: {audio_copy_path}")
        shutil.copy(audio_path, audio_copy_path)  # Copy the audio file to the new location
        
        result = model.classify_file(audio_copy_path)  # Classify the accent
        print(f"Classification result: {result}")
        accent = result[3][0]  # Predicted accent
        confidence = result[1].item()  # Confidence in the prediction
        return accent, confidence
    
    except Exception as e:
        print(f"❌ Error copying audio file: {e}")
        return None, None

# === Select Audio File via File Dialog ===
def select_audio_file():
    uploaded_file = st.file_uploader("Upload your audio file", type=["wav"])
    if uploaded_file is not None:
        # Save the uploaded file to a temporary directory
        temp_audio_path = os.path.join(os.path.dirname(__file__), "output", "extracted_audio", uploaded_file.name)
        with open(temp_audio_path, "wb") as f:
            f.write(uploaded_file.read())
        return temp_audio_path
    return None

# === Final Accent Detection Function ===
def detect_accent(audio_path: str):
    accent, confidence = detect_accent_from_audio(audio_path)  # Detect accent from the audio file
    return {
        "accent": accent,
        "accent_score": confidence
    }

# === Streamlit UI ===
if __name__ == "__main__":
    st.title("🧠🎙️ English Accent & Language Detector")

    audio_file = select_audio_file()  # Ask the user to upload an audio file
    if not audio_file:
        st.error("❌ No audio file selected.")
    else:
        # Detect accent
        result = detect_accent(audio_file)

        # Display the results
        st.markdown("### 🧾 Final Results")
        st.markdown(f"**🗣️ English Accent:** `{result['accent']}`  ")
        st.markdown(f"**📈 Accent Confidence:** `{round(result['accent_score']*100, 2)}%`  ")

        st.markdown("---")
        with st.expander("📜 Show Full Transcript"):
            st.text("This is a placeholder for full transcript.")  # You can replace this with the actual transcript content

        st.balloons()
