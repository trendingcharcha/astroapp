import 'package:hive_flutter/hive_flutter.dart';

class HiveService {
  static const String tasksBoxName = 'local_tasks_box';
  static const String profileBoxName = 'local_profile_box';

  static Future<void> init() async {
    await Hive.initFlutter();
    await Hive.openBox(tasksBoxName);
    await Hive.openBox(profileBoxName);
  }

  static Box get tasksBox => Hive.box(tasksBoxName);
  static Box get profileBox => Hive.box(profileBoxName);

  // Profile operations
  static Map<String, dynamic>? getProfile() {
    final data = profileBox.get('user_profile');
    if (data == null) return null;
    return Map<String, dynamic>.from(data);
  }

  static Future<void> saveProfile(Map<String, dynamic> profile) async {
    await profileBox.put('user_profile', profile);
  }

  static Future<void> clearProfile() async {
    await profileBox.delete('user_profile');
  }

  // Task operations
  static List<Map<String, dynamic>> getTasks() {
    final list = tasksBox.get('tasks_list', defaultValue: []);
    return List<Map<String, dynamic>>.from(list.map((item) => Map<String, dynamic>.from(item)));
  }

  static Future<void> saveTasks(List<Map<String, dynamic>> tasks) async {
    await tasksBox.put('tasks_list', tasks);
  }

  static Future<void> clearTasks() async {
    await tasksBox.delete('tasks_list');
  }
}
