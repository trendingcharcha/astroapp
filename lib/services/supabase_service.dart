import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseService {
  static final client = Supabase.instance.client;

  // Get current user session
  static User? get currentUser => client.auth.currentUser;

  // ─── AUTH OPERATIONS ──────────────────────────────────────────────────────

  static Future<AuthResponse> signUp(String email, String password) async {
    return await client.auth.signUp(email: email, password: password);
  }

  static Future<AuthResponse> signIn(String email, String password) async {
    return await client.auth.signInWithPassword(email: email, password: password);
  }

  static Future<AuthResponse> signInAnonymously() async {
    return await client.auth.signInAnonymously();
  }

  static Future<void> signOut() async {
    await client.auth.signOut();
  }

  // ─── PROFILE OPERATIONS ───────────────────────────────────────────────────

  /// Basic profile upsert for initial setup
  static Future<void> upsertProfile({
    required String name,
    required String goal,
    required String profession,
    required int totalXp,
  }) async {
    final user = currentUser;
    if (user == null) return;

    try {
      await client.from('karma_profiles').upsert({
        'id': user.id,
        'name': name,
        'goal': goal,
        'profession': profession,
        'total_xp': totalXp,
        'updated_at': DateTime.now().toIso8601String(),
      });
    } catch (e) {
      // Silently fail on cloud sync — local Hive is source of truth
    }
  }

  /// Full profile upsert including all onboarding data
  static Future<void> upsertFullProfile(Map<String, dynamic> profileData) async {
    final user = currentUser;
    if (user == null) return;

    try {
      await client.from('karma_profiles').upsert({
        'id': user.id,
        ...profileData,
        'updated_at': DateTime.now().toIso8601String(),
      });
    } catch (e) {
      // Silently fail on cloud sync — local Hive is source of truth
    }
  }

  /// Fetch profile from cloud
  static Future<Map<String, dynamic>?> fetchProfile() async {
    final user = currentUser;
    if (user == null) return null;

    try {
      final response = await client
          .from('karma_profiles')
          .select()
          .eq('id', user.id)
          .maybeSingle();
      return response;
    } catch (e) {
      return null;
    }
  }

  /// Update total XP for user
  static Future<void> updateXp(int totalXp) async {
    final user = currentUser;
    if (user == null) return;

    try {
      await client.from('karma_profiles').update({
        'total_xp': totalXp,
        'updated_at': DateTime.now().toIso8601String(),
      }).eq('id', user.id);
    } catch (e) {
      // Silently fail
    }
  }

  // ─── TASK OPERATIONS ──────────────────────────────────────────────────────

  static Future<List<Map<String, dynamic>>> fetchTasks() async {
    final user = currentUser;
    if (user == null) return [];

    try {
      final response = await client
          .from('karma_tasks')
          .select()
          .eq('user_id', user.id)
          .order('created_at', ascending: true);
      return List<Map<String, dynamic>>.from(response);
    } catch (e) {
      return [];
    }
  }

  static Future<void> saveTask({
    String? taskId,
    required String title,
    required String description,
    required int xp,
    required bool isCompleted,
  }) async {
    final user = currentUser;
    if (user == null) return;

    try {
      final taskData = {
        if (taskId != null) 'id': taskId,
        'user_id': user.id,
        'title': title,
        'description': description,
        'xp': xp,
        'is_completed': isCompleted,
      };
      await client.from('karma_tasks').upsert(taskData);
    } catch (e) {
      // Silently fail on cloud sync
    }
  }

  static Future<void> updateTaskCompletion(String taskId, bool isCompleted) async {
    try {
      await client
          .from('karma_tasks')
          .update({'is_completed': isCompleted})
          .eq('id', taskId);
    } catch (e) {
      // Silently fail
    }
  }

  static Future<void> deleteTask(String taskId) async {
    try {
      await client.from('karma_tasks').delete().eq('id', taskId);
    } catch (e) {
      // Silently fail
    }
  }

  /// Batch clear all tasks for user (used when regenerating fresh daily quests)
  static Future<void> clearAllTasks() async {
    final user = currentUser;
    if (user == null) return;

    try {
      await client.from('karma_tasks').delete().eq('user_id', user.id);
    } catch (e) {
      // Silently fail
    }
  }
}
