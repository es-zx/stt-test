import pyaudio
import wave
import tempfile
import os
import time
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from dotenv import load_dotenv
import logging

# Suppress gRPC ALTS warnings
os.environ["GRPC_DISABLE_ALTS_SERVER_CHECK"] = "1"
# Disable gRPC's default logging for ALTS
os.environ["GRPC_VERBOSITY"] = "NONE"
logging.getLogger("googleapiclient").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

# Load environment variables from .env file
load_dotenv()

# Configuration for audio recording
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate
RECORD_SECONDS = 5  # Duration of recording

def record_audio(filename, duration=RECORD_SECONDS):
    """
    Records audio from the microphone and saves it to a file.
    
    Args:
        filename (str): Path to save the recorded audio
        duration (int): Duration of recording in seconds
    """
    p = pyaudio.PyAudio()

    print("開始錄音...")
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("錄音完成!")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio_with_gemini(audio_file_path, api_key):
    """
    Transcribes audio using the Gemini API.
    
    Args:
        audio_file_path (str): Path to the audio file to transcribe
        api_key (str): Your Google API key
    
    Returns:
        tuple: (transcribed text, upload_time, conversion_time)
    """
    # Configure the API key
    genai.configure(api_key=api_key)
    
    # Track upload time
    upload_start_time = time.time()
    
    # Upload the audio file to Google's servers
    audio_file = genai.upload_file(path=audio_file_path)
    
    # Wait for the upload to complete
    while audio_file.state.name == "PROCESSING":
        time.sleep(0.1)
        audio_file = genai.get_file(audio_file.name)
    
    if audio_file.state.name == "FAILED":
        raise ValueError("Audio file upload failed")
    
    upload_end_time = time.time()
    upload_time = upload_end_time - upload_start_time
    
    # Track conversion time
    conversion_start_time = time.time()
    
    # Choose the model that supports audio input
    model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite")
    
    # Create a text prompt to instruct the model to transcribe
    prompt = "Please transcribe this audio to text. Return only the transcribed text without any additional comments."
    
    try:
        # Generate content using both the audio and text prompt
        response = model.generate_content([audio_file, prompt])
        conversion_end_time = time.time()
        conversion_time = conversion_end_time - conversion_start_time
        return response.text, upload_time, conversion_time
    except Exception as e:
        print(f"Error during transcription: {e}")
        conversion_end_time = time.time()
        conversion_time = conversion_end_time - conversion_start_time
        return None, upload_time, conversion_time

def main():
    """
    Main function to run the voice to text application.
    """
    # Get API key from environment variable or user input
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        api_key = input("請輸入您的 Google API 金鑰: ")
    
    if not api_key:
        print("錯誤: 必須提供 API 金鑰")
        return

    # Create a temporary file for the audio recording
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
        temp_filename = temp_audio_file.name

    try:
        # Record audio from microphone
        start_time = time.time()
        record_audio(temp_filename, RECORD_SECONDS)
        recording_end_time = time.time()
        
        # Transcribe the recorded audio using Gemini API
        print("正在將語音轉換為文字...")
        transcribed_text, upload_time, conversion_time = transcribe_audio_with_gemini(temp_filename, api_key)
        conversion_end_time = time.time()
        
        if transcribed_text:
            print("\n轉錄結果:")
            print(transcribed_text)
            
            # Calculate and display the time difference between recording completion and conversion completion
            time_from_recording_to_conversion = conversion_end_time - recording_end_time
            
            print(f"\n錄音完成到轉換完成時間差: {time_from_recording_to_conversion:.2f} 秒")
            print(f"上傳時間: {upload_time:.2f} 秒")
            print(f"轉換時間: {conversion_time:.2f} 秒")
        else:
            print("轉錄失敗")
            
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == "__main__":
    main()