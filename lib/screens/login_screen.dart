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

  // ─── Email / Password Auth ─────────────────────────────────────────────────
  Future<void> _handleSubmit() async {
    setState(() { _isLoading = true; _errorMessage = null; });

    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      setState(() { _isLoading = false; _errorMessage = "Please enter both email and password."; });
      return;
    }
    if (password.length < 6) {
      setState(() { _isLoading = false; _errorMessage = "Password must be at least 6 characters."; });
      return;
    }

    try {
      if (_isSignUp) {
        await SupabaseService.signUp(email, password);
        // Sign-up complete → Go to Onboarding to collect birth details & goal
        if (mounted) {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => const OnboardingScreen()),
          );
        }
      } else {
        await SupabaseService.signIn(email, password);
        await _navigateNext();
      }
    } catch (e) {
      setState(() { _errorMessage = e.toString().replaceAll("Exception: ", ""); });
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  // ─── Google OAuth ──────────────────────────────────────────────────────────
  Future<void> _handleGoogleSignIn() async {
    setState(() { _isLoading = true; _errorMessage = null; });
    try {
      await SupabaseService.signInWithGoogle();
      // Google OAuth will redirect — session handled via onAuthStateChange listener
      // For in-app webview or deeplink callback, navigate after auth completes
      await Future.delayed(const Duration(seconds: 2));
      await _navigateNext();
    } catch (e) {
      setState(() { _errorMessage = "Google Sign-In failed. Please try again."; });
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  // ─── Guest Mode ────────────────────────────────────────────────────────────
  Future<void> _handleGuestLogin() async {
    setState(() => _isLoading = true);
    try {
      await SupabaseService.client.auth.signInAnonymously();
      await _navigateNext();
    } catch (e) {
      // Offline guest fallback
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool('guest_offline_mode', true);
      await _navigateNext();
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  // ─── Routing Logic ─────────────────────────────────────────────────────────
  Future<void> _navigateNext() async {
    // Verify backend session is valid (catches deleted users)
    final user = SupabaseService.currentUser;
    if (user == null) {
      setState(() { _errorMessage = "Session invalid. Please sign in again."; });
      return;
    }

    final prefs = await SharedPreferences.getInstance();
    // Clear manual logout flag — user has successfully signed in again
    await prefs.setBool('has_manually_logged_out', false);
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

  // ─── Build ─────────────────────────────────────────────────────────────────
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
              // ── Logo / Header ──────────────────────────────────────────────
              Container(
                width: 80,
                height: 80,
                margin: const EdgeInsets.only(bottom: 12),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: const Color(0xFFE8C879), width: 2),
                ),
                child: const Icon(Icons.brightness_3, color: Color(0xFFE8C879), size: 44),
              ),
              const Text(
                'COSMOVEDIC',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Color(0xFFE8C879),
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 3,
                ),
              ),
              const Text(
                'Align with the Cosmos',
                textAlign: TextAlign.center,
                style: TextStyle(color: Color(0xFF8E6FD6), fontSize: 13, fontWeight: FontWeight.w400),
              ),
              const SizedBox(height: 36),

              // ── Google Sign In / Sign Up Button ────────────────────────────
              ElevatedButton.icon(
                onPressed: _isLoading ? null : _handleGoogleSignIn,
                icon: const Icon(Icons.g_mobiledata_rounded, size: 24),
                label: const Text('Sign In / Sign Up with Google', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                  foregroundColor: const Color(0xFF333333),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  elevation: 4,
                ),
              ),
              const SizedBox(height: 16),

              // ── Divider ────────────────────────────────────────────────────
              Row(
                children: const [
                  Expanded(child: Divider(color: Color(0xFF2A244E))),
                  Padding(
                    padding: EdgeInsets.symmetric(horizontal: 12),
                    child: Text('OR EMAIL', style: TextStyle(color: Color(0xFF8E6FD6), fontSize: 11)),
                  ),
                  Expanded(child: Divider(color: Color(0xFF2A244E))),
                ],
              ),
              const SizedBox(height: 16),

              // ── Auth Form Card ─────────────────────────────────────────────
              Card(
                color: const Color(0xFF14102C),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                  side: const BorderSide(color: Color(0xFF2A244E), width: 1),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text(
                        _isSignUp ? 'Create Your Account' : 'Welcome Back',
                        style: const TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 16),

                      // Email
                      TextField(
                        controller: _emailController,
                        keyboardType: TextInputType.emailAddress,
                        style: const TextStyle(color: Colors.white),
                        decoration: _inputDecoration('Email Address', Icons.email_outlined),
                      ),
                      const SizedBox(height: 12),

                      // Password
                      TextField(
                        controller: _passwordController,
                        obscureText: true,
                        style: const TextStyle(color: Colors.white),
                        decoration: _inputDecoration('Password (min 6 chars)', Icons.lock_outline),
                      ),

                      if (_errorMessage != null) ...[
                        const SizedBox(height: 10),
                        Text(_errorMessage!, style: const TextStyle(color: Colors.redAccent, fontSize: 12)),
                      ],

                      const SizedBox(height: 16),

                      // Submit Button
                      ElevatedButton(
                        onPressed: _isLoading ? null : _handleSubmit,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF8E6FD6),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        child: _isLoading
                            ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                            : Text(_isSignUp ? 'SIGN UP' : 'SIGN IN', style: const TextStyle(fontWeight: FontWeight.bold)),
                      ),
                      const SizedBox(height: 8),

                      // Toggle Mode
                      TextButton(
                        onPressed: () => setState(() { _isSignUp = !_isSignUp; _errorMessage = null; }),
                        child: Text(
                          _isSignUp ? 'Already have an account? Sign In' : "New here? Create Account",
                          style: const TextStyle(color: Color(0xFFE8C879), fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // ── Guest Mode Button ──────────────────────────────────────────
              OutlinedButton.icon(
                onPressed: _isLoading ? null : _handleGuestLogin,
                icon: const Icon(Icons.preview, color: Color(0xFFE8C879)),
                label: const Text('Free Guest Kundli Preview', style: TextStyle(color: Color(0xFFE8C879))),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: Color(0xFFE8C879), width: 1.5),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  InputDecoration _inputDecoration(String label, IconData icon) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Colors.grey),
      prefixIcon: Icon(icon, color: const Color(0xFF8E6FD6)),
      enabledBorder: OutlineInputBorder(borderSide: const BorderSide(color: Color(0xFF2A244E)), borderRadius: BorderRadius.circular(12)),
      focusedBorder: OutlineInputBorder(borderSide: const BorderSide(color: Color(0xFF8E6FD6)), borderRadius: BorderRadius.circular(12)),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
