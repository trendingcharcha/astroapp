# 📱 CosmoVedic — Google Play Store APK & AAB Build Guide

This repository contains the **complete source code**, **Flutter App Wrapper (`lib/main.dart`)**, and **PWA Web Engine (`index.html`)** ready to be compiled into an Android `.apk` (for phone testing) and `.aab` (for Google Play Store upload).

---

## 🚀 Method 1: Instant 1-Click APK Generator (PWABuilder / Web2App)
If you want to generate the `.apk` and `.aab` in 60 seconds without installing Android Studio:

1. Go to **[PWABuilder.com](https://www.pwabuilder.com/)** or **[Web2App](https://web2app.com/)**.
2. Enter your live app URL: `https://trendingcharcha.github.io/astroapp/`
3. Click **Package for Store** $ightarrow$ Select **Android**.
4. Set Package ID: `com.cosmovedic.astroapp`
5. Click **Download APK** (for instant phone testing) and **Download AAB** (for Google Play Store upload).

---

## 🛠️ Method 2: Build APK via Flutter CLI (Command Line)
If you have Flutter installed on your PC:

1. Open Terminal in this folder: `c:\Users\EARTH\OneDrive\Desktop\Antigravity 2026\Astro AI app`
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Build the testing APK for your phone:
   ```bash
   flutter build apk --release
   ```
   *Output file*: `build/app/outputs/flutter-apk/app-release.apk`

4. Build the Android App Bundle (`.aab`) for Google Play Store upload:
   ```bash
   flutter build appbundle --release
   ```
   *Output file*: `build/app/outputs/bundle/release/app-release.aab`

---

## 📲 Installing `.apk` on your Phone
1. Transfer `app-release.apk` to your phone via USB or WhatsApp/Drive.
2. Tap the APK on your phone $ightarrow$ Allow "Install from Unknown Sources".
3. CosmoVedic will install as a native Android App with local push notifications!
