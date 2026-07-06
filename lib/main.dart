import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'core/theme/cosmic_theme.dart';
import 'features/onboarding/screens/splash_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Safe initialization of Firebase backend.
  // Will log warning instead of crashing if project credentials aren't linked yet.
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
