import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../core/astrology/astrology_engine.dart';

// Model representing Birth Details
class BirthDetails {
  final String name;
  final DateTime date;
  final String timeString; // "HH:MM"
  final String cityName;
  final double latitude;
  final double longitude;
  final double timezoneOffset;

  BirthDetails({
    required this.name,
    required this.date,
    required this.timeString,
    required this.cityName,
    required this.latitude,
    required this.longitude,
    required this.timezoneOffset,
  });

  BirthDetails copyWith({
    String? name,
    DateTime? date,
    String? timeString,
    String? cityName,
    double? latitude,
    double? longitude,
    double? timezoneOffset,
  }) {
    return BirthDetails(
      name: name ?? this.name,
      date: date ?? this.date,
      timeString: timeString ?? this.timeString,
      cityName: cityName ?? this.cityName,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      timezoneOffset: timezoneOffset ?? this.timezoneOffset,
    );
  }
}

// Model representing a Saved Chart
class SavedChart {
  final String id;
  final String name;
  final String dateTime;
  final String location;
  final Map<String, dynamic> data;

  SavedChart({
    required this.id,
    required this.name,
    required this.dateTime,
    required this.location,
    required this.data,
  });
}

// Local Database of major cities for offline autocomplete & coordinate lookup
class CityLookup {
  static const List<Map<String, dynamic>> majorCities = [
    {"name": "New Delhi, India", "lat": 28.6139, "lng": 77.2090, "tz": 5.5},
    {"name": "Mumbai, India", "lat": 19.0760, "lng": 72.8777, "tz": 5.5},
    {"name": "Bengaluru, India", "lat": 12.9716, "lng": 77.5946, "tz": 5.5},
    {"name": "Kolkata, India", "lat": 22.5726, "lng": 88.3639, "tz": 5.5},
    {"name": "Chennai, India", "lat": 13.0827, "lng": 80.2707, "tz": 5.5},
    {"name": "Hyderabad, India", "lat": 17.3850, "lng": 78.4867, "tz": 5.5},
    {"name": "Pune, India", "lat": 18.5204, "lng": 73.8567, "tz": 5.5},
    {"name": "Ahmedabad, India", "lat": 23.0225, "lng": 72.5714, "tz": 5.5},
    {"name": "Jaipur, India", "lat": 26.9124, "lng": 75.7873, "tz": 5.5},
    {"name": "New York, USA", "lat": 40.7128, "lng": -74.0060, "tz": -5.0},
    {"name": "London, UK", "lat": 51.5074, "lng": -0.1278, "tz": 0.0},
    {"name": "Dubai, UAE", "lat": 25.2048, "lng": 55.2708, "tz": 4.0},
    {"name": "Singapore", "lat": 1.3521, "lng": 103.8198, "tz": 8.0},
    {"name": "Sydney, Australia", "lat": -33.8688, "lng": 151.2093, "tz": 10.0},
  ];

  static Map<String, dynamic> lookup(String query) {
    String cleanQuery = query.toLowerCase().trim();
    for (var city in majorCities) {
      if (city["name"].toLowerCase().contains(cleanQuery)) {
        return city;
      }
    }
    // Default to New Delhi if not found
    return {"name": "$query (Estimated)", "lat": 28.6139, "lng": 77.2090, "tz": 5.5};
  }
}

// State class for Chart calculations
class ChartState {
  final BirthDetails? currentBirthDetails;
  final Map<String, dynamic>? calculatedChartData;
  final Map<String, dynamic>? calculatedPanchang;
  final List<SavedChart> savedCharts;
  final bool isLoading;

  ChartState({
    this.currentBirthDetails,
    this.calculatedChartData,
    this.calculatedPanchang,
    this.savedCharts = const [],
    this.isLoading = false,
  });

  ChartState copyWith({
    BirthDetails? currentBirthDetails,
    Map<String, dynamic>? calculatedChartData,
    Map<String, dynamic>? calculatedPanchang,
    List<SavedChart>? savedCharts,
    bool? isLoading,
  }) {
    return ChartState(
      currentBirthDetails: currentBirthDetails ?? this.currentBirthDetails,
      calculatedChartData: calculatedChartData ?? this.calculatedChartData,
      calculatedPanchang: calculatedPanchang ?? this.calculatedPanchang,
      savedCharts: savedCharts ?? this.savedCharts,
      isLoading: isLoading ?? this.isLoading,
    );
  }
}

// ChartNotifier to calculate charts and store history
class ChartNotifier extends StateNotifier<ChartState> {
  ChartNotifier() : super(ChartState());

  // Calculates a new Kundli chart
  void generateChart(BirthDetails details) {
    state = state.copyWith(isLoading: true);

    // Parse time
    List<String> timeParts = details.timeString.split(":");
    int hour = int.parse(timeParts[0]);
    int minute = int.parse(timeParts[1]);

    // Calculate Julian Day
    double jd = AstrologyEngine.calculateJulianDay(
      details.date.year,
      details.date.month,
      details.date.day,
      hour,
      minute,
      0,
      details.timezoneOffset,
    );

    // Run calculations
    Map<String, dynamic> chartData = AstrologyEngine.generateKundliData(jd, details.latitude, details.longitude);
    Map<String, dynamic> panchang = AstrologyEngine.calculatePanchang(jd, details.latitude, details.longitude);

    state = state.copyWith(
      currentBirthDetails: details,
      calculatedChartData: chartData,
      calculatedPanchang: panchang,
      isLoading: false,
    );
  }

  // Save current chart to history list and sync to Supabase in the background
  void saveCurrentChart() async {
    if (state.currentBirthDetails == null || state.calculatedChartData == null) return;

    final details = state.currentBirthDetails!;
    final newChart = SavedChart(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: details.name,
      dateTime: "${details.date.toIso8601String().split('T')[0]} ${details.timeString}",
      location: details.cityName,
      data: state.calculatedChartData!,
    );

    state = state.copyWith(
      savedCharts: [...state.savedCharts, newChart],
    );

    // Sync to Supabase cloud database
    try {
      final supabase = Supabase.instance.client;
      await supabase.from('charts').insert({
        'id': newChart.id,
        'name': newChart.name,
        'date_time': newChart.dateTime,
        'location': newChart.location,
        'data': newChart.data,
      });
    } catch (e) {
      // Local fallback: ignore sync errors and log it
      print("Supabase cloud sync failed (running in local offline mode): $e");
    }
  }

  void deleteChart(String id) async {
    state = state.copyWith(
      savedCharts: state.savedCharts.where((c) => c.id != id).toList(),
    );

    // Delete from Supabase in the background
    try {
      final supabase = Supabase.instance.client;
      await supabase.from('charts').delete().eq('id', id);
    } catch (e) {
      print("Supabase delete sync failed: $e");
    }
  }
}

// Riverpod Provider
final chartProvider = StateNotifierProvider<ChartNotifier, ChartState>((ref) {
  return ChartNotifier();
});
