import 'package:flutter/material.dart';

class CosmicTheme {
  // Color Palette
  static const Color background = Color(0xFF09071A); // Deep cosmic void
  static const Color surface = Color(0xFF14102C);    // Mystic purple cards
  static const Color primaryGold = Color(0xFFE8C879); // Premium warm gold
  static const Color primaryGoldDark = Color(0xFFD4B157);
  static const Color accentPurple = Color(0xFF8E6FD6); // Spiritual violet
  static const Color accentNebula = Color(0xFF4A90E2); // Cosmic blue
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFB3B1C9); // Muted sky grey

  // Material 3 Dark Cosmic Theme Configuration
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: background,
      primaryColor: primaryGold,
      colorScheme: const ColorScheme.dark(
        primary: primaryGold,
        secondary: accentPurple,
        tertiary: accentNebula,
        background: background,
        surface: surface,
        onPrimary: Color(0xFF1E1C0A),
        onSecondary: Colors.white,
        onBackground: textPrimary,
        onSurface: textPrimary,
      ),
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: textPrimary),
        headlineLarge: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: primaryGold),
        headlineMedium: TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: textPrimary),
        titleLarge: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: primaryGold),
        bodyLarge: TextStyle(fontSize: 16, color: textPrimary),
        bodyMedium: TextStyle(fontSize: 14, color: textSecondary),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: background,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: primaryGold),
        iconTheme: IconThemeData(color: primaryGold),
      ),
      cardTheme: CardTheme(
        color: surface,
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: Color(0xFF2A244E), width: 1),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryGold,
          foregroundColor: const Color(0xFF1E1C0A),
          elevation: 6,
          shadowColor: primaryGold.withOpacity(0.4),
          textStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 24),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(30),
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: const Color(0xFF1A1438),
        hintStyle: const TextStyle(color: textSecondary),
        labelStyle: const TextStyle(color: primaryGold),
        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFF2A244E)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFF2A244E)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: primaryGold, width: 1.5),
        ),
      ),
    );
  }

  // Golden Gradient for premium background and banners
  static const LinearGradient cosmicGradient = LinearGradient(
    colors: [background, Color(0xFF1B143E)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  static const LinearGradient goldGradient = LinearGradient(
    colors: [primaryGold, Color(0xFFF9E8A2)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient purpleGradient = LinearGradient(
    colors: [accentPurple, Color(0xFFB59FF3)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
