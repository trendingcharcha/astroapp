import 'package:flutter/material.dart';

// Short codes for rendering planets on the chart
const Map<String, String> planetShortCodes = {
  "Lagna": "As",
  "Sun": "Su",
  "Moon": "Mo",
  "Mars": "Ma",
  "Mercury": "Me",
  "Jupiter": "Ju",
  "Venus": "Ve",
  "Saturn": "Sa",
  "Rahu": "Ra",
  "Ketu": "Ke"
};

class KundliChartWidget extends StatefulWidget {
  final List<Map<String, dynamic>> planetPlacements; // Comes from vargas["D1"] or similar
  final String chartTitle;

  const KundliChartWidget({
    Key? key,
    required this.planetPlacements,
    required this.chartTitle,
  }) : super(key: key);

  @override
  State<KundliChartWidget> createState() => _KundliChartWidgetState();
}

class _KundliChartWidgetState extends State<KundliChartWidget> {
  bool isNorthIndian = true;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              widget.chartTitle,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFE8C879)),
            ),
            Row(
              children: [
                const Text("South", style: TextStyle(fontSize: 12, color: Colors.white70)),
                Switch(
                  value: isNorthIndian,
                  onChanged: (val) {
                    setState(() {
                      isNorthIndian = val;
                    });
                  },
                  activeColor: const Color(0xFFE8C879),
                  activeTrackColor: const Color(0xFF2A244E),
                  inactiveThumbColor: const Color(0xFF8E6FD6),
                  inactiveTrackColor: const Color(0xFF14102C),
                ),
                const Text("North", style: TextStyle(fontSize: 12, color: Colors.white70)),
              ],
            ),
          ],
        ),
        const SizedBox(height: 10),
        AspectRatio(
          aspectRatio: 1,
          child: Container(
            decoration: BoxDecoration(
              color: const Color(0xFF0C0922),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFFE8C879).withOpacity(0.5), width: 1.5),
              boxShadow: [
                BoxShadow(
                  color: const Color(0xFF8E6FD6).withOpacity(0.15),
                  blurRadius: 15,
                  spreadRadius: 2,
                )
              ]
            ),
            child: CustomPaint(
              painter: isNorthIndian
                  ? NorthIndianChartPainter(widget.planetPlacements)
                  : SouthIndianChartPainter(widget.planetPlacements),
            ),
          ),
        ),
      ],
    );
  }
}

// ----------------------------------------------------
// NORTH INDIAN (DIAMOND STYLE) CUSTOM PAINTER
// ----------------------------------------------------
class NorthIndianChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> planetPlacements;

  NorthIndianChartPainter(this.planetPlacements);

  @override
  void paint(Canvas canvas, Size size) {
    double w = size.width;
    double h = size.height;

    final linePaint = Paint()
      ..color = const Color(0xFFE8C879)
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;

    final goldFillPaint = Paint()
      ..color = const Color(0xFFE8C879)
      ..style = PaintingStyle.fill;

    // 1. Draw outer boundary box
    canvas.drawRect(Rect.fromLTWH(0, 0, w, h), linePaint);

    // 2. Draw diagonals
    canvas.drawLine(Offset(0, 0), Offset(w, h), linePaint);
    canvas.drawLine(Offset(w, 0), Offset(0, h), linePaint);

    // 3. Draw internal diamonds
    canvas.drawLine(Offset(w / 2, 0), Offset(0, h / 2), linePaint);
    canvas.drawLine(Offset(0, h / 2), Offset(w / 2, h), linePaint);
    canvas.drawLine(Offset(w / 2, h), Offset(w, h / 2), linePaint);
    canvas.drawLine(Offset(w, h / 2), Offset(w / 2, 0), linePaint);

    // 4. Map houses (1 to 12) to geometric coordinate centers and boundaries
    // North Indian charts go counter-clockwise starting from the top diamond (House 1)
    // We will place the zodiac sign numbers and list of planets in each house.
    
    // Find Lagna sign
    var lagnaPlacement = planetPlacements.firstWhere((p) => p["name"] == "Lagna", orElse: () => {"sign": 0});
    int lagnaSign = lagnaPlacement["sign"] + 1; // 1-based zodiac sign (1=Aries, 2=Taurus...)

    // Map each house relative to the Lagna sign
    // House 1 has Lagna Sign. House 2 has (Lagna Sign + 1) etc.
    Map<int, int> houseToSign = {};
    for (int h = 1; h <= 12; h++) {
      int signVal = (lagnaSign - 1 + (h - 1)) % 12 + 1;
      houseToSign[h] = signVal;
    }

    // Group planets by house (1-12)
    Map<int, List<String>> housePlanets = {};
    for (int h = 1; h <= 12; h++) {
      housePlanets[h] = [];
    }

    for (var planet in planetPlacements) {
      String name = planet["name"];
      int sign = planet["sign"] + 1;
      // Calculate house index for planet based on Lagna sign
      int houseIdx = (sign - lagnaSign + 12) % 12 + 1;
      String short = planetShortCodes[name] ?? name;
      housePlanets[houseIdx]!.add(short);
    }

    // Define label center offset and sign number offset for each of the 12 houses
    // Values are fractional multipliers of width and height
    final List<Offset> houseCenters = [
      Offset(w * 0.5, h * 0.28),   // House 1 (Top Center Diamond)
      Offset(w * 0.25, h * 0.16),  // House 2 (Top Left Triangle)
      Offset(w * 0.16, h * 0.25),  // House 3 (Middle Left Top)
      Offset(w * 0.28, h * 0.5),   // House 4 (Left Center Diamond)
      Offset(w * 0.16, h * 0.75),  // House 5 (Middle Left Bottom)
      Offset(w * 0.25, h * 0.84),  // House 6 (Bottom Left Triangle)
      Offset(w * 0.5, h * 0.72),   // House 7 (Bottom Center Diamond)
      Offset(w * 0.75, h * 0.84),  // House 8 (Bottom Right Triangle)
      Offset(w * 0.84, h * 0.75),  // House 9 (Middle Right Bottom)
      Offset(w * 0.72, h * 0.5),   // House 10 (Right Center Diamond)
      Offset(w * 0.84, h * 0.25),  // House 11 (Middle Right Top)
      Offset(w * 0.75, h * 0.16),  // House 12 (Top Right Triangle)
    ];

    final List<Offset> signNumberOffsets = [
      Offset(w * 0.5, h * 0.38),   // House 1
      Offset(w * 0.33, h * 0.22),  // House 2
      Offset(w * 0.22, h * 0.33),  // House 3
      Offset(w * 0.38, h * 0.5),   // House 4
      Offset(w * 0.22, h * 0.67),  // House 5
      Offset(w * 0.33, h * 0.78),  // House 6
      Offset(w * 0.5, h * 0.62),   // House 7
      Offset(w * 0.67, h * 0.78),  // House 8
      Offset(w * 0.78, h * 0.67),  // House 9
      Offset(w * 0.62, h * 0.5),   // House 10
      Offset(w * 0.78, h * 0.33),  // House 11
      Offset(w * 0.67, h * 0.22),  // House 12
    ];

    // Render numbers and planets
    for (int i = 0; i < 12; i++) {
      int houseNum = i + 1;
      int signNum = houseToSign[houseNum]!;
      List<String> planets = housePlanets[houseNum]!;

      // 1. Draw Zodiac Sign Number (small text in gold)
      final textSpan = TextSpan(
        text: "$signNum",
        style: const TextStyle(
          color: Color(0xFFE8C879),
          fontSize: 10,
          fontWeight: FontWeight.bold,
        ),
      );
      final textPainter = TextPainter(
        text: textSpan,
        textDirection: TextDirection.ltr,
      )..layout();
      
      Offset signOffset = signNumberOffsets[i];
      textPainter.paint(canvas, Offset(signOffset.dx - textPainter.width / 2, signOffset.dy - textPainter.height / 2));

      // 2. Draw Planets inside the house
      if (planets.isNotEmpty) {
        String planetsText = planets.join(" ");
        final planetSpan = TextSpan(
          text: planetsText,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 11,
            fontWeight: FontWeight.bold,
          ),
        );
        final planetPainter = TextPainter(
          text: planetSpan,
          textDirection: TextDirection.ltr,
        )..layout();

        Offset center = houseCenters[i];
        planetPainter.paint(
          canvas,
          Offset(center.dx - planetPainter.width / 2, center.dy - planetPainter.height / 2),
        );
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

// ----------------------------------------------------
// SOUTH INDIAN (GRID STYLE) CUSTOM PAINTER
// ----------------------------------------------------
class SouthIndianChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> planetPlacements;

  SouthIndianChartPainter(this.planetPlacements);

  @override
  void paint(Canvas canvas, Size size) {
    double w = size.width;
    double h = size.height;

    final linePaint = Paint()
      ..color = const Color(0xFFE8C879)
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;

    // 1. Draw 4x4 Grid layout (12 outer boxes, center 4 boxes empty)
    double stepW = w / 4;
    double stepH = h / 4;

    // Draw grid lines
    canvas.drawRect(Rect.fromLTWH(0, 0, w, h), linePaint);
    
    // Horizontal lines
    canvas.drawLine(Offset(0, stepH), Offset(w, stepH), linePaint);
    canvas.drawLine(Offset(0, stepH * 2), Offset(stepW, stepH * 2), linePaint);
    canvas.drawLine(Offset(stepW * 3, stepH * 2), Offset(w, stepH * 2), linePaint);
    canvas.drawLine(Offset(0, stepH * 3), Offset(w, stepH * 3), linePaint);

    // Vertical lines
    canvas.drawLine(Offset(stepW, 0), Offset(stepW, h), linePaint);
    canvas.drawLine(Offset(stepW * 2, 0), Offset(stepW * 2, stepH), linePaint);
    canvas.drawLine(Offset(stepW * 2, stepH * 3), Offset(stepW * 2, h), linePaint);
    canvas.drawLine(Offset(stepW * 3, 0), Offset(stepW * 3, h), linePaint);

    // 2. Map South Indian layout box indices (0 to 11) to actual signs starting from Aries
    // South Indian charts have fixed sign locations going clockwise:
    // Box (Row, Col) mapping:
    // Row 0: Aries (col 1), Taurus (col 2), Gemini (col 3), Cancer (col 4)
    // Row 1: Leo (col 4), Virgo (col 4)
    // Row 2: Libra (col 4), Scorpio (col 4)
    // Row 3: Sagittarius (col 4), Capricorn (col 3), Aquarius (col 2), Pisces (col 1)
    // Let's index the 12 boxes clockwise starting from Aries:
    // Index 0: Pisces (Col 0, Row 0) -> Wait, traditional layout:
    // Row 0: Box 1 (Col 1) = Aries, Box 2 (Col 2) = Taurus, Box 3 (Col 3) = Gemini, Box 4 (Col 4) = Cancer
    // Row 1: Col 3 = Leo
    // Row 2: Col 3 = Virgo
    // Row 3: Col 3 = Libra, Col 2 = Scorpio, Col 1 = Sagittarius, Col 0 = Capricorn
    // Row 2: Col 0 = Aquarius
    // Row 1: Col 0 = Pisces
    // Let's build a clean list of grid cell coordinates matching Aries (1) to Pisces (12)
    final List<Map<String, int>> signGridCoords = [
      {"r": 0, "c": 1}, // Aries (1)
      {"r": 0, "c": 2}, // Taurus (2)
      {"r": 0, "c": 3}, // Gemini (3)
      {"r": 1, "c": 3}, // Cancer (4)
      {"r": 2, "c": 3}, // Leo (5)
      {"r": 3, "c": 3}, // Virgo (6)
      {"r": 3, "c": 2}, // Libra (7)
      {"r": 3, "c": 1}, // Scorpio (8)
      {"r": 3, "c": 0}, // Sagittarius (9)
      {"r": 2, "c": 0}, // Capricorn (10)
      {"r": 1, "c": 0}, // Aquarius (11)
      {"r": 0, "c": 0}, // Pisces (12)
    ];

    // Group planets by sign index (0-11)
    Map<int, List<String>> signPlanets = {};
    for (int i = 0; i < 12; i++) {
      signPlanets[i] = [];
    }

    for (var planet in planetPlacements) {
      String name = planet["name"];
      int sign = planet["sign"]; // 0 to 11
      String short = planetShortCodes[name] ?? name;
      signPlanets[sign]!.add(short);
    }

    // Render center Title inside the central blank 2x2 area
    final centerSpan = TextSpan(
      text: "COSMOVEDIC\nD1 CHART",
      style: TextStyle(
        color: const Color(0xFFE8C879).withOpacity(0.3),
        fontSize: 14,
        fontWeight: FontWeight.bold,
        letterSpacing: 1.5,
      ),
    );
    final centerPainter = TextPainter(
      text: centerSpan,
      textAlign: TextAlign.center,
      textDirection: TextDirection.ltr,
    )..layout();
    centerPainter.paint(
      canvas,
      Offset(w / 2 - centerPainter.width / 2, h / 2 - centerPainter.height / 2),
    );

    // Draw sign names and planets inside each box
    for (int s = 0; s < 12; s++) {
      var coords = signGridCoords[s];
      double boxLeft = coords["c"]! * stepW;
      double boxTop = coords["r"]! * stepH;

      // 1. Draw zodiac sign name (abbreviation) in gold in top-left of box
      String signName = AstrologyEngine.signNamesEN[s].substring(0, 3).toUpperCase();
      final signSpan = TextSpan(
        text: signName,
        style: const TextStyle(
          color: Color(0xFF8E6FD6),
          fontSize: 9,
          fontWeight: FontWeight.bold,
        ),
      );
      final signPainter = TextPainter(
        text: signSpan,
        textDirection: TextDirection.ltr,
      )..layout();
      signPainter.paint(canvas, Offset(boxLeft + 4, boxTop + 4));

      // 2. Draw Planets inside the box (centered)
      List<String> planets = signPlanets[s]!;
      if (planets.isNotEmpty) {
        String planetsText = planets.join("\n");
        final planetSpan = TextSpan(
          text: planetsText,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 10,
            fontWeight: FontWeight.bold,
            height: 1.2,
          ),
        );
        final planetPainter = TextPainter(
          text: planetSpan,
          textAlign: TextAlign.center,
          textDirection: TextDirection.ltr,
        )..layout();

        planetPainter.paint(
          canvas,
          Offset(
            boxLeft + (stepW - planetPainter.width) / 2,
            boxTop + (stepH - planetPainter.height) / 2 + 3,
          ),
        );
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
