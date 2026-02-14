[app]
title = BlindVoiceAssistant
package.name = blindvoiceassistant
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,md
author = You
version = 0.1
requirements = python3,kivy==2.3.0,plyer,pyjnius
orientation = portrait
fullscreen = 0

# Android
android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.permissions = RECORD_AUDIO,INTERNET,ACCESS_NETWORK_STATE

# Keep logs for test builds
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1