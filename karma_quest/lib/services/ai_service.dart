import 'dart:convert';
import 'package:http/http.dart' as http;

class AIService {
  // A clean, beginner-friendly function executing a prompt query to a free LLM or local mockup
  static Future<String> generateDailyTask({required String goal, required String profession}) async {
    final prompt = """
    Role: Vedic + Lal Kitab Astrologer + Career Coach
    Goal: $goal
    Profession: $profession
    Generate a specific daily mission suggestion. Keep it concise, positive and actionable.
    """;

    try {
      // Connect to your backend API endpoint or serverless function
      final response = await http.post(
        Uri.parse('https://api.openai.com/v1/chat/completions'), // Placeholder API URL
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'prompt': prompt,
        }),
      ).timeout(const Duration(seconds: 3));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['text'] ?? "Align your desk North and apply for 3 $profession positions today.";
      }
    } catch (e) {
      // Dynamic local backup suggestions:
      final fallbackSuggestions = [
        "🕉️ Vedic: Chant 'Om Suryaya Namah' 108 times.\n🔴 Lal Kitab: Offer water in a copper vessel to Sun.\n🏡 Vastu: Keep work desk in North-East.\n💼 Action: Tailor your resume summary specifically for a $profession role today.",
        "🕉️ Vedic: Chant 'Om Budhaya Namah' 108 times.\n🔴 Lal Kitab: Feed birds with 7 grains.\n🏡 Vastu: Place a green plant on your desk.\n💼 Action: Apply to at least 3 relevant $profession roles on Naukri or LinkedIn.",
        "🕉️ Vedic: Chant 'Om Guruve Namah' 108 times.\n🔴 Lal Kitab: Donate yellow sweets to a temple.\n🏡 Vastu: Sit facing North while working.\n💼 Action: Reach out to 5 senior $profession professionals on LinkedIn today."
      ];
      // Select a random recommendation based on hash code of the current day to change it daily!
      final dayIndex = DateTime.now().day % fallbackSuggestions.length;
      return fallbackSuggestions[dayIndex];
    }
    
    return "Optimize your workdesk layout today and prepare to apply to 3 $profession jobs tomorrow morning.";
  }
}
