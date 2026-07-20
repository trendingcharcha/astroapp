import 'package:flutter/material.dart';
import '../services/supabase_service.dart';
import 'onboarding_screen.dart';
import 'home_dashboard.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;
  bool _isSignUp = false;
  String? _errorMessage;

  Future<void> _handleSubmit() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      setState(() {
        _isLoading = false;
        _errorMessage = "Please enter both email and password.";
      });
      return;
    }

    try {
      if (_isSignUp) {
        await SupabaseService.signUp(email, password);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Account created! Please sign in.")),
        );
        setState(() => _isSignUp = false);
      } else {
        await SupabaseService.signIn(email, password);
        _navigateNext();
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll("Exception: ", "");
      });
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _handleGuestLogin() async {
    setState(() => _isLoading = true);
    try {
      await SupabaseService.client.auth.signInAnonymously();
      _navigateNext();
    } catch (e) {
      // Offline / network failure fallback
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool('guest_offline_mode', true);
      _navigateNext();
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _navigateNext() async {
    final prefs = await SharedPreferences.getInstance();
    final hasOnboarded = prefs.getBool('has_completed_onboarding') ?? false;

    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => hasOnboarded 
              ? const HomeDashboard() 
              : const OnboardingScreen(),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF09071A),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Cosmic Logo/Header
              const Icon(Icons.stars, color: Color(0xFFE8C879), size: 80),
              const SizedBox(height: 16),
              const Text(
                'KARMA QUEST',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Color(0xFFE8C879),
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2,
                ),
              ),
              const Text(
                'Vedic Tasks & Spiritual Sync',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Color(0xFF8E6FD6),
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: 48),

              // Form Card
              Card(
                color: const Color(0xFF14102C),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                  side: const BorderSide(color: Color(0xFF2A244E), width: 1),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text(
                        _isSignUp ? 'Create Cosmic Account' : 'Sign In to Your Stars',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 20),

                      // Email input
                      TextField(
                        controller: _emailController,
                        keyboardType: TextInputType.emailAddress,
                        style: const TextStyle(color: Colors.white),
                        decoration: InputDecoration(
                          labelText: 'Email Address',
                          labelStyle: const TextStyle(color: Colors.grey),
                          prefixIcon: const Icon(Icons.email_outlined, color: Color(0xFF8E6FD6)),
                          enabledBorder: OutlineInputBorder(
                            borderSide: const BorderSide(color: Color(0xFF2A244E)),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderSide: const BorderSide(color: Color(0xFF8E6FD6)),
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),

                      // Password input
                      TextField(
                        controller: _passwordController,
                        obscureText: true,
                        style: const TextStyle(color: Colors.white),
                        decoration: InputDecoration(
                          labelText: 'Password',
                          labelStyle: const TextStyle(color: Colors.grey),
                          prefixIcon: const Icon(Icons.lock_outline, color: Color(0xFF8E6FD6)),
                          enabledBorder: OutlineInputBorder(
                            borderSide: const BorderSide(color: Color(0xFF2A244E)),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderSide: const BorderSide(color: Color(0xFF8E6FD6)),
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),

                      if (_errorMessage != null)
                        Text(
                          _errorMessage!,
                          style: const TextStyle(color: Colors.redAccent, fontSize: 13),
                        ),

                      const SizedBox(height: 20),

                      // Submit Button
                      ElevatedButton(
                        onPressed: _isLoading ? null : _handleSubmit,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF8E6FD6),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                        child: _isLoading
                            ? const CircularProgressIndicator(color: Colors.white)
                            : Text(_isSignUp ? 'SIGN UP' : 'SIGN IN'),
                      ),
                      const SizedBox(height: 16),

                      // Mode Switch Text
                      TextButton(
                        onPressed: () {
                          setState(() {
                            _isSignUp = !_isSignUp;
                            _errorMessage = null;
                          });
                        },
                        child: Text(
                          _isSignUp
                              ? 'Already have an account? Sign In'
                              : 'New to KarmaQuest? Create Account',
                          style: const TextStyle(color: Color(0xFFE8C879)),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 24),

              // Guest Mode / Skip login button
              OutlinedButton.icon(
                onPressed: _isLoading ? null : _handleGuestLogin,
                icon: const Icon(Icons.arrow_forward, color: Color(0xFFE8C879)),
                label: const Text(
                  'CONTINUE AS GUEST',
                  style: TextStyle(color: Color(0xFFE8C879), fontWeight: FontWeight.bold),
                ),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: Color(0xFFE8C879), width: 1.5),
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
