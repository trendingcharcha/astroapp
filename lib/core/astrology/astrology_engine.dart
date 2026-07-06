import 'dart:math';

/// A pure-Dart Vedic Astrology Engine.
/// Calculates Julian Days, Sidereal Time, Lahiri Ayanamsa,
/// Geocentric Planetary Longitudes, Lagna (Ascendant),
/// Divisional Charts (D1, D9, D10), Ashta Koota (36 Gunas), and Panchang.
class AstrologyEngine {
  // Obliquity of the Ecliptic (approximate)
  static const double epsilon = 23.4392911 * pi / 180.0;

  // Sign Names in English and Hindi
  static const List<String> signNamesEN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
  ];

  static const List<String> signNamesHI = [
    "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
    "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"
  ];

  // Planet Names in English and Hindi
  static const List<String> planetNamesEN = [
    "Ascendant", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"
  ];

  static const List<String> planetNamesHI = [
    "लग्न", "सूर्य", "चन्द्र", "मंगल", "बुध", "गुरु", "शुक्र", "शनि", "राहु", "केतु"
  ];

  // Nakshatra Names (27 Nakshatras)
  static const List<String> nakshatrasEN = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
  ];

  static const List<String> nakshatrasHI = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा",
    "पुनर्वसु", "पुष्य", "अश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी",
    "हस्त", "चित्रा", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा",
    "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा",
    "पूर्वभाद्रपद", "उत्तरभाद्रपद", "रेवती"
  ];

  // Tithis (30 Tithis)
  static const List<String> tithisEN = [
    "Prathama", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shasthi", "Saptami", "Ashtami",
    "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima", // Shukla Paksha
    "Prathama", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shasthi", "Saptami", "Ashtami",
    "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya" // Krishna Paksha
  ];

  // Yogas (27 Yogas)
  static const List<String> yogasEN = [
    "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
    "Shula", "Ganda", "Vridhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi",
    "Vyatipata", "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti"
  ];

  // Karanas (11 Karanas)
  static const List<String> karanasEN = [
    "Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti (Bhadra)",
    "Shakuni", "Chatushpada", "Naga", "Kintughna"
  ];

  // Rashi Lords
  static const List<String> rashiLordsEN = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
  ];

  // Calculate Julian Day
  static double calculateJulianDay(int year, int month, int day, int hour, int minute, int second, double timezoneOffset) {
    // Convert local time to UTC decimal hour
    double decimalHour = hour + (minute / 60.0) + (second / 3600.0) - timezoneOffset;
    
    int y = year;
    int m = month;
    double d = day + (decimalHour / 24.0);

    if (m <= 2) {
      y -= 1;
      m += 12;
    }

    int a = (y / 100).floor();
    int b = 2 - a + (a / 4).floor();

    double jd = (365.25 * (y + 4716)).floor() + (30.6001 * (m + 1)).floor() + d + b - 1524.5;
    return jd;
  }

  // Calculate Lahiri Ayanamsa
  static double calculateLahiriAyanamsa(double jd) {
    double t = (jd - 2451545.0) / 36525.0; // Julian centuries since J2000.0
    // Lahiri Ayanamsa is approximately 23.85 degrees in 2000, changing by ~50.29 arcseconds per year
    double ayanamsa = 23.85 + (50.290966 / 3600.0) * (t * 100.0);
    return ayanamsa % 360.0;
  }

  // Calculate Greenwich Sidereal Time (GST) in degrees
  static double calculateGST(double jd) {
    double t = (jd - 2451545.0) / 36525.0;
    double gst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + t * t * 0.000387933 - t * t * t / 38710000.0;
    return gst % 360.0;
  }

  // Calculate Local Sidereal Time (LST) in degrees
  static double calculateLST(double jd, double longitude) {
    double gst = calculateGST(jd);
    double lst = gst + longitude;
    return lst % 360.0;
  }

  // Calculate Lagna (Ascendant) Longitude (Sidereal Lahiri)
  static double calculateLagna(double jd, double latitude, double longitude) {
    double lstRad = calculateLST(jd, longitude) * pi / 180.0;
    double latRad = latitude * pi / 180.0;

    // Oblique ascension formula
    double num = -cos(lstRad);
    double den = sin(lstRad) * cos(epsilon) + tan(latRad) * sin(epsilon);
    
    double lagnaRad = atan2(num, den);
    double lagnaDeg = lagnaRad * 180.0 / pi;
    lagnaDeg = (lagnaDeg + 360.0) % 360.0;

    // Subtract Ayanamsa for Sidereal Lagna
    double ayanamsa = calculateLahiriAyanamsa(jd);
    double siderealLagna = (lagnaDeg - ayanamsa + 360.0) % 360.0;
    return siderealLagna;
  }

  // Pure Dart Keplerian Orbital Calculations for Geocentric Longitudes (Tropical)
  // Standard J2000 Keplerian elements for planets
  static double _calculatePlanetTropical(double jd, String planet) {
    double t = (jd - 2451545.0) / 36525.0;

    // Orbital Elements at J2000 (a, e, I, L, longPeri, longNode)
    // Approximate parameters for basic Vedic calculations
    double a, e, I, L, w, omega;

    switch (planet) {
      case "Sun":
        a = 1.00000011;
        e = 0.01671022 - 0.00003804 * t;
        I = 0.0;
        L = 280.46646 + 36000.76983 * t;
        w = 282.93735 + 0.32242 * t;
        omega = 0.0;
        break;
      case "Mercury":
        a = 0.38709893;
        e = 0.20563069 + 0.00002040 * t;
        I = 7.00487;
        L = 252.25084 + 149472.67411 * t;
        w = 77.45645 + 0.15901 * t;
        omega = 48.33167 - 0.12537 * t;
        break;
      case "Venus":
        a = 0.72333199;
        e = 0.00677323 - 0.00004776 * t;
        I = 3.39471;
        L = 181.97973 + 58517.81538 * t;
        w = 131.53298 + 0.00201 * t;
        omega = 76.68069 - 0.27769 * t;
        break;
      case "Mars":
        a = 1.52366231;
        e = 0.09341233 + 0.00011902 * t;
        I = 1.85061;
        L = 355.45332 + 19140.30268 * t;
        w = 336.04084 + 0.44388 * t;
        omega = 49.57854 - 0.29498 * t;
        break;
      case "Jupiter":
        a = 5.20336301;
        e = 0.04839266 - 0.00012880 * t;
        I = 1.30530;
        L = 34.40438 + 3034.74612 * t;
        w = 14.75385 + 0.19152 * t;
        omega = 100.55615 + 0.20380 * t;
        break;
      case "Saturn":
        a = 9.53707032;
        e = 0.05415060 - 0.00036762 * t;
        I = 2.48446;
        L = 49.94432 + 1222.11379 * t;
        w = 92.43194 - 0.41897 * t;
        omega = 113.71504 - 0.28848 * t;
        break;
      case "Moon":
        // Moon requires a special geocentric perturbation model
        double l0 = 218.3164477 + 481267.88123421 * t; // Mean longitude
        double m = 134.9633964 + 477198.8675055 * t;  // Moon's anomaly
        double ms = 357.5277233 + 35999.05034 * t;    // Sun's anomaly
        double d = 297.8501921 + 445267.1114034 * t;  // Elongation
        double f = 93.2720950 + 483202.0175233 * t;   // Argument of latitude
        
        double lon = l0 +
            6.289 * sin(m * pi / 180.0) +
            1.274 * sin((2 * d - m) * pi / 180.0) +
            0.658 * sin(2 * d * pi / 180.0) +
            0.214 * sin(2 * m * pi / 180.0) -
            0.186 * sin(ms * pi / 180.0);
        return lon % 360.0;
      default:
        return 0.0;
    }

    // Convert Keplarian elements to 3D Cartesian Heliocentric Coordinates
    double m = (L - w) % 360.0;
    double mRad = m * pi / 180.0;
    
    // Kepler equation solver: E - e*sin(E) = M
    double eccentricAnomaly = mRad;
    for (int i = 0; i < 5; i++) {
      eccentricAnomaly = eccentricAnomaly - (eccentricAnomaly - e * sin(eccentricAnomaly) - mRad) / (1.0 - e * cos(eccentricAnomaly));
    }

    // Coordinates in orbital plane
    double xOrb = a * (cos(eccentricAnomaly) - e);
    double yOrb = a * sqrt(1.0 - e * e) * sin(eccentricAnomaly);

    // Coordinate transformation to Ecliptic 3D
    double wRad = (w - omega) * pi / 180.0;
    double omegaRad = omega * pi / 180.0;
    double iRad = I * pi / 180.0;

    double cosW = cos(wRad);
    double sinW = sin(wRad);
    double cosO = cos(omegaRad);
    double sinO = sin(omegaRad);
    double cosI = cos(iRad);
    double sinI = sin(iRad);

    double xEcl = xOrb * (cosW * cosO - sinW * sinO * cosI) - yOrb * (sinW * cosO + cosW * sinO * cosI);
    double yEcl = xOrb * (cosW * sinO + sinW * cosO * cosI) - yOrb * (sinW * sinO - cosW * cosO * cosI);
    double zEcl = xOrb * (sinW * sinI) + yOrb * (cosW * sinI);

    // Compute Earth coordinates to convert to Geocentric
    double eM = (280.46646 + 36000.76983 * t - (282.93735 + 0.32242 * t)) % 360.0;
    double eMRad = eM * pi / 180.0;
    double eE = 0.01671022 - 0.00003804 * t;
    double eEcc = eMRad;
    for (int i = 0; i < 5; i++) {
      eEcc = eEcc - (eEcc - eE * sin(eEcc) - eMRad) / (1.0 - eE * cos(eEcc));
    }
    double earthX = 1.00000011 * (cos(eEcc) - eE);
    double earthY = 1.00000011 * sqrt(1.0 - eE * eE) * sin(eEcc);
    
    // Earth's perihelion longitude
    double earthW = (282.93735 + 0.32242 * t) * pi / 180.0;
    double xEarthEcl = earthX * cos(earthW) - earthY * sin(earthW);
    double yEarthEcl = earthX * sin(earthW) + earthY * cos(earthW);

    // Geocentric coordinates of the planet
    double geoX = xEcl - xEarthEcl;
    double geoY = yEcl - yEarthEcl;

    double geoLonRad = atan2(geoY, geoX);
    double geoLonDeg = geoLonRad * 180.0 / pi;
    return (geoLonDeg + 360.0) % 360.0;
  }

  // Get Sidereal Planetary Longitudes
  static Map<String, double> getPlanetaryPositions(double jd) {
    double ayanamsa = calculateLahiriAyanamsa(jd);
    Map<String, double> positions = {};

    List<String> physicalPlanets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];
    for (var planet in physicalPlanets) {
      double tropical = _calculatePlanetTropical(jd, planet);
      positions[planet] = (tropical - ayanamsa + 360.0) % 360.0;
    }

    // Rahu (Mean Moon's Node)
    double t = (jd - 2451545.0) / 36525.0;
    double rahuTropical = 125.04452 - 1934.13626 * t; // Node regresses
    positions["Rahu"] = (rahuTropical - ayanamsa + 360.0) % 360.0;

    // Ketu (Opposite node)
    positions["Ketu"] = (positions["Rahu"]! + 180.0) % 360.0;

    return positions;
  }

  // Calculate divisional charts (D1, D9, D10)
  // Returns sign index (0-11) for the planet in the given Varga (Divisional chart)
  static int getVargaSign(double longitude, String varga) {
    int baseSign = (longitude / 30.0).floor();
    double degreeInSign = longitude % 30.0;

    if (varga == "D1") {
      return baseSign;
    } else if (varga == "D9") {
      // D9 (Navamsa): Each sign is split into 9 parts of 3d 20m
      int navamsaPart = (degreeInSign / (30.0 / 9.0)).floor();
      // Navamsa starts from Aries for Fire signs, Capricorn for Earth, Libra for Air, Cancer for Water
      int startSign = 0;
      int element = baseSign % 4; // 0: Fire, 1: Earth, 2: Air, 3: Water
      if (element == 0) startSign = 0; // Aries (Mesha)
      if (element == 1) startSign = 9; // Capricorn (Makara)
      if (element == 2) startSign = 6; // Libra (Tula)
      if (element == 3) startSign = 3; // Cancer (Karka)
      
      return (startSign + navamsaPart) % 12;
    } else if (varga == "D10") {
      // D10 (Dasamsa): Each sign is split into 10 parts of 3d
      int dasamsaPart = (degreeInSign / 3.0).floor();
      // Dasamsa starts from same sign if Odd, or 9th sign away if Even
      bool isOdd = (baseSign % 2) == 0; // 0-indexed: 0 (Aries) is Odd sign 1, 1 (Taurus) is Even sign 2
      int startSign = isOdd ? baseSign : (baseSign + 8) % 12;
      return (startSign + dasamsaPart) % 12;
    }
    return baseSign;
  }

  // Get Chart Data Model (Planets and Lagna mapped to Signs and Houses)
  static Map<String, dynamic> generateKundliData(double jd, double latitude, double longitude) {
    double lagna = calculateLagna(jd, latitude, longitude);
    Map<String, double> planetPositions = getPlanetaryPositions(jd);
    
    // Complete map with Lagna
    Map<String, double> allPositions = {"Lagna": lagna, ...planetPositions};

    // Calculate D1, D9, D10 placements
    Map<String, List<Map<String, dynamic>>> vargas = {
      "D1": [],
      "D9": [],
      "D10": [],
    };

    // Lagna sign in D1
    int lagnaD1Sign = (lagna / 30.0).floor();

    for (var entry in allPositions.entries) {
      double lon = entry.value;
      
      // Calculate placements
      int d1Sign = getVargaSign(lon, "D1");
      int d9Sign = getVargaSign(lon, "D9");
      int d10Sign = getVargaSign(lon, "D10");

      // Calculate Houses relative to Lagna in D1
      // Lagna is always House 1 in D1 Rasi chart
      int d1House = (d1Sign - lagnaD1Sign + 12) % 12 + 1;

      vargas["D1"]!.add({
        "name": entry.key,
        "longitude": lon,
        "sign": d1Sign,
        "house": d1House,
        "formatted": "${(lon % 30.0).toStringAsFixed(2)}° ${signNamesEN[d1Sign]}"
      });

      vargas["D9"]!.add({
        "name": entry.key,
        "longitude": lon,
        "sign": d9Sign,
        "house": (d9Sign - getVargaSign(lagna, "D9") + 12) % 12 + 1,
      });

      vargas["D10"]!.add({
        "name": entry.key,
        "longitude": lon,
        "sign": d10Sign,
        "house": (d10Sign - getVargaSign(lagna, "D10") + 12) % 12 + 1,
      });
    }

    // Determine Yogas and Doshas
    List<String> yogas = [];
    List<String> doshas = [];

    // Simple Vedic checks:
    // 1. Manglik Dosha: Mars in 1st, 4th, 7th, 8th, or 12th house in D1
    var marsPlacment = vargas["D1"]!.firstWhere((p) => p["name"] == "Mars");
    int marsHouse = marsPlacment["house"];
    if ([1, 4, 7, 8, 12].contains(marsHouse)) {
      doshas.add("Manglik Dosha (Kuja Dosha) detected. Mars is in house $marsHouse.");
    } else {
      yogas.add("No Kuja Dosha (Non-Manglik). Mars is favorably placed.");
    }

    // 2. Gajakesari Yoga: Jupiter in Kendras (1, 4, 7, 10) from Moon
    var jupiterHouse = vargas["D1"]!.firstWhere((p) => p["name"] == "Jupiter")["house"];
    var moonHouse = vargas["D1"]!.firstWhere((p) => p["name"] == "Moon")["house"];
    int diffMoonJup = (jupiterHouse - moonHouse + 12) % 12 + 1;
    if ([1, 4, 7, 10].contains(diffMoonJup)) {
      yogas.add("Gajakesari Yoga: Jupiter is in a angular house (${diffMoonJup}) from the Moon, granting wisdom and wealth.");
    }

    // 3. Budhaditya Yoga: Sun and Mercury in the same house
    var sunSign = vargas["D1"]!.firstWhere((p) => p["name"] == "Sun")["sign"];
    var mercurySign = vargas["D1"]!.firstWhere((p) => p["name"] == "Mercury")["sign"];
    if (sunSign == mercurySign) {
      yogas.add("Budhaditya Yoga: Sun and Mercury are conjunct in ${signNamesEN[sunSign]}, promoting intelligence and status.");
    }

    return {
      "jd": jd,
      "ayanamsa": calculateLahiriAyanamsa(jd),
      "vargas": vargas,
      "yogas": yogas,
      "doshas": doshas
    };
  }

  // Calculate Panchang Elements
  static Map<String, dynamic> calculatePanchang(double jd, double latitude, double longitude) {
    Map<String, double> planets = getPlanetaryPositions(jd);
    double sunLon = planets["Sun"]!;
    double moonLon = planets["Moon"]!;

    // 1. Nakshatra (based on Moon's longitude: 360 / 27 = 13.333 degrees each)
    double nakDegree = 360.0 / 27.0;
    int nakIdx = (moonLon / nakDegree).floor();
    double nakProgress = (moonLon % nakDegree) / nakDegree * 100.0;

    // 2. Tithi (lunar phase: difference between Moon and Sun longitude: 360 / 30 = 12 degrees each)
    double diff = (moonLon - sunLon + 360.0) % 360.0;
    int tithiIdx = (diff / 12.0).floor();
    double tithiProgress = (diff % 12.0) / 12.0 * 100.0;
    String paksha = (tithiIdx < 15) ? "Shukla (Waxing)" : "Krishna (Waning)";

    // 3. Yoga (sum of Sun and Moon longitude: 360 / 27 = 13.333 degrees each)
    double yogaLon = (sunLon + moonLon) % 360.0;
    int yogaIdx = (yogaLon / nakDegree).floor();

    // 4. Karana (half of a Tithi: 6 degrees each)
    // Tithi 1 start is Karana 11 (Kintughna). Standard Karana calculation:
    int karanaIdx;
    if (diff < 6) {
      karanaIdx = 10; // Kintughna
    } else if (diff >= 354) {
      karanaIdx = 7; // Shakuni
    } else if (diff >= 348) {
      karanaIdx = 8; // Chatushpada
    } else if (diff >= 342) {
      karanaIdx = 9; // Naga
    } else {
      // General movable Karanas (Bava, Balava, etc.)
      int kVal = ((diff - 6) / 6).floor() % 7;
      karanaIdx = kVal;
    }

    // 5. Vara (Weekday)
    // Julian Day 0 is Monday. Let's calculate day of week
    int dayOfWeekIdx = ((jd + 1.5).floor() % 7);
    List<String> weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    List<String> weekdaysHI = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"];

    return {
      "nakshatra": nakshatrasEN[nakIdx],
      "nakshatraHI": nakshatrasHI[nakIdx],
      "nakshatraProgress": nakProgress,
      "tithi": tithisEN[tithiIdx],
      "tithiIdx": tithiIdx,
      "paksha": paksha,
      "tithiProgress": tithiProgress,
      "yoga": yogasEN[yogaIdx],
      "karana": karanasEN[karanaIdx],
      "vara": weekdays[dayOfWeekIdx],
      "varaHI": weekdaysHI[dayOfWeekIdx]
    };
  }

  // Ashta Koota Compatibility (36 Gunas Matching Score)
  // Based on Moon Signs and Moon Nakshatras of Bride (Female) & Groom (Male)
  static Map<String, dynamic> calculateAshtaKoota(
      double femaleMoonLon, double maleMoonLon) {
    int fSign = (femaleMoonLon / 30.0).floor();
    int mSign = (maleMoonLon / 30.0).floor();
    int fNak = (femaleMoonLon / (360.0 / 27.0)).floor();
    int mNak = (maleMoonLon / (360.0 / 27.0)).floor();

    double score = 0.0;
    List<String> breakdown = [];

    // 1. Varna Koota (1 point) - Work compatibility (class based on Rashi)
    int fVarna = _getVarna(fSign);
    int mVarna = _getVarna(mSign);
    double varnaScore = (fVarna >= mVarna) ? 1.0 : 0.0;
    score += varnaScore;
    breakdown.add("Varna Koota: $varnaScore / 1.0 (${varnaScore > 0 ? 'Excellent' : 'Average'})");

    // 2. Vashya Koota (2 points) - Mutual attraction / control
    double vashyaScore = _getVashyaScore(fSign, mSign);
    score += vashyaScore;
    breakdown.add("Vashya Koota: $vashyaScore / 2.0");

    // 3. Tara Koota (3 points) - Health & longevity (Nakshatra relative distance)
    double taraScore = _getTaraScore(fNak, mNak);
    score += taraScore;
    breakdown.add("Tara Koota: $taraScore / 3.0");

    // 4. Yoni Koota (4 points) - Physical / intimacy compatibility (based on animal yoni)
    double yoniScore = _getYoniScore(fNak, mNak);
    score += yoniScore;
    breakdown.add("Yoni Koota: $yoniScore / 4.0");

    // 5. Maitri Koota (5 points) - Friendship / Lord relationship
    double maitriScore = _getMaitriScore(fSign, mSign);
    score += maitriScore;
    breakdown.add("Maitri Koota: $maitriScore / 5.0");

    // 6. Gana Koota (6 points) - Temperament (Deva, Manushya, Rakshasa)
    double ganaScore = _getGanaScore(fNak, mNak);
    score += ganaScore;
    breakdown.add("Gana Koota: $ganaScore / 6.0");

    // 7. Bhakoot Koota (7 points) - Family & children (Rashi relative position)
    double bhakootScore = _getBhakootScore(fSign, mSign);
    score += bhakootScore;
    breakdown.add("Bhakoot Koota: $bhakootScore / 7.0");

    // 8. Nadi Koota (8 points) - Health / genetic compatibility
    double nadiScore = _getNadiScore(fNak, mNak);
    score += nadiScore;
    breakdown.add("Nadi Koota: $nadiScore / 8.0");

    String resultText;
    if (score >= 18) {
      resultText = "Compatible (Match is recommended. Gunas matched: ${score.toStringAsFixed(1)}/36)";
    } else {
      resultText = "Incompatible (Match not recommended without remedies. Gunas matched: ${score.toStringAsFixed(1)}/36)";
    }

    return {
      "score": score,
      "breakdown": breakdown,
      "result": resultText
    };
  }

  // Varna helper (0: Shudra, 1: Vaishya, 2: Kshatriya, 3: Brahmin)
  static int _getVarna(int rashi) {
    if ([3, 7, 11].contains(rashi)) return 3; // Cancer, Scorpio, Pisces (Water) -> Brahmin
    if ([0, 4, 8].contains(rashi)) return 2;  // Aries, Leo, Sag (Fire) -> Kshatriya
    if ([1, 5, 9].contains(rashi)) return 1;  // Taurus, Virgo, Cap (Earth) -> Vaishya
    return 0; // Gemini, Libra, Aqu (Air) -> Shudra
  }

  static double _getVashyaScore(int fSign, int mSign) {
    // Simplified Vashya score based on compatibility categories
    if (fSign == mSign) return 2.0;
    if ((fSign - mSign).abs() == 6) return 0.0;
    return 1.0;
  }

  static double _getTaraScore(int fNak, int mNak) {
    int diff1 = (mNak - fNak + 27) % 9;
    int diff2 = (fNak - mNak + 27) % 9;
    if ([2, 4, 6, 8, 0].contains(diff1) && [2, 4, 6, 8, 0].contains(diff2)) return 3.0;
    if ([2, 4, 6, 8, 0].contains(diff1) || [2, 4, 6, 8, 0].contains(diff2)) return 1.5;
    return 0.0;
  }

  static double _getYoniScore(int fNak, int mNak) {
    // Nakshatras animal yoni associations: Horse, Elephant, Sheep, Serpent, Dog, Cat, Rat, Cow, Buffalo, Tiger, Hare, Monkey, Lion, Mongoose
    int fYoni = fNak % 14;
    int mYoni = mNak % 14;
    if (fYoni == mYoni) return 4.0;
    // Enemy pairs (e.g. Serpent-Mongoose, Cat-Rat)
    if ((fYoni - mYoni).abs() == 7) return 0.0;
    return 2.0;
  }

  static double _getMaitriScore(int fSign, int mSign) {
    // Planet relationships
    if (fSign == mSign) return 5.0;
    String fLord = rashiLordsEN[fSign];
    String mLord = rashiLordsEN[mSign];
    if (fLord == mLord) return 5.0;
    // Friends, Neutral, Enemies
    return 3.0;
  }

  static double _getGanaScore(int fNak, int mNak) {
    // 0: Deva, 1: Manushya, 2: Rakshasa
    List<int> devas = [0, 4, 5, 7, 12, 14, 16, 21, 26];
    List<int> manushyas = [1, 3, 10, 11, 19, 20, 24, 25, 6];
    
    int fGana = devas.contains(fNak) ? 0 : (manushyas.contains(fNak) ? 1 : 2);
    int mGana = devas.contains(mNak) ? 0 : (manushyas.contains(mNak) ? 1 : 2);

    if (fGana == mGana) return 6.0;
    if (fGana == 0 && mGana == 1) return 5.0;
    if (fGana == 1 && mGana == 0) return 5.0;
    if (fGana == 2 || mGana == 2) return 0.0; // Rakshasa clash
    return 1.0;
  }

  static double _getBhakootScore(int fSign, int mSign) {
    int diff = (mSign - fSign + 12) % 12 + 1;
    if ([1, 7, 3, 4, 10, 11].contains(diff)) return 7.0; // Auspicious distances: 1-1, 3-11, 4-10
    return 0.0; // Inauspicious: 2-12, 5-9, 6-8 (Shadastak)
  }

  static double _getNadiScore(int fNak, int mNak) {
    // Nadis: 0: Aadi (Vata), 1: Madhya (Pitta), 2: Antya (Kapha)
    int fNadi = fNak % 3;
    int mNadi = mNak % 3;
    if (fNadi != mNadi) return 8.0; // Best compatibility (different nadis)
    return 0.0; // Nadi Dosha (same Nadi)
  }

  // Numerology Calculator
  static Map<String, dynamic> calculateNumerology(String name, String dobString) {
    // Remove non-alphabetic characters
    String cleanName = name.toUpperCase().replaceAll(RegExp(r'[^A-Z]'), '');
    
    // Pythagorean values for letters
    // A/J/S=1, B/K/T=2, C/L/U=3, D/M/V=4, E/N/W=5, F/O/X=6, G/P/Y=7, H/Q/Z=8, I/R=9
    Map<String, int> values = {
      'A':1,'J':1,'S':1,
      'B':2,'K':2,'T':2,
      'C':3,'L':3,'U':3,
      'D':4,'M':4,'V':4,
      'E':5,'N':5,'W':5,
      'F':6,'O':6,'X':6,
      'G':7,'P':7,'Y':7,
      'H':8,'Q':8,'Z':8,
      'I':9,'R':9
    };

    int nameSum = 0;
    for (int i = 0; i < cleanName.length; i++) {
      nameSum += values[cleanName[i]] ?? 0;
    }
    int destinyNumber = _reduceNumber(nameSum);

    // Calculate Life Path Number from dobString (YYYY-MM-DD)
    int dobSum = 0;
    for (int i = 0; i < dobString.length; i++) {
      int? num = int.tryParse(dobString[i]);
      if (num != null) dobSum += num;
    }
    int lifePathNumber = _reduceNumber(dobSum);

    // Soul Urge (sum of vowels in name)
    int vowelSum = 0;
    String vowels = "AEIOU";
    for (int i = 0; i < cleanName.length; i++) {
      if (vowels.contains(cleanName[i])) {
        vowelSum += values[cleanName[i]] ?? 0;
      }
    }
    int soulUrgeNumber = _reduceNumber(vowelSum);

    // Numerological characteristics descriptions
    Map<int, String> descriptions = {
      1: "The Leader. Ambitious, independent, pioneering, and assertive.",
      2: "The Peacemaker. Diplomatic, cooperative, sensitive, and harmonious.",
      3: "The Creative. Expressive, social, artistic, optimistic, and imaginative.",
      4: "The Builder. Practical, disciplined, steady, methodical, and honest.",
      5: "The Adventurer. Free-spirited, dynamic, versatile, and adaptable.",
      6: "The Nurturer. Responsible, loving, sympathetic, protective, and family-oriented.",
      7: "The Seeker. Analytical, intellectual, spiritual, meditative, and mysterious.",
      8: "The Executive. Powerful, ambitious, authoritative, material-focused, and organized.",
      9: "The Humanitarian. Compassionate, generous, idealistic, and creative."
    };

    return {
      "lifePath": lifePathNumber,
      "destiny": destinyNumber,
      "soulUrge": soulUrgeNumber,
      "lifePathDesc": descriptions[lifePathNumber] ?? "Dynamic vibration.",
      "destinyDesc": descriptions[destinyNumber] ?? "Creative purpose.",
      "soulUrgeDesc": descriptions[soulUrgeNumber] ?? "Heart's deep calling."
    };
  }

  static int _reduceNumber(int num) {
    while (num > 9) {
      // Don't reduce master numbers 11, 22 if you want to support them,
      // but standard single-digit reduction is typical for general numerology
      int temp = 0;
      while (num > 0) {
        temp += num % 10;
        num = (num / 10).floor();
      }
      num = temp;
    }
    return num;
  }
}
