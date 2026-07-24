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

  static Future<bool> signInWithGoogle() async {
    return await client.auth.signInWithOAuth(OAuthProvider.google);
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
      final existing = await fetchRawProfile();
      Map<String, dynamic> activeGoals = {};
      if (existing != null && existing['active_goals'] != null) {
        activeGoals = Map<String, dynamic>.from(existing['active_goals']);
      }
      activeGoals['goals'] = [goal];
      activeGoals['profession'] = profession;
      activeGoals['total_xp'] = totalXp;

      await client.from('profiles').upsert({
        'id': user.id,
        'full_name': name,
        'gender': existing?['gender'] ?? 'M',
        'dob': existing?['dob'] ?? '1990-01-01',
        'tob': existing?['tob'] ?? '12:00',
        'pob': existing?['pob'] ?? 'New Delhi',
        'lat': existing?['lat'] ?? 28.6139,
        'lng': existing?['lng'] ?? 77.2090,
        'timezone': existing?['timezone'] ?? 5.5,
        'active_goals': activeGoals,
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
      final fullName = profileData['name'] ?? 'Seeker';
      final gender = profileData['gender'] ?? 'M';
      final dobStr = profileData['dob'] ?? '1990-01-01';
      final tobStr = profileData['tob'] ?? '12:00';
      final pob = profileData['pob'] ?? 'New Delhi';

      // Parse coordinates safely
      final double lat = profileData['lat'] != null ? double.parse(profileData['lat'].toString()) : 28.6139;
      final double lng = profileData['lng'] != null ? double.parse(profileData['lng'].toString()) : 77.2090;
      final double timezone = profileData['timezone'] != null ? double.parse(profileData['timezone'].toString()) : 5.5;

      // Extract existing active_goals to preserve tasks/XP/streak if already set
      Map<String, dynamic> activeGoals = {};
      try {
        final existing = await fetchRawProfile();
        if (existing != null && existing['active_goals'] != null) {
          activeGoals = Map<String, dynamic>.from(existing['active_goals']);
        }
      } catch (e) {}

      // Update onboarding details
      activeGoals['goals'] = [profileData['goal'] ?? 'job'];
      activeGoals['onboarding_path'] = profileData['onboarding_path'] ?? 'single';
      activeGoals['profession'] = profileData['profession'] ?? '';
      activeGoals['custom_issue'] = profileData['custom_issue'] ?? '';
      activeGoals['property_number'] = profileData['property_number'] ?? '';
      activeGoals['property_type'] = profileData['property_type'] ?? '';
      activeGoals['property_city'] = profileData['property_city'] ?? '';
      activeGoals['baby_number'] = profileData['baby_number'] ?? '';
      activeGoals['first_baby_dob'] = profileData['first_baby_dob'] ?? '';
      activeGoals['first_baby_age'] = profileData['first_baby_age'] ?? '';
      activeGoals['second_baby_age'] = profileData['second_baby_age'] ?? '';
      activeGoals['include_partner'] = profileData['include_partner'] ?? false;
      activeGoals['partner_name'] = profileData['partner_name'] ?? '';
      activeGoals['partner_dob'] = profileData['partner_dob'] ?? '';
      activeGoals['partner_tob'] = profileData['partner_tob'] ?? '';
      activeGoals['partner_pob'] = profileData['partner_pob'] ?? '';
      activeGoals['partner_gender'] = profileData['partner_gender'] ?? 'F';
      activeGoals['total_xp'] = profileData['total_xp'] ?? activeGoals['total_xp'] ?? 0;
      activeGoals['level'] = profileData['level'] ?? activeGoals['level'] ?? 1;
      activeGoals['streak'] = profileData['streak'] ?? activeGoals['streak'] ?? 0;

      await client.from('profiles').upsert({
        'id': user.id,
        'full_name': fullName,
        'gender': gender,
        'dob': dobStr,
        'tob': tobStr,
        'pob': pob,
        'lat': lat,
        'lng': lng,
        'timezone': timezone,
        'active_goals': activeGoals,
        'updated_at': DateTime.now().toIso8601String(),
      });
    } catch (e) {
      // Silently fail on cloud sync
    }
  }

  /// Helper to fetch raw profile columns
  static Future<Map<String, dynamic>?> fetchRawProfile() async {
    final user = currentUser;
    if (user == null) return null;
    try {
      final response = await client
          .from('profiles')
          .select()
          .eq('id', user.id)
          .maybeSingle();
      return response;
    } catch (e) {
      return null;
    }
  }

  /// Fetch profile from cloud and map to local format
  static Future<Map<String, dynamic>?> fetchProfile() async {
    try {
      final response = await fetchRawProfile();
      if (response != null) {
        final activeGoals = response['active_goals'] ?? {};
        final Map<String, dynamic> profileData = {
          'name': response['full_name'],
          'gender': response['gender'],
          'dob': response['dob'],
          'tob': response['tob'],
          'pob': response['pob'],
          'lat': response['lat'],
          'lng': response['lng'],
          'timezone': response['timezone'],
        };

        if (activeGoals is Map) {
          if (activeGoals.containsKey('goals') && activeGoals['goals'] is List && (activeGoals['goals'] as List).isNotEmpty) {
            profileData['goal'] = activeGoals['goals'][0];
          }
          profileData['onboarding_path'] = activeGoals['onboarding_path'];
          profileData['profession'] = activeGoals['profession'];
          profileData['custom_issue'] = activeGoals['custom_issue'];
          profileData['property_number'] = activeGoals['property_number'];
          profileData['property_type'] = activeGoals['property_type'];
          profileData['property_city'] = activeGoals['property_city'];
          profileData['baby_number'] = activeGoals['baby_number'];
          profileData['first_baby_dob'] = activeGoals['first_baby_dob'];
          profileData['first_baby_age'] = activeGoals['first_baby_age'];
          profileData['second_baby_age'] = activeGoals['second_baby_age'];
          profileData['include_partner'] = activeGoals['include_partner'];
          profileData['partner_name'] = activeGoals['partner_name'];
          profileData['partner_dob'] = activeGoals['partner_dob'];
          profileData['partner_tob'] = activeGoals['partner_tob'];
          profileData['partner_pob'] = activeGoals['partner_pob'];
          profileData['partner_gender'] = activeGoals['partner_gender'];
          profileData['total_xp'] = activeGoals['total_xp'];
          profileData['level'] = activeGoals['level'];
          profileData['streak'] = activeGoals['streak'];
        }
        return profileData;
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  /// Update total XP for user
  static Future<void> updateXp(int totalXp) async {
    final user = currentUser;
    if (user == null) return;

    try {
      final existing = await fetchRawProfile();
      Map<String, dynamic> activeGoals = {};
      if (existing != null && existing['active_goals'] != null) {
        activeGoals = Map<String, dynamic>.from(existing['active_goals']);
      }
      activeGoals['total_xp'] = totalXp;

      await client.from('profiles').update({
        'active_goals': activeGoals,
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
      final existing = await fetchRawProfile();
      if (existing != null && existing['active_goals'] != null) {
        final activeGoals = Map<String, dynamic>.from(existing['active_goals']);
        if (activeGoals.containsKey('tasks') && activeGoals['tasks'] is List) {
          return List<Map<String, dynamic>>.from(activeGoals['tasks']);
        }
      }
    } catch (e) {
      // Fallback
    }
    return [];
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
      final existing = await fetchRawProfile();
      Map<String, dynamic> activeGoals = {};
      if (existing != null && existing['active_goals'] != null) {
        activeGoals = Map<String, dynamic>.from(existing['active_goals']);
      }

      final List<dynamic> tasks = List.from(activeGoals['tasks'] ?? []);
      final int index = tasks.indexWhere((t) => t['title'] == title);

      final taskData = {
        'id': taskId ?? 'task_${title.replaceAll(' ', '_').toLowerCase()}',
        'title': title,
        'description': description,
        'xp': xp,
        'is_completed': isCompleted,
      };

      if (index != -1) {
        tasks[index] = taskData;
      } else {
        tasks.add(taskData);
      }

      activeGoals['tasks'] = tasks;

      await client.from('profiles').update({
        'active_goals': activeGoals,
        'updated_at': DateTime.now().toIso8601String(),
      }).eq('id', user.id);
    } catch (e) {
      // Silently fail
    }
  }

  static Future<void> updateTaskCompletion(String taskId, bool isCompleted) async {
    final user = currentUser;
    if (user == null) return;

    try {
      final existing = await fetchRawProfile();
      Map<String, dynamic> activeGoals = {};
      if (existing != null && existing['active_goals'] != null) {
        activeGoals = Map<String, dynamic>.from(existing['active_goals']);
      }

      final List<dynamic> tasks = List.from(activeGoals['tasks'] ?? []);
      final int index = tasks.indexWhere((t) => t['id'] == taskId);

      if (index != -1) {
        tasks[index]['is_completed'] = isCompleted;
        activeGoals['tasks'] = tasks;

        await client.from('profiles').update({
          'active_goals': activeGoals,
          'updated_at': DateTime.now().toIso8601String(),
        }).eq('id', user.id);
      }
    } catch (e) {
      // Silently fail
    }
  }

  static Future<void> deleteTask(String taskId) async {
    final user = currentUser;
    if (user == null) return;

    try {
      final existing = await fetchRawProfile();
      Map<String, dynamic> activeGoals = {};
      if (existing != null && existing['active_goals'] != null) {
        activeGoals = Map<String, dynamic>.from(existing['active_goals']);
      }

      final List<dynamic> tasks = List.from(activeGoals['tasks'] ?? []);
      tasks.removeWhere((t) => t['id'] == taskId);
      activeGoals['tasks'] = tasks;

      await client.from('profiles').update({
        'active_goals': activeGoals,
        'updated_at': DateTime.now().toIso8601String(),
      }).eq('id', user.id);
    } catch (e) {
      // Silently fail
    }
  }

  static Future<void> clearAllTasks() async {
    final user = currentUser;
    if (user == null) return;

    try {
      final existing = await fetchRawProfile();
      Map<String, dynamic> activeGoals = {};
      if (existing != null && existing['active_goals'] != null) {
        activeGoals = Map<String, dynamic>.from(existing['active_goals']);
      }

      activeGoals['tasks'] = [];

      await client.from('profiles').update({
        'active_goals': activeGoals,
        'updated_at': DateTime.now().toIso8601String(),
      }).eq('id', user.id);
    } catch (e) {
      // Silently fail
    }
  }
}
