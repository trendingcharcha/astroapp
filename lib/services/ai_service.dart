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
    String? lagnaName,
    String? rulingLord,
    String? moonSignName,
    String? moonNakshatra,
    String? goalLord,
    Map<String, dynamic>? placements,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    final apiKey = prefs.getString('gemini_api_key') ?? '';

    final effectiveLagna = lagnaName ?? 'Aries';
    final effectiveLord = rulingLord ?? 'Mars';
    final effectiveMoon = moonSignName ?? 'Taurus';
    final effectiveNak = moonNakshatra ?? 'Rohini';
    final effectiveGoalLord = goalLord ?? effectiveLord;

    final prompt = """
    Role: Authentic Vedic Astrologer + Lal Kitab Expert + Vastu Shastra Consultant + Career Coach.
    User Birth Chart Kundali Data:
    - Lagna (Ascendant): $effectiveLagna (Ruled by $effectiveLord)
    - Moon Sign (Rashi): $effectiveMoon (Nakshatra: $effectiveNak)
    - Goal Significator Lord: $effectiveGoalLord
    User Path: ${path ?? 'single'}
    User Core Goal: $goal
    User Profession: $profession
    ${(customIssue != null && customIssue.isNotEmpty) ? 'Specific Custom Issue: $customIssue' : ''}
    ${(partnerName != null && partnerName.isNotEmpty) ? 'Partner Name: $partnerName' : ''}

    Task: Generate a set of 4 100% personalized daily karma quests dynamically aligned with their $effectiveLagna Lagna and $effectiveGoalLord energy:
    1. Vedic Quest: A personalized mantra or sacred ritual activating their $effectiveGoalLord and $effectiveLord.
    2. Lal Kitab Quest: A practical karmic remedy suited for their planetary alignments (e.g., offering to Sun, feeding specific birds/animals, copper/silver remedy).
    3. Vastu Quest: A directional and spatial alignment suggestion based on their Lagna lord ($effectiveLord) and work goals.
    4. Action Quest: A practical, actionable professional step for a $profession working towards their $goal goal today.

    Format the output as clear bullet points. Keep it authentic, empowering, and strictly personalized to their astrological Kundali.
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
        // Fall back to offline dynamic astrology engine
      }
    }

    // High quality dynamic offline rule-based Vedic / Lal Kitab / Vastu recommendations
    // computed directly from their calculated Kundali parameters
    final Map<String, String> planetMantras = {
      'Sun': "Chant 'Om Suryaya Namah' 108 times at sunrise facing East to amplify executive leadership and solar vitality.",
      'Moon': "Chant 'Om Som Somaya Namah' 108 times and drink water from a silver cup to balance mental peace and intuitive clarity.",
      'Mars': "Chant 'Om Bhaumaya Namah' 108 times or recite Hanuman Chalisa to eliminate obstacles and invoke bold initiative.",
      'Mercury': "Chant 'Om Budhaya Namah' 108 times facing North to sharpen analytical intellect, speech, and commercial success.",
      'Jupiter': "Chant 'Om Brihaspataye Namah' 108 times and apply a saffron or turmeric tilak to expand wisdom and fortune.",
      'Venus': "Chant 'Om Shukraya Namah' 108 times and wear clean white attire to invite harmony, elegance, and prosperity.",
      'Saturn': "Chant 'Om Sham Shanaishcharaya Namah' 108 times and light a mustard oil lamp under a Peepal tree to burn karmic blocks.",
      'Rahu': "Chant 'Om Rahave Namah' 108 times and feed mixed grains (Satnaja) to birds to clear illusions.",
      'Ketu': "Chant 'Om Ketave Namah' 108 times and donate blankets to the needy to activate spiritual detachment."
    };

    final Map<String, String> lalkitabUpays = {
      'Sun': "Offer fresh water with a pinch of red vermilion to the rising Sun from a copper vessel.",
      'Moon': "Offer raw cow's milk or sweet water to a banyan tree root and apply the damp soil tilak.",
      'Mars': "Keep a pure solid silver ball in your pocket and donate sweet rotis to stray dogs on Tuesdays.",
      'Mercury': "Feed green grass or spinach to cows and avoid gifting electronic gadgets today.",
      'Jupiter': "Donate yellow lentils (chana dal) or bananas at a spiritual temple on Thursdays.",
      'Venus': "Offer white sweets or rice pudding (kheer) to young girls or needy individuals.",
      'Saturn': "Keep a small iron ring or square silver piece and donate mustard oil on Saturdays.",
      'Rahu': "Keep a square piece of pure silver in your wallet and avoid taking or lending loans at night.",
      'Ketu': "Feed sweet bread to stray dogs and keep a small silver coin with a central hole."
    };

    final Map<String, String> vastuDirections = {
      'Sun': "Ensure your primary workspace faces East to welcome early solar energies.",
      'Moon': "Keep your North-West (Vayu corner) well-ventilated and decluttered to allow smooth emotional flow.",
      'Mars': "Keep electrical appliances and heat elements aligned with the South-East (Agni zone).",
      'Mercury': "Align your office desk facing North; keep a green plant or green aventurine crystal on your table.",
      'Jupiter': "Keep the North-East (Ishan corner) exceptionally clean, light, and illuminated with natural light.",
      'Venus': "Decorate the South-East corner of your living area with fresh flowers or scented incense.",
      'Saturn': "Place heavy storage cabinets and structural files in the West or South-West sectors.",
      'Rahu': "Keep the South-West sector heavy and avoid open water features in that area.",
      'Ketu': "Keep the center of your room (Brahmasthan) completely open, clean, and unencumbered."
    };

    final vedicText = planetMantras[effectiveGoalLord] ?? planetMantras[effectiveLord] ?? planetMantras['Sun']!;
    final lkText = lalkitabUpays[effectiveGoalLord] ?? lalkitabUpays[effectiveLord] ?? lalkitabUpays['Sun']!;
    final vastuText = vastuDirections[effectiveLord] ?? vastuDirections['Jupiter']!;
    final actionText = "Dedicate 45 minutes of focused effort as a $profession towards your core $goal milestone today.";

    return "Vedic: $vedicText\n\nLal Kitab: $lkText\n\nVastu: $vastuText\n\nAction: $actionText";
  }
}
