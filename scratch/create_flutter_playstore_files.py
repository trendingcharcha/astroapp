import os

# Create directory structure
os.makedirs('lib', exist_ok=True)
os.makedirs('android/app/src/main/kotlin/com/cosmovedic/astroapp', exist_ok=True)
os.makedirs('android/app/src/main/res/mipmap-hdpi', exist_ok=True)

# 1. lib/main.dart (Production Flutter WebView + Local Notification Bridge)
main_dart_content = '''import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:permission_handler/permission_handler.dart';

final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
    FlutterLocalNotificationsPlugin();

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);

  // Initialize Native Local Notifications
  const AndroidInitializationSettings initializationSettingsAndroid =
      AndroidInitializationSettings('@mipmap/ic_launcher');
  const DarwinInitializationSettings initializationSettingsIOS =
      DarwinInitializationSettings();
  const InitializationSettings initializationSettings = InitializationSettings(
    android: initializationSettingsAndroid,
    iOS: initializationSettingsIOS,
  );

  await flutterLocalNotificationsPlugin.initialize(
    initializationSettings,
    onDidReceiveNotificationResponse: (NotificationResponse details) {
      debugPrint('Notification clicked: ${details.payload}');
    },
  );

  runApp(const CosmoVedicApp());
}

class CosmoVedicApp extends StatelessWidget {
  const CosmoVedicApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CosmoVedic',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0C0922),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE8C879),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const CosmoVedicMainScreen(),
    );
  }
}

class CosmoVedicMainScreen extends StatefulWidget {
  const CosmoVedicMainScreen({super.key});

  @override
  State<CosmoVedicMainScreen> createState() => _CosmoVedicMainScreenState();
}

class _CosmoVedicMainScreenState extends State<CosmoVedicMainScreen> {
  late final WebViewController _controller;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _requestPermissions();

    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0xFF0C0922))
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (String url) {
            setState(() {
              _isLoading = true;
            });
          },
          onPageFinished: (String url) {
            setState(() {
              _isLoading = false;
            });
          },
          onWebResourceError: (WebResourceError error) {
            debugPrint('WebView Error: ${error.description}');
          },
        ),
      )
      ..addJavaScriptChannel(
        'FlutterNotificationBridge',
        onMessageReceived: (JavaScriptMessage message) {
          _handleNotificationMessage(message.message);
        },
      )
      ..loadRequest(Uri.parse('https://trendingcharcha.github.io/astroapp/'));
  }

  Future<void> _requestPermissions() async {
    await [
      Permission.notification,
      Permission.location,
      Permission.microphone,
    ].request();
  }

  void _handleNotificationMessage(String jsonStr) async {
    try {
      final Map<String, dynamic> data = jsonDecode(jsonStr);
      debugPrint('Received Notification Bridge Payload: $data');

      // Schedule local notification in Android / iOS native engine
      const AndroidNotificationDetails androidDetails = AndroidNotificationDetails(
        'cosmovedic_daily_channel',
        'CosmoVedic Daily Reminders',
        channelDescription: 'Daily Astrology Tasks, Fast Alerts & Rahu Kaal Warnings',
        importance: Importance.max,
        priority: Priority.high,
        color: Color(0xFFE8C879),
      );
      const NotificationDetails notifDetails = NotificationDetails(
        android: androidDetails,
        iOS: DarwinNotificationDetails(),
      );

      if (data.containsKey('fastPrep')) {
        final fast = data['fastPrep'];
        await flutterLocalNotificationsPlugin.show(
          1,
          fast['title'] ?? '🍎 1-Day Prior Fast Prep',
          fast['body'] ?? 'Tomorrow is sacred fast day! Prepare your sattvic items today.',
          notifDetails,
        );
      }
    } catch (e) {
      debugPrint('Error parsing notification bridge payload: $e');
    }
  }

  Future<bool> _onWillPop() async {
    if (await _controller.canGoBack()) {
      _controller.goBack();
      return false;
    }
    return true;
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: _onWillPop,
      child: Scaffold(
        body: SafeArea(
          child: Stack(
            children: [
              WebViewWidget(controller: _controller),
              if (_isLoading)
                Container(
                  color: const Color(0xFF0C0922),
                  child: const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CircularProgressIndicator(
                          valueColor: AlwaysStoppedAnimation<Color>(Color(0xFFE8C879)),
                        ),
                        SizedBox(height: 16),
                        Text(
                          'COSMOVEDIC',
                          style: TextStyle(
                            color: Color(0xFFE8C879),
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 2,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
'''

with open('lib/main.dart', 'w', encoding='utf-8') as f:
    f.write(main_dart_content)
print("SUCCESS: Written lib/main.dart")

# 2. pubspec.yaml (Flutter Package Manifest)
pubspec_content = '''name: astroapp
description: CosmoVedic - Premium Vedic Astrology & KarmaQuest App
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  webview_flutter: ^4.7.0
  flutter_local_notifications: ^17.1.0
  permission_handler: ^11.3.1
  timezone: ^0.9.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  assets:
    - manifest.json
'''

with open('pubspec.yaml', 'w', encoding='utf-8') as f:
    f.write(pubspec_content)
print("SUCCESS: Written pubspec.yaml")

# 3. AndroidManifest.xml (Permissions & Play Store Config)
manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.cosmovedic.astroapp">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />
    <uses-permission android:name="android.permission.VIBRATE" />

    <application
        android:label="CosmoVedic"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="true">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            
            <meta-data
              android:name="io.flutter.embedding.android.NormalTheme"
              android:resource="@style/NormalTheme"
              />
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        
        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
'''

with open('android/app/src/main/AndroidManifest.xml', 'w', encoding='utf-8') as f:
    f.write(manifest_content)
print("SUCCESS: Written AndroidManifest.xml")

# 4. playstore_build_guide.md (Complete Step-by-Step Play Store APK Build Guide)
guide_content = '''# 📱 CosmoVedic — Google Play Store APK & AAB Build Guide

This repository contains the **complete source code**, **Flutter App Wrapper (`lib/main.dart`)**, and **PWA Web Engine (`index.html`)** ready to be compiled into an Android `.apk` (for phone testing) and `.aab` (for Google Play Store upload).

---

## 🚀 Method 1: Instant 1-Click APK Generator (PWABuilder / Web2App)
If you want to generate the `.apk` and `.aab` in 60 seconds without installing Android Studio:

1. Go to **[PWABuilder.com](https://www.pwabuilder.com/)** or **[Web2App](https://web2app.com/)**.
2. Enter your live app URL: `https://trendingcharcha.github.io/astroapp/`
3. Click **Package for Store** $\rightarrow$ Select **Android**.
4. Set Package ID: `com.cosmovedic.astroapp`
5. Click **Download APK** (for instant phone testing) and **Download AAB** (for Google Play Store upload).

---

## 🛠️ Method 2: Build APK via Flutter CLI (Command Line)
If you have Flutter installed on your PC:

1. Open Terminal in this folder: `c:\\Users\\EARTH\\OneDrive\\Desktop\\Antigravity 2026\\Astro AI app`
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
2. Tap the APK on your phone $\rightarrow$ Allow "Install from Unknown Sources".
3. CosmoVedic will install as a native Android App with local push notifications!
'''

with open('playstore_build_guide.md', 'w', encoding='utf-8') as f:
    f.write(guide_content)
print("SUCCESS: Written playstore_build_guide.md")
