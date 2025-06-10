import os
import shutil
from speechbrain.pretrained import EncoderClassifier
from tkinter import filedialog
from tkinter import Tk

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
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Get the dynamic path to the "output/extracted_audio" folder
    audio_folder = os.path.join(os.path.dirname(__file__), "output", "extracted_audio")  # Dynamic folder path

    # Open the file dialog in the extracted_audio folder
    file_path = filedialog.askopenfilename(
        title="Select Audio File", 
        filetypes=[("WAV Files", "*.wav")],
        initialdir=audio_folder  # Start file dialog in extracted_audio folder
    )
    return file_path

# === Final Accent Detection Function ===
def detect_accent(audio_path: str):
    accent, confidence = detect_accent_from_audio(audio_path)  # Detect accent from the audio file
    return {
        "accent": accent,
        "accent_score": confidence
    }

# === Test the Code ===
if __name__ == "__main__":
    audio_file = select_audio_file()  # Ask the user to select an audio file
    if not audio_file:
        print("❌ No audio file selected.")
    else:
        # Detect accent
        result = detect_accent(audio_file)

        # Display the results
        print("Accent:", result["accent"])
        print("Accent Confidence:", result["accent_score"])
