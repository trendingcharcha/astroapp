import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../providers/chart_provider.dart';
import 'kundli_result_screen.dart';

class KundliFormScreen extends ConsumerStatefulWidget {
  const KundliFormScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<KundliFormScreen> createState() => _KundliFormScreenState();
}

class _KundliFormScreenState extends ConsumerState<KundliFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _cityController = TextEditingController();

  DateTime _selectedDate = DateTime.now().subtract(const Duration(days: 365 * 25)); // Default age 25
  TimeOfDay _selectedTime = const TimeOfDay(hour: 12, minute: 0);
  
  double _latitude = 28.6139;
  double _longitude = 77.2090;
  double _timezone = 5.5;

  List<Map<String, dynamic>> _citySuggestions = [];

  @override
  void dispose() {
    _nameController.dispose();
    _cityController.dispose();
    super.dispose();
  }

  // Pick Date
  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(1930),
      lastDate: DateTime.now(),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.dark(
              primary: Color(0xFFE8C879),
              onPrimary: Color(0xFF14102C),
              surface: Color(0xFF14102C),
              onSurface: Colors.white,
            ),
          ),
          child: child!,
        );
      },
    );
    if (picked != null) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  // Pick Time
  Future<void> _pickTime() async {
    final picked = await showTimePicker(
      context: context,
      initialTime: _selectedTime,
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.dark(
              primary: Color(0xFFE8C879),
              onPrimary: Color(0xFF14102C),
              surface: Color(0xFF14102C),
              onSurface: Colors.white,
            ),
          ),
          child: child!,
        );
      },
    );
    if (picked != null) {
      setState(() {
        _selectedTime = picked;
      });
    }
  }

  // Filter city suggestions
  void _onCityChanged(String text) {
    if (text.isEmpty) {
      setState(() {
        _citySuggestions = [];
      });
      return;
    }
    
    final matches = CityLookup.majorCities.where((c) {
      return c["name"].toLowerCase().contains(text.toLowerCase());
    }).toList();

    setState(() {
      _citySuggestions = matches;
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(chartProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text("Create Kundli"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                "Enter birth details to map your planetary alignments",
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white70, fontSize: 14),
              ),
              const SizedBox(height: 30),

              // Name Input
              TextFormField(
                controller: _nameController,
                style: const TextStyle(color: Colors.white),
                decoration: const InputDecoration(
                  labelText: "Full Name",
                  prefixIcon: Icon(Icons.person_outline, color: Color(0xFFE8C879)),
                ),
                validator: (val) => val == null || val.isEmpty ? "Please enter a name" : null,
              ),
              const SizedBox(height: 20),

              // Date Picker Field
              InkWell(
                onTap: _pickDate,
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
                          const Text("Birth Date", style: TextStyle(color: Color(0xFFE8C879), fontSize: 12)),
                          const SizedBox(height: 4),
                          Text(
                            DateFormat('dd MMMM yyyy').format(_selectedDate),
                            style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                      const Icon(Icons.calendar_today, color: Color(0xFFE8C879)),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Time Picker Field
              InkWell(
                onTap: _pickTime,
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
                          const Text("Birth Time", style: TextStyle(color: Color(0xFFE8C879), fontSize: 12)),
                          const SizedBox(height: 4),
                          Text(
                            _selectedTime.format(context),
                            style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                      const Icon(Icons.access_time, color: Color(0xFFE8C879)),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // City Search
              TextFormField(
                controller: _cityController,
                onChanged: _onCityChanged,
                style: const TextStyle(color: Colors.white),
                decoration: const InputDecoration(
                  labelText: "Birth Place (City)",
                  prefixIcon: Icon(Icons.location_on_outlined, color: Color(0xFFE8C879)),
                  hintText: "Type city (e.g. New Delhi, New York)",
                ),
                validator: (val) => val == null || val.isEmpty ? "Please enter a location" : null,
              ),

              // Autocomplete suggestions list
              if (_citySuggestions.isNotEmpty)
                Container(
                  margin: const EdgeInsets.only(top: 8),
                  decoration: BoxDecoration(
                    color: const Color(0xFF14102C),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFF2A244E)),
                  ),
                  child: ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: _citySuggestions.length,
                    itemBuilder: (context, idx) {
                      final city = _citySuggestions[idx];
                      return ListTile(
                        title: Text(city["name"], style: const TextStyle(color: Colors.white)),
                        subtitle: Text(
                          "Lat: ${city['lat']} | Lng: ${city['lng']}",
                          style: const TextStyle(color: Colors.white54, fontSize: 11),
                        ),
                        onTap: () {
                          setState(() {
                            _cityController.text = city["name"];
                            _latitude = city["lat"];
                            _longitude = city["lng"];
                            _timezone = city["tz"];
                            _citySuggestions = [];
                          });
                        },
                      );
                    },
                  ),
                ),
              const SizedBox(height: 35),

              // Submit Button
              ElevatedButton(
                onPressed: state.isLoading
                    ? null
                    : () {
                        if (_formKey.currentState!.validate()) {
                          final details = BirthDetails(
                            name: _nameController.text,
                            date: _selectedDate,
                            timeString: "${_selectedTime.hour.toString().padLeft(2, '0')}:${_selectedTime.minute.toString().padLeft(2, '0')}",
                            cityName: _cityController.text,
                            latitude: _latitude,
                            longitude: _longitude,
                            timezoneOffset: _timezone,
                          );

                          ref.read(chartProvider.notifier).generateChart(details);
                          ref.read(chartProvider.notifier).saveCurrentChart(); // Auto-save to history

                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const KundliResultScreen(),
                            ),
                          );
                        }
                      },
                child: state.isLoading
                    ? const CircularProgressIndicator(color: Color(0xFF14102C))
                    : const Text("GENERATE KUNDLI"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
