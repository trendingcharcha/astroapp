import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../auth/providers/auth_provider.dart';
import '../providers/chart_provider.dart';
import '../widgets/kundli_chart_painter.dart';

class KundliResultScreen extends ConsumerWidget {
  const KundliResultScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final chartState = ref.watch(chartProvider);
    final authState = ref.watch(authProvider);

    if (chartState.isLoading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(color: Color(0xFFE8C879)),
        ),
      );
    }

    final details = chartState.currentBirthDetails;
    final data = chartState.calculatedChartData;

    if (details == null || data == null) {
      return Scaffold(
        appBar: AppBar(title: const Text("Error")),
        body: const Center(
          child: Text("No chart data calculated.", style: TextStyle(color: Colors.white70)),
        ),
      );
    }

    final ayanamsaVal = data["ayanamsa"] as double;
    final yogas = data["yogas"] as List<String>;
    final doshas = data["doshas"] as List<String>;
    final Map<String, List<Map<String, dynamic>>> vargas = Map<String, List<Map<String, dynamic>>>.from(data["vargas"]);

    // Format Ayanamsa degrees/minutes
    int ayDegree = ayanamsaVal.floor();
    int ayMinute = ((ayanamsaVal - ayDegree) * 60).floor();
    String formattedAyanamsa = "$ayDegree° $ayMinute' (Lahiri)";

    return DefaultTabController(
      length: 5,
      child: Scaffold(
        appBar: AppBar(
          title: Text("${details.name}'s Kundli"),
          bottom: const TabBar(
            isScrollable: true,
            indicatorColor: Color(0xFFE8C879),
            labelColor: Color(0xFFE8C879),
            unselectedLabelColor: Colors.white60,
            tabs: [
              Tab(text: "D1 Rasi"),
              Tab(text: "D9 Navamsa"),
              Tab(text: "D10 Dasamsa"),
              Tab(text: "Placements"),
              Tab(text: "Yogas & Doshas"),
            ],
          ),
        ),
        body: Column(
          children: [
            // Birth Information Summary Header
            Container(
              padding: const EdgeInsets.all(16),
              margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              decoration: BoxDecoration(
                color: const Color(0xFF14102C),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: const Color(0xFF2A244E)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.stars, color: Color(0xFFE8C879), size: 40),
                  const SizedBox(width: 15),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          details.cityName,
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Colors.white),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          "${DateFormat('dd MMM yyyy').format(details.date)} | ${details.timeString}",
                          style: const TextStyle(fontSize: 12, color: Colors.white70),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          "Ayanamsa: $formattedAyanamsa",
                          style: const TextStyle(fontSize: 11, color: Color(0xFF8E6FD6), fontWeight: FontWeight.w600),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            // Tab contents
            Expanded(
              child: TabBarView(
                children: [
                  // D1 Chart Tab
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: SingleChildScrollView(
                      child: Column(
                        children: [
                          KundliChartWidget(
                            planetPlacements: vargas["D1"]!,
                            chartTitle: "D1 Birth Chart (Lagna Rasi)",
                          ),
                          const SizedBox(height: 20),
                          const Text(
                            "This chart describes the physical body and overall lifetime projection.",
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.white60, fontSize: 13),
                          )
                        ],
                      ),
                    ),
                  ),

                  // D9 Navamsa Chart Tab
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: SingleChildScrollView(
                      child: Column(
                        children: [
                          KundliChartWidget(
                            planetPlacements: vargas["D9"]!,
                            chartTitle: "D9 Navamsa Chart (Spiritual/Marriage)",
                          ),
                          const SizedBox(height: 20),
                          const Text(
                            "The Navamsa represents sub-conscious strength, spiritual path, and partnership.",
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.white60, fontSize: 13),
                          )
                        ],
                      ),
                    ),
                  ),

                  // D10 Dasamsa Chart Tab
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: SingleChildScrollView(
                      child: Column(
                        children: [
                          KundliChartWidget(
                            planetPlacements: vargas["D10"]!,
                            chartTitle: "D10 Dasamsa Chart (Career/Profession)",
                          ),
                          const SizedBox(height: 20),
                          const Text(
                            "The Dasamsa reveals professional achievements, career status, and social duty.",
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.white60, fontSize: 13),
                          )
                        ],
                      ),
                    ),
                  ),

                  // Planetary Placements Table Tab
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Table(
                      border: TableBorder.all(color: const Color(0xFF2A244E), width: 1, borderRadius: BorderRadius.circular(8)),
                      columnWidths: const {
                        0: FlexColumnWidth(2.5),
                        1: FlexColumnWidth(3.5),
                        2: FlexColumnWidth(2.5),
                      },
                      children: [
                        TableRow(
                          decoration: const BoxDecoration(color: Color(0xFF1B143E)),
                          children: [
                            _buildTableHeaderCell("Planet"),
                            _buildTableHeaderCell("Longitude & Sign"),
                            _buildTableHeaderCell("House"),
                          ],
                        ),
                        ...vargas["D1"]!.map((p) {
                          return TableRow(
                            children: [
                              _buildTableCell(p["name"], isTitle: true),
                              _buildTableCell(p["formatted"] ?? ""),
                              _buildTableCell("House ${p['house']}"),
                            ],
                          );
                        }).toList()
                      ],
                    ),
                  ),

                  // Yogas & Doshas List Tab
                  SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        const Text(
                          "YOGAS (Auspicious Combinations)",
                          style: TextStyle(color: Color(0xFFE8C879), fontWeight: FontWeight.bold, fontSize: 16),
                        ),
                        const SizedBox(height: 10),
                        if (yogas.isEmpty)
                          const Text("No significant yogas active in standard configurations.", style: TextStyle(color: Colors.white70))
                        else
                          ...yogas.map((y) => _buildYogaCard(y, true)).toList(),
                        
                        const SizedBox(height: 25),
                        const Text(
                          "DOSHAS (Inauspicious Combinations)",
                          style: TextStyle(color: Color(0xFF8E6FD6), fontWeight: FontWeight.bold, fontSize: 16),
                        ),
                        const SizedBox(height: 10),
                        if (doshas.isEmpty)
                          const Text("No critical Doshas (like Manglik or Rahu afflictions) found.", style: TextStyle(color: Colors.white70))
                        else
                          ...doshas.map((d) => _buildYogaCard(d, false)).toList(),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTableHeaderCell(String text) {
    return Padding(
      padding: const EdgeInsets.all(12),
      child: Text(
        text,
        textAlign: TextAlign.center,
        style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFFE8C879), fontSize: 13),
      ),
    );
  }

  Widget _buildTableCell(String text, {bool isTitle = false}) {
    return Padding(
      padding: const EdgeInsets.all(12),
      child: Text(
        text,
        textAlign: TextAlign.center,
        style: TextStyle(
          color: isTitle ? const Color(0xFFE8C879) : Colors.white,
          fontSize: 12,
          fontWeight: isTitle ? FontWeight.bold : FontWeight.normal,
        ),
      ),
    );
  }

  Widget _buildYogaCard(String text, bool isAuspicious) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      color: const Color(0xFF14102C),
      child: ListTile(
        leading: Icon(
          isAuspicious ? Icons.check_circle : Icons.warning_amber_rounded,
          color: isAuspicious ? const Color(0xFFE8C879) : const Color(0xFF8E6FD6),
        ),
        title: Text(
          text,
          style: const TextStyle(fontSize: 13, height: 1.3, color: Colors.white),
        ),
      ),
    );
  }
}
