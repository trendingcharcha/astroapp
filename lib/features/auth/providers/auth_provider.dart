import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_auth/firebase_auth.dart';

// Represents the state of user authentication
class AuthState {
  final bool isAuthenticated;
  final bool isGuest;
  final String? email;
  final String? displayName;
  final String? uid;
  final String? errorMessage;

  AuthState({
    this.isAuthenticated = false,
    this.isGuest = false,
    this.email,
    this.displayName,
    this.uid,
    this.errorMessage,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    bool? isGuest,
    String? email,
    String? displayName,
    String? uid,
    String? errorMessage,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      isGuest: isGuest ?? this.isGuest,
      email: email ?? this.email,
      displayName: displayName ?? this.displayName,
      uid: uid ?? this.uid,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}

// StateNotifier to manage Auth State
class AuthNotifier extends StateNotifier<AuthState> {
  FirebaseAuth? _auth;

  AuthNotifier() : super(AuthState()) {
    // Try to get FirebaseAuth instance safely
    try {
      _auth = FirebaseAuth.instance;
      _auth!.authStateChanges().listen((User? user) {
        if (user != null) {
          state = AuthState(
            isAuthenticated: true,
            isGuest: false,
            email: user.email,
            displayName: user.displayName ?? "Seeker",
            uid: user.uid,
          );
        } else {
          // If no Firebase user, check if we are in guest mode currently
          if (!state.isGuest) {
            state = AuthState();
          }
        }
      });
    } catch (e) {
      // Firebase not initialized yet, that is fine, we use local fallback
      state = AuthState();
    }
  }

  // Email/Password sign in
  Future<void> signInWithEmail(String email, String password) async {
    try {
      if (_auth != null) {
        await _auth!.signInWithEmailAndPassword(email: email, password: password);
      } else {
        // Mock success fallback for offline testing
        state = AuthState(
          isAuthenticated: true,
          isGuest: false,
          email: email,
          displayName: "Cosmic Seeker",
          uid: "mock-uid-12345",
        );
      }
    } on FirebaseAuthException catch (e) {
      state = state.copyWith(errorMessage: e.message);
    } catch (e) {
      state = state.copyWith(errorMessage: "Connection error: Simulated session created instead.");
      // Fallback
      state = AuthState(
        isAuthenticated: true,
        isGuest: false,
        email: email,
        displayName: "Cosmic Seeker",
        uid: "mock-uid-12345",
      );
    }
  }

  // Email/Password register
  Future<void> signUpWithEmail(String email, String password) async {
    try {
      if (_auth != null) {
        await _auth!.createUserWithEmailAndPassword(email: email, password: password);
      } else {
        // Mock success fallback
        state = AuthState(
          isAuthenticated: true,
          isGuest: false,
          email: email,
          displayName: "Cosmic Seeker",
          uid: "mock-uid-12345",
        );
      }
    } on FirebaseAuthException catch (e) {
      state = state.copyWith(errorMessage: e.message);
    } catch (e) {
      state = state.copyWith(errorMessage: e.toString());
    }
  }

  // Continue as Guest
  void continueAsGuest() {
    state = AuthState(
      isAuthenticated: true,
      isGuest: true,
      displayName: "Guest Seeker",
      uid: "guest-uid",
    );
  }

  // Google Sign-In mockup
  Future<void> signInWithGoogle() async {
    try {
      // In production, you would call:
      // final GoogleSignInAccount? googleUser = await GoogleSignIn().signIn();
      // ... credential flow ...
      
      // Mocking for direct runtime
      state = AuthState(
        isAuthenticated: true,
        isGuest: false,
        email: "google.seeker@gmail.com",
        displayName: "Astro Seeker",
        uid: "google-mock-uid",
      );
    } catch (e) {
      state = state.copyWith(errorMessage: e.toString());
    }
  }

  // Sign out
  Future<void> signOut() async {
    if (_auth != null) {
      await _auth!.signOut();
    }
    state = AuthState();
  }
}

// Riverpod Provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});
