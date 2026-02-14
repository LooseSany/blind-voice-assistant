# Voice Assistant for Visually Impaired (Test APK)

This is a **starter Python Android app** built with **Kivy**.
It supports:
- Voice input (Android speech recognizer)
- Spoken responses (TTS)
- To-Do list commands
- Open common apps
- Navigation via Google Maps

## 1) Local development (desktop test)
```bash
pip install -r requirements.txt
python main.py
```

Note: Desktop voice capture is not wired. Use command text input on desktop.

## 2) Build APK (recommended on Linux/WSL/VM)
Buildozer does not build APK reliably on native Windows. Use WSL Ubuntu or Linux:

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev
pip install --upgrade pip
pip install buildozer cython==0.29.37
```

Then in project folder:
```bash
buildozer android debug
```

APK output:
- `bin/voiceassistant-0.1-arm64-v8a-debug.apk` (name may vary)

## 2A) Build APK on GitHub (no local setup)
This repo includes `.github/workflows/build-apk.yml`.

1. Push this folder to a GitHub repo.
2. Open GitHub -> `Actions` -> `Build Android APK`.
3. Click `Run workflow`.
4. After the job finishes, download artifact `blind-voice-assistant-apk`.

This gives you a ready debug APK from cloud CI.

## 3) First test commands
Try these in command box or voice button:
- `add todo buy medicines`
- `show todos`
- `open youtube`
- `open calculator`
- `navigate to nearest hospital`
- `time`
- `help`

## 4) Important notes
- This is a **test prototype** for tomorrow’s demo.
- For a production blind-assistant agent, you should add:
  - Wake-word handling
  - Better NLP (intent parser / LLM)
  - Offline fallback STT/TTS
  - Emergency/SOS flows
  - Accessibility testing with real users