# Vosk Chinese Language Model Setup

To use Chinese speech recognition, you need to download a Chinese language model from the Vosk website.

## Available Chinese Models:

1. Small Chinese model (about 50MB):
   - URL: https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip

2. Large Chinese model (better accuracy, ~1.4GB):
   - URL: https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip

## Setup Instructions:

1. Download one of the models above (recommend starting with the small model)

2. Extract the downloaded zip file

3. Rename the extracted folder to "model" or update the MODEL_PATH in speech_to_text.py

4. Place the model folder in the same directory as speech_to_text.py

## Example folder structure:
ttl2/
├── vosk_env/
├── speech_to_text.py
├── model/                 # <- Your extracted model folder
│   ├── am/
│   ├── ivector/
│   ├── model/
│   └── graph/
└── ...

## Running the Application:

1. Activate your virtual environment:
   ```bash
   vosk_env\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install vosk pyaudio sounddevice
   ```

3. Run the speech recognition:
   ```bash
   python speech_to_text.py
   ```

## Alternative - Using wget or curl on Windows:

If you have wget or curl available on your system, you can download the model directly:

For small model:
```
curl -L https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip -o vosk-model-small-cn.zip
```

Or with PowerShell:
```
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip" -OutFile "vosk-model-small-cn.zip"
```

After downloading, extract the zip file and rename the extracted folder to "model".