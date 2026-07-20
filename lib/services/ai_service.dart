import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AIService {
  // Uses Google Generative AI (Gemini 1.5 Flash) with fallback to rich offline astrology rule-based engine
  static Future<String> generateDailyTask({
    required String goal,
    required String profession,
    String? customIssue,
    String? path,
    String? partnerName,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    final apiKey = prefs.getString('gemini_api_key') ?? '';

    final prompt = """
    Role: Vedic Astrologer + Lal Kitab Expert + Vastu Shastra Consultant + Career Coach.
    User Path: ${path ?? 'single'}
    User Core Goal: $goal
    User Profession: $profession
    ${(customIssue != null && customIssue.isNotEmpty) ? 'Specific Custom Issue: $customIssue' : ''}
    ${(partnerName != null && partnerName.isNotEmpty) ? 'Partner Name: $partnerName' : ''}

    Task: Generate a set of 4 daily quests:
    1. 🕉️ Vedic Quest: A simple mantra, prayer, or ritual suited for the goal.
    2. 🔴 Lal Kitab Quest: A practical karmic remedy (e.g., feeding birds, watering tree, donating).
    3. 🏡 Vastu Quest: A home alignment suggestion (direction of desk, mirrors, colors).
    4. 💼 Action Quest: A practical, actionable career or life step to progress towards the goal today.

    Format the output as clear bullet points. Keep it concise, encouraging, and highly specific to the goal.
    """;

    if (apiKey.isNotEmpty) {
      try {
        final model = GenerativeModel(
          model: 'gemini-1.5-flash',
          apiKey: apiKey,
        );
        final content = [Content.text(prompt)];
        final response = await model.generateContent(content);
        if (response.text != null && response.text!.isNotEmpty) {
          return response.text!;
        }
      } catch (e) {
        // Fall back silently to offline rules
      }
    }

    // High quality offline rule-based Vedic / Lal Kitab / Vastu recommendations
    // matching their exact goal configuration (similar to web app)
    final Map<String, List<String>> offlineQuests = {
      'job': [
        "🕉️ Vedic: Chant 'Om Suryaya Namah' 108 times facing East to invite career recognition.",
        "🔴 Lal Kitab: Offer fresh water with a pinch of vermilion to the rising Sun.",
        "🏡 Vastu: Ensure your work desk is facing North-East and is free of clutter.",
        "💼 Action: Tailor your resume summary specifically for a $profession role today."
      ],
      'debt': [
        "🕉️ Vedic: Recite the Rinmochan Mangal Stotra to dissolve debt energies.",
        "🔴 Lal Kitab: Feed sweet rotis to stray dogs on Tuesday evenings.",
        "🏡 Vastu: Keep your cash locker in the South-West zone facing North.",
        "💼 Action: Draft a simple financial repayment timeline and track this week's expenses."
      ],
      'marriage': [
        "🕉️ Vedic: Recite 'Om Katyayanyai Namah' (if single) or 'Om Namah Shivaya' 108 times.",
        "🔴 Lal Kitab: Donate yellow sweets or bananas to a local temple on Thursday.",
        "🏡 Vastu: Place a rose quartz crystal or pink lovebirds in the South-West of your bedroom.",
        "💼 Action: Dedicate 20 minutes to self-reflection on your relationship boundaries today."
      ],
      'baby': [
        "🕉️ Vedic: Recite the Santan Gopal Mantra together each morning for progeny blessings.",
        "🔴 Lal Kitab: Offer sweet milk to the roots of a banyan tree and apply tilak.",
        "🏡 Vastu: Keep the North-East zone of your bedroom light, clean, and decorated with fresh flowers.",
        "💼 Action: Schedule a couple's physical wellness check or track fertility calendars today."
      ],
      'business': [
        "🕉️ Vedic: Perform a simple Ganesh Puja and chant 'Om Gan Ganapataye Namah' 21 times.",
        "🔴 Lal Kitab: Feed birds with 7 mixed grains (Satnaja) before starting work.",
        "🏡 Vastu: Keep the main entrance of your store or office clean and well-lit.",
        "💼 Action: Outline 3 new networking leads or potential clients to message today."
      ],
      'property': [
        "🕉️ Vedic: Chant 'Om Bhaumaya Namah' 108 times on Tuesday to invoke Mars energy.",
        "🔴 Lal Kitab: Donate red lentils (masoor dal) to a needy person on Tuesday.",
        "🏡 Vastu: Keep the center region (Brahmasthan) of your home open and clean.",
        "💼 Action: Research real estate listings in your target city location today."
      ],
      'health': [
        "🕉️ Vedic: Chant the Maha Mrityunjaya Mantra 11 times for healing solar energy.",
        "🔴 Lal Kitab: Keep water in a copper vessel overnight and drink it first thing in the morning.",
        "🏡 Vastu: Sleep with your head pointing towards the South direction for deep rest.",
        "💼 Action: Drink 3 liters of water today and do 15 minutes of conscious pranayama breathing."
      ],
      'custom': [
        "🕉️ Vedic: Light a ghee lamp at your home temple and pray for resolution.",
        "🔴 Lal Kitab: Donate food or basic essentials to a needy person today.",
        "🏡 Vastu: Clear any old, unused, or broken electronic items from your house.",
        "💼 Action: Write down 3 actionable steps to directly address your concern: $customIssue."
      ]
    };

    final selectedList = offlineQuests[goal] ?? offlineQuests['custom']!;
    return selectedList.join('\n\n');
  }
}
