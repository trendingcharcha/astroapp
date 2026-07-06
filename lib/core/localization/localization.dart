import 'package:flutter_riverpod/flutter_riverpod.dart';

// Locale State Provider: default is English ('en')
final localeProvider = StateProvider<String>((ref) => 'en');

class CosmoLocalization {
  static const Map<String, Map<String, String>> _localizedValues = {
    'en': {
      'app_name': 'CosmoVedic',
      'tagline': 'Your Cosmic Vedic Companion',
      'login': 'Login to Begin',
      'email': 'Email Address',
      'password': 'Password',
      'sign_in': 'Sign In',
      'sign_in_google': 'Sign in with Google',
      'guest_mode': 'Continue as Guest',
      'home': 'Home',
      'kundli': 'Kundli',
      'matching': 'Matching',
      'panchang': 'Panchang',
      'tarot': 'Tarot Reading',
      'numerology': 'Numerology',
      'settings': 'Settings',
      'daily_horoscope': 'Daily Horoscope',
      'current_panchang': 'Current Panchang',
      'quick_tools': 'Quick Astro Tools',
      'generate_kundli': 'Generate Birth Chart',
      'saved_charts': 'Saved Charts',
      'language': 'Language',
      'notification': 'Notifications',
      'about': 'About CosmoVedic',
      'enter_birth_details': 'Enter Birth Details',
      'name': 'Name',
      'birth_date': 'Birth Date',
      'birth_time': 'Birth Time',
      'birth_place': 'Birth Place',
      'calculate': 'Calculate Chart',
      'horoscope_weekly': 'Weekly',
      'horoscope_monthly': 'Monthly',
      'aries': 'Aries', 'taurus': 'Taurus', 'gemini': 'Gemini',
      'cancer': 'Cancer', 'leo': 'Leo', 'virgo': 'Virgo',
      'libra': 'Libra', 'scorpio': 'Scorpio', 'sagittarius': 'Sagittarius',
      'capricorn': 'Capricorn', 'aquarius': 'Aquarius', 'pisces': 'Pisces',
    },
    'hi': {
      'app_name': 'कोस्मोवैदिक',
      'tagline': 'आपका वैदिक ज्योतिष साथी',
      'login': 'शुरू करने के लिए लॉगिन करें',
      'email': 'ईमेल पता',
      'password': 'पासवर्ड',
      'sign_in': 'साइन इन करें',
      'sign_in_google': 'गूगल से लॉगिन करें',
      'guest_mode': 'अतिथि के रूप में जारी रखें',
      'home': 'मुख्य पृष्ठ',
      'kundli': 'कुंडली',
      'matching': 'गुण मिलान',
      'panchang': 'पंचांग',
      'tarot': 'टैरो रीडिंग',
      'numerology': 'अंकशास्त्र',
      'settings': 'सेटिंग्स',
      'daily_horoscope': 'दैनिक राशिफल',
      'current_panchang': 'आज का पंचांग',
      'quick_tools': 'त्वरित ज्योतिष टूल्स',
      'generate_kundli': 'कुंडली बनाएं',
      'saved_charts': 'सहेजी गई कुंडली',
      'language': 'भाषा',
      'notification': 'सूचनाएं',
      'about': 'कोस्मोवैदिक के बारे में',
      'enter_birth_details': 'जन्म विवरण दर्ज करें',
      'name': 'नाम',
      'birth_date': 'जन्म तिथि',
      'birth_time': 'जन्म समय',
      'birth_place': 'जन्म स्थान',
      'calculate': 'गणना करें',
      'horoscope_weekly': 'साप्ताहिक',
      'horoscope_monthly': 'मासिक',
      'aries': 'मेष', 'taurus': 'वृषभ', 'gemini': 'मिथुन',
      'cancer': 'कर्क', 'leo': 'सिंह', 'virgo': 'कन्या',
      'libra': 'तुला', 'scorpio': 'वृश्चिक', 'sagittarius': 'धनु',
      'capricorn': 'मकर', 'aquarius': 'कुंभ', 'pisces': 'मीन',
    }
  };

  final String lang;
  CosmoLocalization(this.lang);

  static CosmoLocalization of(WidgetRef ref) {
    final currentLang = ref.watch(localeProvider);
    return CosmoLocalization(currentLang);
  }

  String translate(String key) {
    return _localizedValues[lang]?[key] ?? key;
  }
}
