import 'dart:convert';
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
