import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'screens/home_dashboard.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Supabase 24/7 Live Cloud Database
  try {
    await Supabase.initialize(
      url: 'https://rnunibjmmowhaxsytthf.supabase.co',
      anonKey: 'sb_publishable_jjYnowJojZtzDjqEmVXACg_C7J1PGlq',
    );
  } catch (e) {
    debugPrint("Failed to initialize Supabase client: $e");
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
