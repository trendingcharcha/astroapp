import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/auth_provider.dart';
import '../../home/screens/home_screen.dart';
import '../../../core/theme/cosmic_theme.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isSignUp = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _submit() async {
    if (!_formKey.currentState!.validate()) return;
    
    final authNotifier = ref.read(authProvider.notifier);
    if (_isSignUp) {
      await authNotifier.signUpWithEmail(_emailController.text, _passwordController.text);
    } else {
      await authNotifier.signInWithEmail(_emailController.text, _passwordController.text);
    }

    // Check if successfully authenticated
    final authState = ref.read(authProvider);
    if (authState.isAuthenticated) {
      _navigateToHome();
    } else if (authState.errorMessage != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(authState.errorMessage!), backgroundColor: CosmicTheme.accentPurple),
      );
    }
  }

  void _navigateToHome() {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const HomeScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    ref.listen<AuthState>(authProvider, (previous, next) {
      if (next.isAuthenticated) {
        _navigateToHome();
      }
    });

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: CosmicTheme.cosmicGradient,
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 30),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const SizedBox(height: 30),
                  // Sun/Astral Icon logo
                  const Center(
                    child: Icon(
                      Icons.nights_stay,
                      size: 60,
                      color: CosmicTheme.primaryGold,
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Text(
                    "COSMOVEDIC",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: CosmicTheme.primaryGold,
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 4,
                    ),
                  ),
                  const SizedBox(height: 40),
                  Text(
                    _isSignUp ? "Create Cosmic Account" : "Access Cosmic Wisdom",
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
                  ),
                  const SizedBox(height: 20),

                  // Email Field
                  TextFormField(
                    controller: _emailController,
                    keyboardType: TextInputType.emailAddress,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      labelText: "Email Address",
                      prefixIcon: Icon(Icons.email_outlined, color: CosmicTheme.primaryGold),
                    ),
                    validator: (val) => val == null || !val.contains("@") ? "Enter a valid email" : null,
                  ),
                  const SizedBox(height: 16),

                  // Password Field
                  TextFormField(
                    controller: _passwordController,
                    obscureText: true,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      labelText: "Password",
                      prefixIcon: Icon(Icons.lock_outline, color: CosmicTheme.primaryGold),
                    ),
                    validator: (val) => val == null || val.length < 6 ? "Password must be 6+ chars" : null,
                  ),
                  const SizedBox(height: 24),

                  // Sign In Button
                  ElevatedButton(
                    onPressed: _submit,
                    child: Text(_isSignUp ? "CREATE ACCOUNT" : "SIGN IN"),
                  ),
                  const SizedBox(height: 16),

                  // Switch between Sign In / Sign Up
                  TextButton(
                    onPressed: () {
                      setState(() {
                        _isSignUp = !_isSignUp;
                      });
                    },
                    child: Text(
                      _isSignUp ? "Already have an account? Sign In" : "New to CosmoVedic? Sign Up",
                      style: const TextStyle(color: CosmicTheme.primaryGold),
                    ),
                  ),

                  const SizedBox(height: 20),
                  Row(
                    children: [
                      Expanded(child: Divider(color: CosmicTheme.textSecondary.withOpacity(0.3))),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 10),
                        child: Text("OR", style: TextStyle(color: Colors.white54, fontSize: 12)),
                      ),
                      Expanded(child: Divider(color: CosmicTheme.textSecondary.withOpacity(0.3))),
                    ],
                  ),
                  const SizedBox(height: 20),

                  // Google Sign-In Button
                  OutlinedButton.icon(
                    onPressed: () async {
                      await ref.read(authProvider.notifier).signInWithGoogle();
                    },
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      side: const BorderSide(color: CosmicTheme.primaryGold),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                    ),
                    icon: const Icon(Icons.g_mobiledata, color: CosmicTheme.primaryGold, size: 28),
                    label: const Text(
                      "Sign in with Google",
                      style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Guest Mode Button
                  TextButton(
                    onPressed: () {
                      ref.read(authProvider.notifier).continueAsGuest();
                      _navigateToHome();
                    },
                    child: const Text(
                      "Explore as Guest (Offline)",
                      style: TextStyle(color: CosmicTheme.textSecondary, decoration: TextDecoration.underline),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
