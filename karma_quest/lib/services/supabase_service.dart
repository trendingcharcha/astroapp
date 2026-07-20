import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseService {
  static final client = Supabase.instance.client;

  // Get current user session
  static User? get currentUser => client.auth.currentUser;

  // Auth Operations
  static Future<AuthResponse> signUp(String email, String password) async {
    return await client.auth.signUp(email: email, password: password);
  }

  static Future<AuthResponse> signIn(String email, String password) async {
    return await client.auth.signInWithPassword(email: email, password: password);
  }

  static Future<void> signOut() async {
    await client.auth.signOut();
  }

  // Database Profile operations
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

  static Future<void> upsertProfile({
    required String name,
    required String goal,
    required String profession,
    required int totalXp,
  }) async {
    final user = currentUser;
    if (user == null) return;

    await client.from('karma_profiles').upsert({
      'id': user.id,
      'name': name,
      'goal': goal,
      'profession': profession,
      'total_xp': totalXp,
    });
  }

  // Database Tasks operations
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

    final taskData = {
      if (taskId != null) 'id': taskId,
      'user_id': user.id,
      'title': title,
      'description': description,
      'xp': xp,
      'is_completed': isCompleted,
    };

    await client.from('karma_tasks').upsert(taskData);
  }

  static Future<void> updateTaskCompletion(String taskId, bool isCompleted) async {
    await client
        .from('karma_tasks')
        .update({'is_completed': isCompleted})
        .eq('id', taskId);
  }

  static Future<void> deleteTask(String taskId) async {
    await client.from('karma_tasks').delete().eq('id', taskId);
  }
}
