# Blind Assistant - Kotlin + Python (Chaquopy)

This Android-native project uses:
- Kotlin for Android UI + speech + intents
- Python for command parsing and assistant logic

Path: `android-chaquopy/`

## Features
- Voice input (speech recognizer)
- Text to speech responses
- To-do commands
- Open installed apps
- Navigation to a place using Google Maps

## Build APK in Android Studio (Windows-friendly)
1. Install Android Studio (Koala or newer).
2. Install SDK Platform 34 and Build-Tools 34.x from SDK Manager.
3. Install JDK 17 (Android Studio embedded JDK is fine).
4. Open folder `android-chaquopy` in Android Studio.
5. Let Gradle sync and download dependencies.
6. Build APK:
   - Build -> Build Bundle(s) / APK(s) -> Build APK(s)
7. APK output:
   - `android-chaquopy/app/build/outputs/apk/debug/app-debug.apk`

## CLI build (after Android Studio installs SDK)
From PowerShell:
```powershell
cd c:\Users\LOOSE\vsvoice\android-chaquopy
.\gradlew.bat assembleDebug
```

## Commands to test
- `add todo buy medicine`
- `show todos`
- `open youtube`
- `navigate to nearest hospital`
- `help`