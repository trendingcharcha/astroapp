import 'package:flutter/material.dart';
import '../services/ai_service.dart';

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
}

class HomeDashboard extends StatefulWidget {
  const HomeDashboard({super.key});

  @override
  State<HomeDashboard> createState() => _HomeDashboardState();
}

class _HomeDashboardState extends State<HomeDashboard> {
  // Sample Task List
  final List<KarmaTask> _tasks = [
    KarmaTask(title: "Feed Birds", description: "Feed grains to birds in the morning.", karmaPoints: 15),
    KarmaTask(title: "Clutter-free Desk", description: "Clean your study/work desk in North-East.", karmaPoints: 10),
    KarmaTask(title: "Chant Mantra", description: "108 chants of Om Suryaya Namah.", karmaPoints: 20),
    KarmaTask(title: "Help a Colleague", description: "Assist a peer with a technical challenge.", karmaPoints: 25),
  ];

  String _aiSuggestion = "Click the button below to ask the Karma AI for a custom daily task!";
  bool _isLoadingAi = false;

  int get totalKarma => _tasks.fold(0, (sum, task) => sum + (task.isCompleted ? task.karmaPoints : 0));
  int get maxKarma => _tasks.fold(0, (sum, task) => sum + task.karmaPoints);
  double get progressPercentage => maxKarma == 0 ? 0.0 : totalKarma / maxKarma;

  void _getAiTask() async {
    setState(() {
      _isLoadingAi = true;
      _aiSuggestion = "Reading your stars and career goals...";
    });

    try {
      final suggestion = await AIService.generateDailyTask(
        goal: "Get Software Job",
        profession: "Flutter Developer",
      );
      setState(() {
        _aiSuggestion = suggestion;
      });
    } catch (e) {
      setState(() {
        _aiSuggestion = "Failed to load task. Please check your internet connection.";
      });
    } finally {
      setState(() {
        _isLoadingAi = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('KarmaQuest Dashboard', style: TextStyle(color: Color(0xFFE8C879))),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Karma Progress Card
            Card(
              color: const Color(0xFF14102C),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Your Ecliptic Karma', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                        Text('$totalKarma / $maxKarma XP', style: const TextStyle(color: Color(0xFFE8C879), fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const SizedBox(height: 15),
                    LinearProgressIndicator(
                      value: progressPercentage,
                      backgroundColor: Colors.grey[800],
                      color: const Color(0xFF8E6FD6),
                      minHeight: 10,
                    ),
                    const SizedBox(height: 10),
                    Text(
                      '${(progressPercentage * 100).toStringAsFixed(0)}% Daily Mission Completed',
                      style: TextStyle(color: Colors.grey[400], fontSize: 12),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 25),

            // AI Suggestion Box
            const Text('AI Astro Coach Advice', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFFE8C879))),
            const SizedBox(height: 10),
            Card(
              color: const Color(0xFF1B163B),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _aiSuggestion,
                      style: const TextStyle(fontSize: 14, height: 1.4, fontStyle: FontStyle.italic),
                    ),
                    const SizedBox(height: 15),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: _isLoadingAi ? null : _getAiTask,
                        icon: _isLoadingAi 
                            ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                            : const Icon(Icons.psychology, color: Colors.black),
                        label: const Text('Ask Astro Coach', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFFE8C879),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                        ),
                      ),
                    )
                  ],
                ),
                  ),
            ),
            const SizedBox(height: 25),

            // Task List Header
            const Text('Daily Karma Quests', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFFE8C879))),
            const SizedBox(height: 10),

            // Task List
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _tasks.length,
              itemBuilder: (context, index) {
                final task = _tasks[index];
                return Card(
                  color: const Color(0xFF14102C),
                  margin: const EdgeInsets.only(bottom: 10),
                  child: ListTile(
                    leading: Checkbox(
                      value: task.isCompleted,
                      activeColor: const Color(0xFF8E6FD6),
                      onChanged: (val) {
                        setState(() {
                          task.isCompleted = val ?? false;
                        });
                      },
                    ),
                    title: Text(
                      task.title,
                      style: TextStyle(
                        decoration: task.isCompleted ? TextDecoration.lineThrough : null,
                        color: task.isCompleted ? Colors.grey : Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    subtitle: Text(task.description, style: TextStyle(color: Colors.grey[400])),
                    trailing: Text('+${task.karmaPoints} XP', style: const TextStyle(color: Color(0xFFE8C879))),
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
