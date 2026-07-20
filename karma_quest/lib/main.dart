import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'screens/login_screen.dart';
import 'screens/onboarding_screen.dart';
import 'screens/home_dashboard.dart';
import 'services/supabase_service.dart';
import 'services/hive_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // 1. Initialize Hive Local Database
  try {
    await HiveService.init();
  } catch (e) {
    debugPrint("Hive initialization skipped/failed: $e");
  }

  // 2. Initialize Supabase 24/7 Live Cloud Database
  try {
    await Supabase.initialize(
      url: 'https://rnunibjmmowhaxsytthf.supabase.co',
      anonKey: 'sb_publishable_jjYnowJojZtzDjqEmVXACg_C7J1PGlq',
    );
  } catch (e) {
    debugPrint("Failed to initialize Supabase client: $e");
  }
  
  // 3. Resolve start screen path
  final prefs = await SharedPreferences.getInstance();
  final hasOnboarded = prefs.getBool('has_completed_onboarding') ?? false;
  final guestMode = prefs.getBool('guest_offline_mode') ?? false;
  
  Widget initialScreen = const LoginScreen();
  
  if (guestMode) {
    initialScreen = hasOnboarded ? const HomeDashboard() : const OnboardingScreen();
  } else if (SupabaseService.currentUser != null) {
    initialScreen = hasOnboarded ? const HomeDashboard() : const OnboardingScreen();
  }

  runApp(KarmaQuestApp(startScreen: initialScreen));
}

class KarmaQuestApp extends StatelessWidget {
  final Widget startScreen;
  const KarmaQuestApp({super.key, required this.startScreen});

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
      home: startScreen,
    );
  }
}
