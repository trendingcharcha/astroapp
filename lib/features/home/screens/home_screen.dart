import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../auth/providers/auth_provider.dart';
import '../../auth/screens/login_screen.dart';
import '../../kundli/providers/chart_provider.dart';
import '../../kundli/screens/kundli_form_screen.dart';
import '../../kundli/screens/kundli_result_screen.dart';
import '../../../core/astrology/astrology_engine.dart';
import '../../../core/localization/localization.dart';
import '../../../core/theme/cosmic_theme.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  int _currentIndex = 0;

  final List<Widget> _tabs = [
    const HomeTab(),
    const KundliTab(),
    const MatchingTab(),
    const TarotTab(),
    const SettingsTab(),
  ];

  @override
  Widget build(BuildContext context) {
    final local = CosmoLocalization.of(ref);

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: CosmicTheme.cosmicGradient),
        child: IndexedStack(
          index: _currentIndex,
          children: _tabs,
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        type: BottomNavigationBarType.fixed,
        backgroundColor: CosmicTheme.surface,
        selectedItemColor: CosmicTheme.primaryGold,
        unselectedItemColor: CosmicTheme.textSecondary.withOpacity(0.6),
        items: [
          BottomNavigationBarItem(icon: const Icon(Icons.home_outlined), activeIcon: const Icon(Icons.home), label: local.translate('home')),
          BottomNavigationBarItem(icon: const Icon(Icons.explore_outlined), activeIcon: const Icon(Icons.explore), label: local.translate('kundli')),
          BottomNavigationBarItem(icon: const Icon(Icons.favorite_border), activeIcon: const Icon(Icons.favorite), label: local.translate('matching')),
          BottomNavigationBarItem(icon: const Icon(Icons.filter_b_and_w_outlined), activeIcon: const Icon(Icons.filter_b_and_w), label: local.translate('tarot')),
          BottomNavigationBarItem(icon: const Icon(Icons.settings_outlined), activeIcon: const Icon(Icons.settings), label: local.translate('settings')),
        ],
      ),
    );
  }
}

// ==========================================
// 1. HOME TAB (Dashboard & Horoscope)
// ==========================================
class HomeTab extends ConsumerWidget {
  const HomeTab({Key? key}) : super(key: key);

  // Sample static horoscopes
  static const Map<String, String> horoscopeData = {
    "Aries": "Today, trust your pioneering spirit. A sudden burst of energy will help you resolve a long-standing career issue. Stay patient in communications.",
    "Taurus": "Focus on stability. Financial plans made today will bear fruit. Spend time in nature to recharge your grounding energies.",
    "Gemini": "Your mental agility is at an all-time high. A great day to write, pitch ideas, or connect with estranged friends.",
    "Cancer": "Listen to your intuition. A quiet, reflective morning will help you navigate emotional currents with family members.",
    "Leo": "The Sun shines on your self-expression. Leading a project or taking center stage at work will bring positive attention.",
    "Virgo": "Attention to detail is your superpower today. You'll organize complex schedules easily, but remember to rest your mind.",
    "Libra": "Harmony is returning. You'll find it easy to balance conflicting viewpoints in relationships. A good day for artistic expression.",
    "Scorpio": "Your inner transformation is visible. Face your fears directly; you're supported in letting go of old habits.",
    "Sagittarius": "Adventure calls! Expand your horizons through research or learning. A philosophical outlook helps resolve conflicts.",
    "Capricorn": "Focus on structure and duty. Long-term goals are aligning nicely. Keep working diligently, rewards are on the horizon.",
    "Aquarius": "Your humanitarian values are highlighted. Engage in community service or share your innovative solutions.",
    "Pisces": "Dreams and creativity flow naturally today. Meditate or express your insights through music or art. Trust your gut."
  };

  void _showHoroscopeSheet(BuildContext context, String sign) {
    showModalBottomSheet(
      context: context,
      backgroundColor: CosmicTheme.surface,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.only(topLeft: Radius.circular(20), topRight: Radius.circular(20)),
      ),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    "$sign Horoscope",
                    style: const TextStyle(color: CosmicTheme.primaryGold, fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  const Icon(Icons.stars, color: CosmicTheme.primaryGold),
                ],
              ),
              const Divider(color: Color(0xFF2A244E), height: 30),
              const Text(
                "DAILY PREDICTION",
                style: TextStyle(color: CosmicTheme.accentPurple, fontWeight: FontWeight.bold, fontSize: 12),
              ),
              const SizedBox(height: 10),
              Text(
                horoscopeData[sign] ?? "Your cosmic alignments are shifting.",
                style: const TextStyle(color: Colors.white, fontSize: 15, height: 1.4),
              ),
              const SizedBox(height: 30),
              ElevatedButton(
                onPressed: () => Navigator.pop(context),
                child: const Text("CLOSE"),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final local = CosmoLocalization.of(ref);
    final authState = ref.watch(authProvider);

    // Calculate current Panchang for today
    final now = DateTime.now();
    double jd = AstrologyEngine.calculateJulianDay(now.year, now.month, now.day, 12, 0, 0, 5.5);
    Map<String, dynamic> panchang = AstrologyEngine.calculatePanchang(jd, 28.6139, 77.2090);

    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          // Welcome Header
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Namaste,",
                    style: TextStyle(color: CosmicTheme.textSecondary.withOpacity(0.8), fontSize: 16),
                  ),
                  Text(
                    authState.displayName ?? "Cosmic Seeker",
                    style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.all(10),
                decoration: const BoxDecoration(color: CosmicTheme.surface, shape: BoxShape.circle),
                child: const Icon(Icons.wb_sunny, color: CosmicTheme.primaryGold, size: 28),
              )
            ],
          ),
          const SizedBox(height: 25),

          // Daily Panchang Card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        local.translate('current_panchang'),
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: CosmicTheme.primaryGold),
                      ),
                      Text(
                        DateFormat('dd MMM yyyy').format(DateTime.now()),
                        style: const TextStyle(fontSize: 12, color: CosmicTheme.textSecondary),
                      ),
                    ],
                  ),
                  const Divider(color: Color(0xFF2A244E), height: 25),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      _buildPanchangItem("Tithi", panchang["tithi"]),
                      _buildPanchangItem("Nakshatra", panchang["nakshatra"]),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      _buildPanchangItem("Yoga", panchang["yoga"]),
                      _buildPanchangItem("Day (Vara)", panchang["vara"]),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 25),

          // Horoscope Title
          Text(
            local.translate('daily_horoscope'),
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
          ),
          const SizedBox(height: 12),

          // Zodiac Horizontal List
          SizedBox(
            height: 105,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: 12,
              itemBuilder: (context, idx) {
                String sign = AstrologyEngine.signNamesEN[idx];
                String signHI = AstrologyEngine.signNamesHI[idx];
                String activeLang = ref.watch(localeProvider);
                
                return GestureDetector(
                  onTap: () => _showHoroscopeSheet(context, sign),
                  child: Container(
                    width: 85,
                    margin: const EdgeInsets.only(right: 12),
                    decoration: BoxDecoration(
                      color: CosmicTheme.surface,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: const Color(0xFF2A244E)),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.star_outline, color: CosmicTheme.primaryGold, size: 24),
                        const SizedBox(height: 6),
                        Text(
                          activeLang == 'en' ? sign : signHI,
                          style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 25),

          // Quick Tools Entry
          Text(
            local.translate('quick_tools'),
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
          ),
          const SizedBox(height: 12),

          // Quick tools grid
          GridTile(
            child: Row(
              children: [
                Expanded(
                  child: _buildQuickToolCard(
                    context,
                    "Create Chart",
                    Icons.explore,
                    () => Navigator.push(context, MaterialPageRoute(builder: (_) => const KundliFormScreen())),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildQuickToolCard(
                    context,
                    "Numerology",
                    Icons.pin,
                    () => Navigator.push(context, MaterialPageRoute(builder: (_) => const NumerologyScreen())),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPanchangItem(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(color: CosmicTheme.textSecondary, fontSize: 11)),
        const SizedBox(height: 2),
        Text(
          value,
          style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }

  Widget _buildQuickToolCard(BuildContext context, String title, IconData icon, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: CosmicTheme.surface,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: const Color(0xFF2A244E)),
        ),
        child: Column(
          children: [
            Icon(icon, color: CosmicTheme.primaryGold, size: 30),
            const SizedBox(height: 10),
            Text(
              title,
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================
// 2. KUNDLI TAB (Saved & History)
// ==========================================
class KundliTab extends ConsumerWidget {
  const KundliTab({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final chartState = ref.watch(chartProvider);
    final local = CosmoLocalization.of(ref);

    return Scaffold(
      appBar: AppBar(title: Text(local.translate('saved_charts'))),
      body: chartState.savedCharts.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.explore_off_outlined, color: Colors.white24, size: 64),
                  const SizedBox(height: 16),
                  const Text("No saved charts found", style: TextStyle(color: Colors.white54)),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.push(context, MaterialPageRoute(builder: (_) => const KundliFormScreen()));
                    },
                    child: Text(local.translate('generate_kundli')),
                  ),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: chartState.savedCharts.length,
              itemBuilder: (context, idx) {
                final saved = chartState.savedCharts[idx];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    leading: const Icon(Icons.explore, color: CosmicTheme.primaryGold),
                    title: Text(saved.name, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                    subtitle: Text("${saved.location} | ${saved.dateTime}", style: const TextStyle(fontSize: 12)),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete_outline, color: CosmicTheme.accentPurple),
                      onPressed: () {
                        ref.read(chartProvider.notifier).deleteChart(saved.id);
                      },
                    ),
                    onTap: () {
                      // Reload in state and show
                      // In a real app we'd save inputs instead of outputs, but we can simulate the load:
                      List<String> dt = saved.dateTime.split(" ");
                      final details = BirthDetails(
                        name: saved.name,
                        date: DateTime.parse(dt[0]),
                        timeString: dt[1],
                        cityName: saved.location,
                        latitude: 28.6139,
                        longitude: 77.2090,
                        timezoneOffset: 5.5,
                      );
                      ref.read(chartProvider.notifier).generateChart(details);
                      Navigator.push(context, MaterialPageRoute(builder: (_) => const KundliResultScreen()));
                    },
                  ),
                );
              },
            ),
      floatingActionButton: chartState.savedCharts.isNotEmpty
          ? FloatingActionButton(
              backgroundColor: CosmicTheme.primaryGold,
              child: const Icon(Icons.add, color: Color(0xFF14102C)),
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const KundliFormScreen()));
              },
            )
          : null,
    );
  }
}

// ==========================================
// 3. MATCHING TAB (Ashta Koota / 36 Gunas)
// ==========================================
class MatchingTab extends StatefulWidget {
  const MatchingTab({Key? key}) : super(key: key);

  @override
  State<MatchingTab> createState() => _MatchingTabState();
}

class _MatchingTabState extends State<MatchingTab> {
  // Dropdown values
  int femaleSignIdx = 0;
  int maleSignIdx = 0;
  int femaleNakIdx = 0;
  int maleNakIdx = 0;

  Map<String, dynamic>? matchingResult;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Kundli Matching")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              "Calculate Ashta Koota Compatibility Score (36 Gunas)",
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white70, fontSize: 13),
            ),
            const SizedBox(height: 25),

            // Bride selection card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("Bride (Female) Moon Details", style: TextStyle(color: CosmicTheme.primaryGold, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 12),
                    DropdownButtonFormField<int>(
                      value: femaleSignIdx,
                      decoration: const InputDecoration(labelText: "Moon Sign"),
                      items: List.generate(12, (idx) {
                        return DropdownMenuItem(value: idx, child: Text(AstrologyEngine.signNamesEN[idx]));
                      }),
                      onChanged: (val) {
                        setState(() {
                          femaleSignIdx = val ?? 0;
                        });
                      },
                    ),
                    const SizedBox(height: 12),
                    DropdownButtonFormField<int>(
                      value: femaleNakIdx,
                      decoration: const InputDecoration(labelText: "Moon Nakshatra"),
                      items: List.generate(27, (idx) {
                        return DropdownMenuItem(value: idx, child: Text(AstrologyEngine.nakshatrasEN[idx]));
                      }),
                      onChanged: (val) {
                        setState(() {
                          femaleNakIdx = val ?? 0;
                        });
                      },
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Groom selection card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("Groom (Male) Moon Details", style: TextStyle(color: CosmicTheme.primaryGold, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 12),
                    DropdownButtonFormField<int>(
                      value: maleSignIdx,
                      decoration: const InputDecoration(labelText: "Moon Sign"),
                      items: List.generate(12, (idx) {
                        return DropdownMenuItem(value: idx, child: Text(AstrologyEngine.signNamesEN[idx]));
                      }),
                      onChanged: (val) {
                        setState(() {
                          maleSignIdx = val ?? 0;
                        });
                      },
                    ),
                    const SizedBox(height: 12),
                    DropdownButtonFormField<int>(
                      value: maleNakIdx,
                      decoration: const InputDecoration(labelText: "Moon Nakshatra"),
                      items: List.generate(27, (idx) {
                        return DropdownMenuItem(value: idx, child: Text(AstrologyEngine.nakshatrasEN[idx]));
                      }),
                      onChanged: (val) {
                        setState(() {
                          maleNakIdx = val ?? 0;
                        });
                      },
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 25),

            ElevatedButton(
              onPressed: () {
                // Approximate longitude from choices
                double fLon = (femaleSignIdx * 30.0) + (femaleNakIdx % 2 * 13.333 + 5.0);
                double mLon = (maleSignIdx * 30.0) + (maleNakIdx % 2 * 13.333 + 5.0);

                final res = AstrologyEngine.calculateAshtaKoota(fLon, mLon);
                setState(() {
                  matchingResult = res;
                });
              },
              child: const Text("CALCULATE COMPATIBILITY"),
            ),

            if (matchingResult != null) ...[
              const SizedBox(height: 30),
              Card(
                color: const Color(0xFF1B143E),
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      const Text(
                        "Matching Result Score",
                        style: TextStyle(color: CosmicTheme.textSecondary, fontSize: 13),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        "${matchingResult!['score']} / 36.0",
                        style: const TextStyle(color: CosmicTheme.primaryGold, fontSize: 36, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        matchingResult!['result'],
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 14),
                      ),
                      const Divider(color: Color(0xFF2A244E), height: 30),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: (matchingResult!['breakdown'] as List<String>).map((str) {
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4),
                            child: Text("• $str", style: const TextStyle(color: Colors.white70, fontSize: 12)),
                          );
                        }).toList(),
                      ),
                    ],
                  ),
                ),
              )
            ]
          ],
        ),
      ),
    );
  }
}

// ==========================================
// 4. TAROT TAB (Draw Card Reading)
// ==========================================
class TarotTab extends StatefulWidget {
  const TarotTab({Key? key}) : super(key: key);

  @override
  State<TarotTab> createState() => _TarotTabState();
}

class _TarotTabState extends State<TarotTab> {
  bool isDrawn = false;
  String cardName = "";
  String cardArcana = "";
  String cardMeaning = "";
  IconData cardIcon = Icons.help_outline;

  static const List<Map<String, dynamic>> tarotCards = [
    {
      "name": "The Fool",
      "arcana": "Major Arcana (0)",
      "icon": Icons.directions_walk,
      "meaning": "Represents new beginnings, clean slates, faith, and spontaneity. The cosmos is urging you to take a leap of faith."
    },
    {
      "name": "The Magician",
      "arcana": "Major Arcana (I)",
      "icon": Icons.auto_awesome,
      "meaning": "Indicates manifestation, willpower, resourcefulness, and skill. You hold all the tools to manifest your dreams."
    },
    {
      "name": "The High Priestess",
      "arcana": "Major Arcana (II)",
      "icon": Icons.self_improvement,
      "meaning": "Signifies intuition, subconscious mind, divine feminine, and sacred knowledge. Tune in to your inner voice."
    },
    {
      "name": "The Empress",
      "arcana": "Major Arcana (III)",
      "icon": Icons.local_florist,
      "meaning": "Vibrates abundance, creativity, fertility, and nature. Growth, comfort, and safety surround your immediate path."
    },
    {
      "name": "The Emperor",
      "arcana": "Major Arcana (IV)",
      "icon": Icons.account_balance,
      "meaning": "Stands for authority, structure, solid foundation, and protection. Bring discipline to your finances and work."
    }
  ];

  void _drawCard() {
    setState(() {
      // Pick a random card
      final idx = DateTime.now().millisecond % tarotCards.length;
      final card = tarotCards[idx];
      cardName = card["name"];
      cardArcana = card["arcana"];
      cardMeaning = card["meaning"];
      cardIcon = card["icon"];
      isDrawn = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Tarot Card Reading")),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (!isDrawn) ...[
                const Icon(Icons.auto_stories, color: CosmicTheme.primaryGold, size: 64),
                const SizedBox(height: 20),
                const Text(
                  "Focus on a question. Clear your mind, then draw a card from the deck.",
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white70, fontSize: 14, height: 1.4),
                ),
                const SizedBox(height: 40),
                ElevatedButton(
                  onPressed: _drawCard,
                  child: const Text("DRAW TAROT CARD"),
                )
              ] else ...[
                // Animated Card Display
                Container(
                  width: 200,
                  height: 320,
                  decoration: BoxDecoration(
                    color: CosmicTheme.surface,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: CosmicTheme.primaryGold, width: 2),
                    boxShadow: [
                      BoxShadow(
                        color: CosmicTheme.primaryGold.withOpacity(0.2),
                        blurRadius: 25,
                        spreadRadius: 2,
                      )
                    ],
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(cardIcon, color: CosmicTheme.primaryGold, size: 64),
                      const SizedBox(height: 25),
                      Text(
                        cardName,
                        style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold, letterSpacing: 1.5),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        cardArcana,
                        style: const TextStyle(color: CosmicTheme.accentPurple, fontSize: 12, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 30),
                Text(
                  cardMeaning,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.5, fontStyle: FontStyle.italic),
                ),
                const SizedBox(height: 40),
                OutlinedButton(
                  onPressed: () {
                    setState(() {
                      isDrawn = false;
                    });
                  },
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: CosmicTheme.primaryGold),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                  ),
                  child: const Text("DRAW ANOTHER CARD", style: TextStyle(color: CosmicTheme.primaryGold)),
                )
              ],
            ],
          ),
        ),
      ),
    );
  }
}

// ==========================================
// 5. SETTINGS TAB (Profile, Language, numerology)
// ==========================================
class SettingsTab extends ConsumerWidget {
  const SettingsTab({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final local = CosmoLocalization.of(ref);
    final authState = ref.watch(authProvider);
    final currentLang = ref.watch(localeProvider);

    return Scaffold(
      appBar: AppBar(title: Text(local.translate('settings'))),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Profile card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  const CircleAvatar(
                    radius: 30,
                    backgroundColor: CosmicTheme.accentPurple,
                    child: Icon(Icons.person, color: Colors.white, size: 30),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          authState.displayName ?? "Cosmic Seeker",
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.white),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          authState.email ?? "Guest Mode session",
                          style: const TextStyle(color: CosmicTheme.textSecondary, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),

          // Tools Section
          const Text("ASTRO TOOLS", style: TextStyle(color: CosmicTheme.primaryGold, fontSize: 12, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          ListTile(
            leading: const Icon(Icons.pin, color: CosmicTheme.primaryGold),
            title: const Text("Numerology Calculator", style: TextStyle(color: Colors.white)),
            subtitle: const Text("Calculate Life Path and Destiny Numbers"),
            trailing: const Icon(Icons.chevron_right, color: Colors.white54),
            onTap: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => const NumerologyScreen()));
            },
          ),
          const Divider(color: Color(0xFF2A244E)),

          // Language Switcher
          const SizedBox(height: 10),
          const Text("SYSTEM", style: TextStyle(color: CosmicTheme.primaryGold, fontSize: 12, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          ListTile(
            leading: const Icon(Icons.language, color: CosmicTheme.primaryGold),
            title: Text(local.translate('language'), style: const TextStyle(color: Colors.white)),
            subtitle: Text(currentLang == 'en' ? "English" : "हिन्दी"),
            trailing: Switch(
              value: currentLang == 'hi',
              onChanged: (val) {
                ref.read(localeProvider.notifier).state = val ? 'hi' : 'en';
              },
              activeColor: CosmicTheme.primaryGold,
              activeTrackColor: const Color(0xFF2A244E),
            ),
          ),
          const Divider(color: Color(0xFF2A244E)),

          // Sign Out
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () async {
              await ref.read(authProvider.notifier).signOut();
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (_) => const LoginScreen()),
              );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF381414),
              foregroundColor: Colors.redAccent,
              shadowColor: Colors.transparent,
            ),
            child: const Text("LOG OUT"),
          ),
        ],
      ),
    );
  }
}

// ==========================================
// 6. NUMEROLOGY SCREEN
// ==========================================
class NumerologyScreen extends StatefulWidget {
  const NumerologyScreen({Key? key}) : super(key: key);

  @override
  State<NumerologyScreen> createState() => _NumerologyScreenState();
}

class _NumerologyScreenState extends State<NumerologyScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  DateTime _dob = DateTime.now();

  Map<String, dynamic>? _results;

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  void _calculate() {
    if (!_formKey.currentState!.validate()) return;
    
    final dobStr = DateFormat('yyyyMMdd').format(_dob);
    final res = AstrologyEngine.calculateNumerology(_nameController.text, dobStr);

    setState(() {
      _results = res;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Numerology Calculator")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                "Find the cosmic vibrations of your name and birth date",
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white70, fontSize: 13),
              ),
              const SizedBox(height: 25),

              TextFormField(
                controller: _nameController,
                style: const TextStyle(color: Colors.white),
                decoration: const InputDecoration(
                  labelText: "Your Full Name",
                  prefixIcon: Icon(Icons.person_outline, color: CosmicTheme.primaryGold),
                ),
                validator: (val) => val == null || val.isEmpty ? "Please enter your name" : null,
              ),
              const SizedBox(height: 16),

              InkWell(
                onTap: () async {
                  final picked = await showDatePicker(
                    context: context,
                    initialDate: _dob,
                    firstDate: DateTime(1900),
                    lastDate: DateTime.now(),
                  );
                  if (picked != null) {
                    setState(() {
                      _dob = picked;
                    });
                  }
                },
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                  decoration: BoxDecoration(
                    color: const Color(0xFF1A1438),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFF2A244E)),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text("Date of Birth", style: TextStyle(color: CosmicTheme.primaryGold, fontSize: 12)),
                          const SizedBox(height: 4),
                          Text(
                            DateFormat('dd MMMM yyyy').format(_dob),
                            style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                      const Icon(Icons.calendar_today, color: CosmicTheme.primaryGold),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 25),

              ElevatedButton(
                onPressed: _calculate,
                child: const Text("CALCULATE NUMEROLOGY"),
              ),

              if (_results != null) ...[
                const SizedBox(height: 30),
                Card(
                  color: const Color(0xFF1B143E),
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      children: [
                        _buildNumberResult("Life Path Number", _results!["lifePath"], _results!["lifePathDesc"]),
                        const Divider(color: Color(0xFF2A244E), height: 30),
                        _buildNumberResult("Destiny (Expression) Number", _results!["destiny"], _results!["destinyDesc"]),
                        const Divider(color: Color(0xFF2A244E), height: 30),
                        _buildNumberResult("Soul Urge (Heart Desire)", _results!["soulUrge"], _results!["soulUrgeDesc"]),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNumberResult(String label, int number, String desc) {
    return Column(
      children: [
        Text(label, style: const TextStyle(color: CosmicTheme.textSecondary, fontSize: 12)),
        const SizedBox(height: 4),
        Container(
          width: 48,
          height: 48,
          decoration: const BoxDecoration(color: CosmicTheme.primaryGold, shape: BoxShape.circle),
          child: Center(
            child: Text(
              "$number",
              style: const TextStyle(color: Color(0xFF14102C), fontSize: 24, fontWeight: FontWeight.bold),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          desc,
          textAlign: TextAlign.center,
          style: const TextStyle(color: Colors.white70, fontSize: 13, height: 1.4),
        ),
      ],
    );
  }
}
