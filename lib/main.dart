import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:url_launcher/url_launcher.dart';

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

  // ─────────────────────────────────────────────────────────────
  // Notification channel details (shared across all 4 types)
  // ─────────────────────────────────────────────────────────────
  static const AndroidNotificationDetails _androidDetails =
      AndroidNotificationDetails(
    'cosmovedic_daily_channel',
    'CosmoVedic Daily Reminders',
    channelDescription:
        'Daily Astrology Tasks, Fast Alerts & Rahu Kaal Warnings',
    importance: Importance.max,
    priority: Priority.high,
    color: Color(0xFFE8C879),
  );
  static const NotificationDetails _notifDetails = NotificationDetails(
    android: _androidDetails,
    iOS: DarwinNotificationDetails(),
  );

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
            setState(() => _isLoading = true);
          },
          onPageFinished: (String url) {
            setState(() => _isLoading = false);
          },
          onWebResourceError: (WebResourceError error) {
            debugPrint('WebView Error: ${error.description}');
          },
          // ── FIX 2: Intercept Google OAuth URLs ─────────────────
          // Google blocks OAuth inside Android WebView. Open in
          // Chrome Custom Tab (external browser) instead.
          onNavigationRequest: (NavigationRequest request) {
            final uri = request.url;
            if (uri.contains('accounts.google.com') ||
                uri.contains('/auth/v1/authorize') ||
                uri.contains('supabase.co/auth')) {
              launchUrl(
                Uri.parse(uri),
                mode: LaunchMode.externalApplication,
              );
              return NavigationDecision.prevent;
            }
            return NavigationDecision.navigate;
          },
        ),
      )
      ..addJavaScriptChannel(
        'FlutterNotificationBridge',
        onMessageReceived: (JavaScriptMessage message) {
          _handleNotificationMessage(message.message);
        },
      )
      ..loadRequest(
          Uri.parse('https://trendingcharcha.github.io/astroapp/'));
  }

  Future<void> _requestPermissions() async {
    await [
      Permission.notification,
      Permission.location,
      Permission.microphone,
    ].request();
  }

  // ─────────────────────────────────────────────────────────────
  // FIX 5: Handle ALL 4 notification payload types from JS bridge
  // ─────────────────────────────────────────────────────────────
  void _handleNotificationMessage(String jsonStr) async {
    try {
      final Map<String, dynamic> data = jsonDecode(jsonStr);
      debugPrint('Received Notification Bridge Payload: $data');

      // 1. Fast Prep Alert (1-day prior to upcoming fast)
      if (data.containsKey('fastPrep')) {
        final fast = data['fastPrep'];
        await flutterLocalNotificationsPlugin.show(
          1,
          fast['title'] ?? '🍎 1-Day Prior Fast Prep',
          fast['body'] ??
              'Tomorrow is a sacred fast day. Prepare your sattvic items today.',
          _notifDetails,
          payload: 'fastPrep',
        );
      }

      // 2. Morning Daily Task Summary (07:00 AM)
      if (data.containsKey('morning')) {
        final morning = data['morning'];
        await flutterLocalNotificationsPlugin.show(
          2,
          morning['title'] ?? '🌅 Your CosmoVedic Daily Plan is Ready',
          morning['body'] ??
              'Open the app to see today\'s personalized Vedic tasks and remedies.',
          _notifDetails,
          payload: 'morning',
        );
      }

      // 3. Rahu Kaal 15-Minute Warning
      if (data.containsKey('rahuKaal')) {
        final rahu = data['rahuKaal'];
        await flutterLocalNotificationsPlugin.show(
          3,
          rahu['title'] ?? '⚠️ Rahu Kaal Starts in 15 Minutes',
          rahu['body'] ??
              'Avoid new work and important decisions during Rahu Kaal period.',
          _notifDetails,
          payload: 'rahuKaal',
        );
      }

      // 4. Streak Saver Night Reminder (08:30 PM)
      if (data.containsKey('streakSaver')) {
        final streak = data['streakSaver'];
        await flutterLocalNotificationsPlugin.show(
          4,
          streak['title'] ?? '🔥 Don\'t Break Your Streak!',
          streak['body'] ??
              'Complete today\'s Karma tasks before midnight to keep your streak alive.',
          _notifDetails,
          payload: 'streakSaver',
        );
      }
    } catch (e) {
      debugPrint('Error parsing notification bridge payload: $e');
    }
  }

  // ─────────────────────────────────────────────────────────────
  // FIX 1: Replace deprecated WillPopScope with PopScope
  // Correct back-button behaviour: navigate WebView history first,
  // only exit the app when there is no more history to go back to.
  // ─────────────────────────────────────────────────────────────
  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvoked: (bool didPop) async {
        if (didPop) return;
        if (await _controller.canGoBack()) {
          _controller.goBack();
        } else {
          // No WebView history left — allow the OS to close the app
          if (context.mounted) {
            SystemNavigator.pop();
          }
        }
      },
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
                          valueColor: AlwaysStoppedAnimation<Color>(
                              Color(0xFFE8C879)),
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
