#!/usr/bin/env python3
# Real-time speech-to-text using Vosk

import json
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import opencc

# Set up audio parameters
samplerate = 16000  # Vosk model works with 16kHz audio
channels = 1

# Initialize OpenCC for Traditional Chinese conversion
cc = opencc.OpenCC('s2t')  # Convert from Simplified to Traditional Chinese

# Set up audio queue for processing
q = queue.Queue()

def callback(indata, frames, time, status):
    # Callback function to handle incoming audio data
    if status:
        print(f"Audio status: {status}", file=sys.stderr)
    # Add audio data to queue as bytes
    q.put(bytes(indata))

def recognize_speech(model_path):
    # Main function to recognize speech in real-time
    print("Loading model...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, samplerate)
    recognizer.SetWords(True)  # Enable word-level timestamps if needed

    print("Starting real-time recognition. Press Ctrl+C to stop.")
    print("Speak now...")

    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,  # Process audio in chunks
        dtype='int16',
        channels=channels,
        callback=callback
    ):
        while True:
            try:
                # Get audio data from queue
                data = q.get()
                
                # Perform recognition
                if recognizer.AcceptWaveform(data):
                    # Get the final result
                    result = recognizer.Result()
                    result_dict = json.loads(result)
                    if 'text' in result_dict and result_dict['text']:
                        # Convert Simplified Chinese to Traditional Chinese
                        simplified_text = result_dict['text']
                        traditional_text = cc.convert(simplified_text)
                        print(traditional_text)
                else:
                    # Get partial result (interim recognition)
                    partial_result = recognizer.PartialResult()
                    partial_dict = json.loads(partial_result)
                    if 'partial' in partial_dict and partial_dict['partial']:
                        # Convert Simplified Chinese to Traditional Chinese for partial results too
                        simplified_partial = partial_dict['partial']
                        traditional_partial = cc.convert(simplified_partial)
                        print(traditional_partial, end='\r', flush=True)
            except KeyboardInterrupt:
                print("")
                print("Stopping recognition...")
                break

if __name__ == "__main__":
    # Path to the Vosk model
    # You'll need to download the model first
    MODEL_PATH = "model"  # Change this to your model path
    
    if len(sys.argv) > 1:
        MODEL_PATH = sys.argv[1]
    
    recognize_speech(MODEL_PATH)