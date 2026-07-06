import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'firebase_options.dart';
import 'core/theme/cosmic_theme.dart';
import 'features/onboarding/screens/splash_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Safe initialization of Supabase backend.
  try {
    await Supabase.initialize(
      url: 'https://rnunibjmmowhaxsytthf.supabase.co',
      anonKey: 'sb_publishable_jjYnowJojZtzDjqEmVXACg_C7J1PGlq',
    );
  } catch (e) {
    debugPrint("Supabase initialization warning: $e");
  }

  // Safe initialization of Firebase backend.
  try {
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
  } catch (e) {
    debugPrint("Firebase initialization warning (running in offline/fallback mode): $e");
  }

  runApp(
    const ProviderScope(
      child: CosmoVedicApp(),
    ),
  );
}

class CosmoVedicApp extends StatelessWidget {
  const CosmoVedicApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CosmoVedic',
      debugShowCheckedModeBanner: false,
      theme: CosmicTheme.darkTheme,
      home: const SplashScreen(),
    );
  }
}
