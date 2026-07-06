import 'dart:async';
import 'package:flutter/material.dart';
import '../../auth/screens/login_screen.dart';
import '../../../core/theme/cosmic_theme.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({Key? key}) : super(key: key);

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _rotateAnimation;

  @override
  void initState() {
    super.initState();
    
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2000),
    );

    _scaleAnimation = Tween<double>(begin: 0.5, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutBack),
    );

    _rotateAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOutSine),
    );

    _controller.forward();

    // Direct transition after animation completes
    Timer(const Duration(milliseconds: 3000), () {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const LoginScreen()),
      );
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: CosmicTheme.cosmicGradient,
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ScaleTransition(
                scale: _scaleAnimation,
                child: RotationTransition(
                  turns: _rotateAnimation,
                  child: Container(
                    width: 140,
                    height: 140,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: CosmicTheme.primaryGold, width: 2),
                      boxShadow: [
                        BoxShadow(
                          color: CosmicTheme.primaryGold.withOpacity(0.3),
                          blurRadius: 40,
                          spreadRadius: 5,
                        ),
                      ],
                    ),
                    child: const Center(
                      child: Icon(
                        Icons.brightness_7, // Astrological Sun Symbol
                        size: 80,
                        color: CosmicTheme.primaryGold,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 40),
              // App Name
              const Text(
                "COSMOVEDIC",
                style: TextStyle(
                  color: CosmicTheme.primaryGold,
                  fontSize: 34,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 6,
                  shadows: [
                    Shadow(
                      color: CosmicTheme.accentPurple,
                      blurRadius: 10,
                      offset: Offset(0, 4),
                    )
                  ],
                ),
              ),
              const SizedBox(height: 10),
              // Subtitle
              Text(
                "Align with the Cosmos",
                style: TextStyle(
                  color: CosmicTheme.textSecondary.withOpacity(0.8),
                  fontSize: 14,
                  letterSpacing: 2,
                  fontStyle: FontStyle.italic,
                ),
              ),
              const SizedBox(height: 100),
              const SizedBox(
                width: 100,
                child: LinearProgressIndicator(
                  backgroundColor: Color(0xFF14102C),
                  color: CosmicTheme.primaryGold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
