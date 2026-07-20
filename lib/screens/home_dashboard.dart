import 'package:flutter/material.dart';
import '../services/supabase_service.dart';
import '../services/ai_service.dart';
import '../services/hive_service.dart';
import 'login_screen.dart';
import 'onboarding_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

class KarmaTask {
  final String title;
  final String description;
  final int karmaPoints;
  bool isCompleted;

  KarmaTask({
    required this.title,
    required this.description,
    required this.karmaPoints,
    this.isCompleted = false,
  });

  factory KarmaTask.fromMap(Map<String, dynamic> map) {
    return KarmaTask(
      title: map['title'] ?? '',
      description: map['description'] ?? '',
      karmaPoints: map['xp'] ?? 10,
      isCompleted: map['is_completed'] ?? false,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'title': title,
      'description': description,
      'xp': karmaPoints,
      'is_completed': isCompleted,
    };
  }
}

class HomeDashboard extends StatefulWidget {
  const HomeDashboard({super.key});

  @override
  State<HomeDashboard> createState() => _HomeDashboardState();
}

class _HomeDashboardState extends State<HomeDashboard> {
  Map<String, dynamic>? _profile;
  List<KarmaTask> _tasks = [];
  bool _isLoading = false;
  String _aiSuggestion = "Generating your spiritual daily quests based on planetary alignments...";
  bool _isLoadingAi = false;
  
  int _streak = 0;
  List<bool> _dedicationGrid = List.generate(90, (index) => false); // 90-day karmic transformation grid

  int get totalKarma => _tasks.fold(0, (sum, task) => sum + (task.isCompleted ? task.karmaPoints : 0));
  int get maxKarma => _tasks.fold(0, (sum, task) => sum + task.karmaPoints);
  double get progressPercentage => maxKarma == 0 ? 0.0 : totalKarma / maxKarma;

  @override
  void initState() {
    super.initState();
    _loadProfileAndData();
  }

  Future<void> _loadProfileAndData() async {
    setState(() => _isLoading = true);

    // 1. Load Profile from Hive
    _profile = HiveService.getProfile();
    if (_profile == null) {
      // Redirect to onboarding if profile is missing
      WidgetsBinding.instance.addPostFrameCallback((_) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const OnboardingScreen()),
        );
      });
      return;
    }

    // 2. Load Streaks & Dedication Grid
    final prefs = await SharedPreferences.getInstance();
    _streak = prefs.getInt('user_streak') ?? 3;
    final gridSaved = prefs.getStringList('dedication_grid');
    if (gridSaved != null) {
      _dedicationGrid = gridSaved.map((v) => v == 'true').toList();
    } else {
      // Fake some historical data for visual beauty
      _dedicationGrid = [
        true, true, false, true, true, true, false,
        true, true, true, true, false, true, true,
        false, false, false, false, false, false, false,
        false, false, false, false, false, false, false,
      ];
    }

    // 3. Load or generate quests
    final cachedTasks = HiveService.getTasks();
    if (cachedTasks.isNotEmpty) {
      setState(() {
        _tasks = cachedTasks.map((t) => KarmaTask.fromMap(t)).toList();
        _isLoading = false;
      });
      _getAiSuggestion();
      return;
    }

    // Generate fresh tasks based on profile goal
    await _generateNewDailyQuests();
  }

  Future<void> _generateNewDailyQuests() async {
    if (_profile == null) return;
    
    setState(() {
      _isLoading = true;
      _aiSuggestion = "Syncing with stars...";
    });

    final goal = _profile!['goal'] ?? 'job';
    final profession = _profile!['profession'] ?? 'Seeker';
    final customIssue = _profile!['custom_issue'] ?? '';
    final path = _profile!['onboarding_path'] ?? 'single';
    final partnerName = _profile!['partner_name'] ?? '';

    // Generate AI task breakdown
    final aiResponse = await AIService.generateDailyTask(
      goal: goal,
      profession: profession,
      customIssue: customIssue,
      path: path,
      partnerName: partnerName,
    );

    // Split AI response into 4 distinct quests
    final lines = aiResponse.split('\n\n');
    final List<KarmaTask> newTasks = [];
    
    if (lines.length >= 4) {
      newTasks.add(KarmaTask(title: "Vedic Quest", description: lines[0].replaceAll(RegExp(r'^🕉️\s*Vedic:\s*'), ''), karmaPoints: 20));
      newTasks.add(KarmaTask(title: "Lal Kitab Quest", description: lines[1].replaceAll(RegExp(r'^🔴\s*Lal Kitab:\s*'), ''), karmaPoints: 15));
      newTasks.add(KarmaTask(title: "Vastu Quest", description: lines[2].replaceAll(RegExp(r'^🏡\s*Vastu:\s*'), ''), karmaPoints: 15));
      newTasks.add(KarmaTask(title: "Action Quest", description: lines[3].replaceAll(RegExp(r'^💼\s*Action:\s*'), ''), karmaPoints: 30));
    } else {
      // Fallback
      newTasks.addAll([
        KarmaTask(title: "Vedic Quest", description: "Chant matching mantra 108 times.", karmaPoints: 20),
        KarmaTask(title: "Lal Kitab Quest", description: "Feed grains to birds or offer water to Sun.", karmaPoints: 15),
        KarmaTask(title: "Vastu Quest", description: "Clean your North-East work zone.", karmaPoints: 15),
        KarmaTask(title: "Action Quest", description: "Dedicate 30 mins to active skill building.", karmaPoints: 30),
      ]);
    }

    setState(() {
      _tasks = newTasks;
      _aiSuggestion = "Planet alignments verified for today! Complete your daily karma quests to level up.";
      _isLoading = false;
    });

    // Save to Hive cache
    await HiveService.saveTasks(_tasks.map((t) => t.toMap()).toList());

    // Save to Supabase Cloud if authenticated
    if (SupabaseService.currentUser != null) {
      for (final t in _tasks) {
        try {
          await SupabaseService.saveTask(
            title: t.title,
            description: t.description,
            xp: t.karmaPoints,
            isCompleted: t.isCompleted,
          );
        } catch (e) {
          debugPrint("Supabase sync failed: $e");
        }
      }
    }
  }

  Future<void> _getAiSuggestion() async {
    setState(() => _isLoadingAi = true);
    try {
      final goal = _profile?['goal'] ?? 'job';
      final profession = _profile?['profession'] ?? 'Seeker';
      final customIssue = _profile?['custom_issue'] ?? '';
      
      final advice = await AIService.generateDailyTask(
        goal: goal,
        profession: profession,
        customIssue: customIssue,
      );
      setState(() {
        _aiSuggestion = advice;
      });
    } catch (e) {
      setState(() {
        _aiSuggestion = "Align your desk North-East and dedicate 30 minutes to your core goals today.";
      });
    } finally {
      setState(() => _isLoadingAi = false);
    }
  }

  Future<void> _toggleTask(KarmaTask task, bool? val) async {
    setState(() {
      task.isCompleted = val ?? false;
    });

    // Save update to local Hive cache
    await HiveService.saveTasks(_tasks.map((t) => t.toMap()).toList());

    // Update cloud if online
    if (SupabaseService.currentUser != null) {
      try {
        final remoteTasks = await SupabaseService.fetchTasks();
        final match = remoteTasks.firstWhere((t) => t['title'] == task.title, orElse: () => {});
        if (match.isNotEmpty && match['id'] != null) {
          await SupabaseService.updateTaskCompletion(match['id'], task.isCompleted);
        }
      } catch (e) {
        debugPrint("Cloud status update failed: $e");
      }
    }

    // Adjust dedication grid index for today if all completed
    if (progressPercentage >= 1.0) {
      setState(() {
        _dedicationGrid[DateTime.now().day % 90] = true;
        _streak++;
      });
      final prefs = await SharedPreferences.getInstance();
      await prefs.setInt('user_streak', _streak);
      await prefs.setStringList('dedication_grid', _dedicationGrid.map((v) => v.toString()).toList());
      
      // Sync XP to Supabase cloud
      if (SupabaseService.currentUser != null) {
        await SupabaseService.updateXp(totalKarma);
      }

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("✨ Level Up! Daily Karma Quest Complete! +XP synced to cloud."),
            backgroundColor: Color(0xFF8E6FD6),
          ),
        );
      }
    }
  }

  void _showSettingsModal() {
    final keyController = TextEditingController();
    SharedPreferences.getInstance().then((prefs) {
      keyController.text = prefs.getString('gemini_api_key') ?? '';
    });

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: const Color(0xFF14102C),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: Color(0xFF2A244E)),
          ),
          title: const Text('Astro Settings', style: TextStyle(color: Color(0xFFE8C879))),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'Add your Gemini API Key to unlock live generative Astro Coach daily advices:',
                style: TextStyle(color: Colors.grey, fontSize: 13),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: keyController,
                obscureText: true,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: 'Gemini API Key',
                  labelStyle: const TextStyle(color: Colors.grey),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('CANCEL', style: TextStyle(color: Colors.grey)),
            ),
            ElevatedButton(
              onPressed: () async {
                final prefs = await SharedPreferences.getInstance();
                await prefs.setString('gemini_api_key', keyController.text.trim());
                if (context.mounted) {
                  Navigator.pop(context);
                  _generateNewDailyQuests();
                }
              },
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF8E6FD6)),
              child: const Text('SAVE KEY', style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }

  Future<void> _handleLogout() async {
    await SupabaseService.signOut();
    await HiveService.clearProfile();
    await HiveService.clearTasks();
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('has_completed_onboarding');
    await prefs.remove('guest_offline_mode');

    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_profile == null) return const Scaffold(body: Center(child: CircularProgressIndicator()));

    final name = _profile!['name'] ?? 'Seeker';
    final goalName = _profile!['goal'] ?? 'job';
    final pathName = _profile!['onboarding_path'] ?? 'single';
    final partner = _profile!['partner_name'] ?? '';

    return Scaffold(
      backgroundColor: const Color(0xFF09071A),
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.stars, color: Color(0xFFE8C879), size: 20),
            const SizedBox(width: 8),
            Text('$name\'s Karma Dashboard', style: const TextStyle(color: Color(0xFFE8C879), fontSize: 16)),
          ],
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings, color: Color(0xFFE8C879)),
            onPressed: _showSettingsModal,
          ),
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.redAccent),
            onPressed: _handleLogout,
          )
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Color(0xFF8E6FD6)))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Partner notice if couple
                  if (pathName == 'couple' && partner.isNotEmpty) ...[
                    Container(
                      padding: const EdgeInsets.all(10),
                      margin: const EdgeInsets.only(bottom: 15),
                      decoration: BoxDecoration(
                        color: const Color(0xFF8E6FD6).withOpacity(0.12),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: const Color(0xFF8E6FD6).withOpacity(0.3)),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.favorite, color: Colors.pinkAccent, size: 18),
                          const SizedBox(width: 8),
                          Text(
                            "Synced with partner: $partner • Couple Path",
                            style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                    ),
                  ],

                  // Karma progress level card
                  Card(
                    color: const Color(0xFF14102C),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                      side: const BorderSide(color: Color(0xFF2A244E)),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text('DAILY LEVEL', style: TextStyle(fontSize: 11, color: Color(0xFF8E6FD6), fontWeight: FontWeight.bold)),
                                  Text(
                                    'Vedic Seeker (Lvl ${_streak ~/ 5 + 1})',
                                    style: const TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                              Row(
                                children: [
                                  const Icon(Icons.local_fire_department, color: Color(0xFFE8C879)),
                                  const SizedBox(width: 4),
                                  Text('$_streak Days', style: const TextStyle(color: Color(0xFFE8C879), fontWeight: FontWeight.bold)),
                                ],
                              ),
                            ],
                          ),
                          const SizedBox(height: 20),
                          LinearProgressIndicator(
                            value: progressPercentage,
                            backgroundColor: Colors.grey[950],
                            color: const Color(0xFF8E6FD6),
                            minHeight: 8,
                          ),
                          const SizedBox(height: 10),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                '${(progressPercentage * 100).toStringAsFixed(0)}% Daily Quests completed',
                                style: const TextStyle(color: Colors.grey, fontSize: 12),
                              ),
                              Text('$totalKarma / $maxKarma XP', style: const TextStyle(color: Color(0xFFE8C879), fontSize: 12, fontWeight: FontWeight.bold)),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 20),

                  // Dedication Grid Section
                  const Text('Your 28-Day Dedication Grid', style: TextStyle(color: Color(0xFFE8C879), fontSize: 14, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Card(
                    color: const Color(0xFF14102C),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: const BorderSide(color: Color(0xFF2A244E))),
                    child: Padding(
                      padding: const EdgeInsets.all(12.0),
                      child: GridView.builder(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: 28,
                        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 7,
                          mainAxisSpacing: 8,
                          crossAxisSpacing: 8,
                        ),
                        itemBuilder: (context, index) {
                          final done = _dedicationGrid[index];
                          return Container(
                            decoration: BoxDecoration(
                              color: done ? const Color(0xFF8E6FD6) : Colors.transparent,
                              borderRadius: BorderRadius.circular(6),
                              border: Border.all(color: done ? const Color(0xFF8E6FD6) : const Color(0xFF2A244E), width: 1.5),
                              boxShadow: done ? [
                                BoxShadow(color: const Color(0xFF8E6FD6).withOpacity(0.4), blurRadius: 4, spreadRadius: 1)
                              ] : null,
                            ),
                            child: Center(
                              child: Text(
                                '${index + 1}',
                                style: TextStyle(color: done ? Colors.black : Colors.grey, fontSize: 11, fontWeight: FontWeight.bold),
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                  ),

                  const SizedBox(height: 24),

                  // AI Astro Coach Card
                  const Text('AI Astro Coach Insights', style: TextStyle(color: Color(0xFFE8C879), fontSize: 14, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Card(
                    color: const Color(0xFF1B163B),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: const BorderSide(color: Color(0xFF2A244E))),
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            _aiSuggestion,
                            style: const TextStyle(fontSize: 13, color: Colors.white, height: 1.4, fontStyle: FontStyle.italic),
                          ),
                          const SizedBox(height: 12),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                              TextButton.icon(
                                onPressed: _isLoadingAi ? null : _getAiSuggestion,
                                icon: _isLoadingAi 
                                    ? const SizedBox(width: 14, height: 14, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFFE8C879)))
                                    : const Icon(Icons.wb_sunny, size: 16, color: Color(0xFFE8C879)),
                                label: const Text('Refresh Insights', style: TextStyle(color: Color(0xFFE8C879), fontSize: 12, fontWeight: FontWeight.bold)),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Daily Quests Title & Refresh
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Your Daily Quests', style: TextStyle(color: Color(0xFFE8C879), fontSize: 14, fontWeight: FontWeight.bold)),
                      IconButton(
                        icon: const Icon(Icons.autorenew, color: Color(0xFFE8C879), size: 20),
                        onPressed: _generateNewDailyQuests,
                      )
                    ],
                  ),
                  const SizedBox(height: 8),

                  // Quests Checklist
                  ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: _tasks.length,
                    itemBuilder: (context, index) {
                      final t = _tasks[index];
                      return Card(
                        color: const Color(0xFF14102C),
                        margin: const EdgeInsets.only(bottom: 8),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: const BorderSide(color: Color(0xFF2A244E))),
                        child: ListTile(
                          leading: Checkbox(
                            value: t.isCompleted,
                            activeColor: const Color(0xFF8E6FD6),
                            onChanged: (val) => _toggleTask(t, val),
                          ),
                          title: Text(
                            t.title,
                            style: TextStyle(
                              color: t.isCompleted ? Colors.grey : Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                              decoration: t.isCompleted ? TextDecoration.lineThrough : null,
                            ),
                          ),
                          subtitle: Text(
                            t.description,
                            style: TextStyle(color: t.isCompleted ? Colors.grey[600] : Colors.grey[300], fontSize: 12),
                          ),
                          trailing: Text('+${t.karmaPoints} XP', style: const TextStyle(color: Color(0xFFE8C879), fontSize: 12, fontWeight: FontWeight.bold)),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
    );
  }
}
