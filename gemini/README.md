# 語音轉文字應用程式 (Voice to Text Application)

這個應用程式可以從麥克風錄製語音，並使用 Google Gemini API 將語音轉換為文字。

## 功能特色

- 從麥克風錄製語音 (預設 5 秒)
- 使用 Google Gemini API 進行語音轉文字
- 支援 WAV 格式音訊檔案
- 支援環境變數管理 API 金鑰

## 環境需求

- Python 3.7 或更高版本
- 麥克風 (用於錄音)

## 安裝步驟

1. 確保已安裝 Python 3.7+
2. 建立虛擬環境:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. 安裝依賴套件:

```bash
pip install pyaudio google-generativeai python-dotenv
```

## 使用方法

1. 獲取 Google API 金鑰:
   - 前往 [Google Cloud Console](https://console.cloud.google.com/)
   - 啟用 Gemini API
   - 建立 API 金鑰

2. 執行應用程式:

```bash
python voice_to_text.py
```

3. 當提示時輸入您的 API 金鑰，或使用以下方法設定環境變數
4. 開始錄音，應用程式將會錄製 5 秒鐘的語音
5. 應用程式會自動將語音轉換為文字並顯示結果

## 設定環境變數

### 方法 1: 使用 .env 檔案
1. 複製範例環境變數檔案:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```
2. 編輯 `.env` 檔案並輸入您的 API 金鑰:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
3. 執行程式時會自動載入環境變數

### 方法 2: 系統環境變數
您也可以將 API 金鑰設定為系統環境變數:

```bash
export GOOGLE_API_KEY='your_api_key_here'
```

在 Windows 上:

```cmd
set GOOGLE_API_KEY=your_api_key_here
```

### 方法 3: 直接輸入
當程式執行時，直接輸入您的 API 金鑰

## 程式碼說明

- `record_audio()`: 從麥克風錄製音訊並儲存為 WAV 檔案
- `transcribe_audio_with_gemini()`: 使用 Gemini API 將音訊轉換為文字
- `main()`: 主要執行流程

## 注意事項

- 需要有有效的 Google API 金鑰才能使用 Gemini API
- 音訊檔案會被暫時儲存並在處理完成後刪除
- 確保麥克風正常工作

## 自訂設定

您可以修改以下參數來調整錄音品質:

- `CHUNK`: 音訊資料塊大小
- `FORMAT`: 音訊格式 (預設 16 位元)
- `CHANNELS`: 音訊通道 (1 = 單聲道, 2 = 立體聲)
- `RATE`: 取樣率 (Hz)
- `RECORD_SECONDS`: 錄音時間 (秒)

## API 模型

此應用程式使用 `gemini-1.5-pro` 模型，該模型支援音訊輸入進行語音轉文字。