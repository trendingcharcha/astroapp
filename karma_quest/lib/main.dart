import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'screens/home_dashboard.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Basic Firebase setup code (wrapped in try-catch to run locally without setup)
  try {
    await Firebase.initializeApp();
  } catch (e) {
    debugPrint("Firebase not configured yet: $e");
  }
  
  runApp(const KarmaQuestApp());
}

class KarmaQuestApp extends StatelessWidget {
  const KarmaQuestApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'KarmaQuest',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: const Color(0xFF8E6FD6),
        scaffoldBackgroundColor: const Color(0xFF09071A),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF8E6FD6),
          secondary: Color(0xFFE8C879),
          surface: Color(0xFF14102C),
        ),
        useMaterial3: true,
      ),
      home: const HomeDashboard(),
    );
  }
}
