import 'package:flutter/material.dart';
import '../services/supabase_service.dart';
import '../services/hive_service.dart';
import '../services/astro_engine.dart';
import 'home_dashboard.dart';
import 'package:shared_preferences/shared_preferences.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final _formKey = GlobalKey<FormState>();
  
  // Base fields
  final _nameController = TextEditingController();
  final _dobController = TextEditingController();
  final _tobController = TextEditingController();
  final _pobController = TextEditingController();
  final _professionController = TextEditingController();
  final _customIssueController = TextEditingController();
  
  String _gender = 'M';
  String _onboardingPath = 'single'; // 'single' or 'couple'
  String _goal = 'job'; // 'job', 'debt', 'marriage', 'baby', 'business', 'property', 'health', 'custom'

  // Property fields
  String _propertyNumber = '1st';
  String _propertyType = 'home';
  final _propertyCityController = TextEditingController();

  // Baby planning fields
  String _babyNumber = '1';
  final _firstBabyDobController = TextEditingController();
  final _firstBabyAgeController = TextEditingController();
  final _secondBabyAgeController = TextEditingController();

  // Partner fields
  bool _includePartner = false;
  final _partnerNameController = TextEditingController();
  final _partnerDobController = TextEditingController();
  final _partnerTobController = TextEditingController();
  final _partnerPobController = TextEditingController();
  String _partnerGender = 'F';

  bool _isLoading = false;

  Future<void> _selectDate(BuildContext context, TextEditingController controller) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now().subtract(const Duration(days: 9125)), // 25 years ago
      firstDate: DateTime(1920),
      lastDate: DateTime.now(),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.dark(
              primary: Color(0xFFE8C879),
              onPrimary: Colors.black,
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
        controller.text = "${picked.year}-${picked.month.toString().padLeft(2, '0')}-${picked.day.toString().padLeft(2, '0')}";
      });
    }
  }

  Future<void> _selectTime(BuildContext context, TextEditingController controller) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: const TimeOfDay(hour: 12, minute: 0),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.dark(
              primary: Color(0xFFE8C879),
              onPrimary: Colors.black,
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
        controller.text = "${picked.hour.toString().padLeft(2, '0')}:${picked.minute.toString().padLeft(2, '0')}";
      });
    }
  }

  Future<void> _submitOnboarding() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    final profileData = {
      'name': _nameController.text.trim(),
      'gender': _gender,
      'dob': _dobController.text,
      'tob': _tobController.text,
      'pob': _pobController.text.trim(),
      'onboarding_path': _onboardingPath,
      'goal': _goal,
      'profession': _professionController.text.trim(),
      'custom_issue': _goal == 'custom' ? _customIssueController.text.trim() : '',
      
      // Property details
      'property_number': _goal == 'property' ? _propertyNumber : '',
      'property_type': _goal == 'property' ? _propertyType : '',
      'property_city': _goal == 'property' ? _propertyCityController.text.trim() : '',

      // Baby planning details
      'baby_number': _goal == 'baby' ? _babyNumber : '',
      'first_baby_dob': (_goal == 'baby' && _babyNumber == '2') ? _firstBabyDobController.text : '',
      'first_baby_age': (_goal == 'baby' && _babyNumber == '3') ? _firstBabyAgeController.text : '',
      'second_baby_age': (_goal == 'baby' && _babyNumber == '3') ? _secondBabyAgeController.text : '',

      // Partner details
      'include_partner': _includePartner || _onboardingPath == 'couple',
      'partner_name': _partnerNameController.text.trim(),
      'partner_dob': _partnerDobController.text,
      'partner_tob': _partnerTobController.text,
      'partner_pob': _partnerPobController.text.trim(),
      'partner_gender': _partnerGender,
    };

    try {
      // Compute authentic Vedic Kundli for user
      int y = 1995, m = 1, d = 1, h = 12, min = 0;
      try {
        final dParts = _dobController.text.split(RegExp(r'[-/]'));
        if (dParts.length >= 3) {
          if (dParts[0].length == 4) {
            y = int.parse(dParts[0]); m = int.parse(dParts[1]); d = int.parse(dParts[2]);
          } else {
            y = int.parse(dParts[2]); m = int.parse(dParts[1]); d = int.parse(dParts[0]);
          }
        }
        final tParts = _tobController.text.split(':');
        if (tParts.length >= 2) {
          h = int.parse(tParts[0]); min = int.parse(tParts[1]);
        }
      } catch (_) {}

      final kundli = AstroEngine.calculateFullKundli(
        year: y,
        month: m,
        day: d,
        hour: h,
        min: min,
        goal: _goal,
      );

      profileData['lagna_name'] = kundli['lagnaName'];
      profileData['ruling_lord'] = kundli['rulingLord'];
      profileData['moon_sign_name'] = kundli['moonSignName'];
      profileData['moon_nakshatra'] = kundli['moonNakshatra'];
      profileData['goal_lord'] = kundli['goalLord'];

      // 1. Cache profile details in local Hive storage
      await HiveService.saveProfile(profileData);

      // 2. Sync to live cloud database if not guest
      if (SupabaseService.currentUser != null) {
        await SupabaseService.upsertFullProfile(profileData);
      }

      // 3. Update Shared Preferences onboarding flag
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool('has_completed_onboarding', true);

      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const HomeDashboard()),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error saving profile: $e")),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF09071A),
      appBar: AppBar(
        title: const Text('Spiritual Setup', style: TextStyle(color: Color(0xFFE8C879))),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Tell us your alignment to configure daily quests, Astro advice, and detailed Kundli.',
                style: TextStyle(color: Colors.grey, fontSize: 13),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),

              // Basic details section
              _buildSectionTitle('1. Personal Details'),
              _buildCard([
                _buildTextField(_nameController, 'Full Name', Icons.person_outline, required: true),
                const SizedBox(height: 16),
                _buildGenderToggle(),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(child: _buildDatePickerField(_dobController, 'Birth Date', context)),
                    const SizedBox(width: 12),
                    Expanded(child: _buildTimePickerField(_tobController, 'Birth Time', context)),
                  ],
                ),
                const SizedBox(height: 16),
                _buildTextField(_pobController, 'Birth Place (City)', Icons.location_on_outlined, required: true),
                const SizedBox(height: 16),
                _buildTextField(_professionController, 'Current Profession / Role', Icons.work_outline, required: true),
              ]),

              const SizedBox(height: 24),

              // Paths setup
              _buildSectionTitle('2. Select Path Mode'),
              _buildCard([
                Row(
                  children: [
                    Expanded(
                      child: _buildChoiceButton(
                        label: 'Single Path',
                        isSelected: _onboardingPath == 'single',
                        onTap: () => setState(() {
                          _onboardingPath = 'single';
                          if (_goal == 'baby') _goal = 'job'; // Baby planning strictly couple goal
                        }),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _buildChoiceButton(
                        label: 'Couple Path',
                        isSelected: _onboardingPath == 'couple',
                        onTap: () => setState(() {
                          _onboardingPath = 'couple';
                          _includePartner = true;
                        }),
                      ),
                    ),
                  ],
                ),
              ]),

              const SizedBox(height: 24),

              // Goal selection
              _buildSectionTitle('3. Your Major Goal'),
              _buildCard([
                DropdownButtonFormField<String>(
                  value: _goal,
                  dropdownColor: const Color(0xFF14102C),
                  style: const TextStyle(color: Colors.white),
                  decoration: InputDecoration(
                    labelText: 'Core Objective',
                    labelStyle: const TextStyle(color: Colors.grey),
                    prefixIcon: const Icon(Icons.stars, color: Color(0xFF8E6FD6)),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  items: [
                    const DropdownMenuItem(value: 'job', child: Text('Get Dream Job / Career')),
                    const DropdownMenuItem(value: 'debt', child: Text('Clear Financial Debt')),
                    const DropdownMenuItem(value: 'marriage', child: Text('Marriage / Relationship Harmony')),
                    if (_onboardingPath == 'couple')
                      const DropdownMenuItem(value: 'baby', child: Text('Baby Planning / Progeny')),
                    const DropdownMenuItem(value: 'business', child: Text('Start or Grow Business')),
                    const DropdownMenuItem(value: 'property', child: Text('Buy Home / Property')),
                    const DropdownMenuItem(value: 'health', child: Text('Improve Health / Fitness')),
                    const DropdownMenuItem(value: 'custom', child: Text('Resolve Specific Issue')),
                  ],
                  onChanged: (val) {
                    if (val != null) setState(() => _goal = val);
                  },
                ),
                
                // If Custom Goal
                if (_goal == 'custom') ...[
                  const SizedBox(height: 16),
                  _buildTextField(_customIssueController, 'Describe your issue (e.g. Visa delay, legal dispute)', Icons.edit_note, required: true),
                ],

                // If Property Goal
                if (_goal == 'property') ...[
                  const SizedBox(height: 16),
                  DropdownButtonFormField<String>(
                    value: _propertyNumber,
                    dropdownColor: const Color(0xFF14102C),
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      labelText: 'Which purchase is this?',
                      labelStyle: const TextStyle(color: Colors.grey),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    items: const [
                      DropdownMenuItem(value: '1st', child: Text('First Home / Property')),
                      DropdownMenuItem(value: '2nd', child: Text('Second Home / Property')),
                      DropdownMenuItem(value: '3rd+', child: Text('Third or More Property')),
                    ],
                    onChanged: (val) => setState(() => _propertyNumber = val ?? '1st'),
                  ),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<String>(
                    value: _propertyType,
                    dropdownColor: const Color(0xFF14102C),
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      labelText: 'Property Type',
                      labelStyle: const TextStyle(color: Colors.grey),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    items: const [
                      DropdownMenuItem(value: 'home', child: Text('Residential Home / Apartment')),
                      DropdownMenuItem(value: 'commercial', child: Text('Commercial Shop / Office')),
                      DropdownMenuItem(value: 'plot', child: Text('Empty Plot / Land')),
                    ],
                    onChanged: (val) => setState(() => _propertyType = val ?? 'home'),
                  ),
                  const SizedBox(height: 16),
                  _buildTextField(_propertyCityController, 'Purchase City Location', Icons.map_outlined, required: true),
                ],

                // If Baby Goal
                if (_goal == 'baby') ...[
                  const SizedBox(height: 16),
                  DropdownButtonFormField<String>(
                    value: _babyNumber,
                    dropdownColor: const Color(0xFF14102C),
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      labelText: 'Planning for baby number:',
                      labelStyle: const TextStyle(color: Colors.grey),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    items: const [
                      DropdownMenuItem(value: '1', child: Text('1st Baby')),
                      DropdownMenuItem(value: '2', child: Text('2nd Baby (Ask 1st baby DOB)')),
                      DropdownMenuItem(value: '3', child: Text('3rd Baby (Ask 1st & 2nd baby age)')),
                    ],
                    onChanged: (val) => setState(() => _babyNumber = val ?? '1'),
                  ),
                  if (_babyNumber == '2') ...[
                    const SizedBox(height: 16),
                    _buildDatePickerField(_firstBabyDobController, '1st Child Birth Date', context),
                  ],
                  if (_babyNumber == '3') ...[
                    const SizedBox(height: 16),
                    _buildTextField(_firstBabyAgeController, '1st Child Age (in years)', Icons.child_care, required: true, isNumber: true),
                    const SizedBox(height: 16),
                    _buildTextField(_secondBabyAgeController, '2nd Child Age (in years)', Icons.child_care, required: true, isNumber: true),
                  ],
                ],
              ]),

              const SizedBox(height: 24),

              // Optional partner integration (available for single path, forced for couple path)
              if (_onboardingPath == 'single') ...[
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('Include Partner Details?', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    Switch(
                      value: _includePartner,
                      activeColor: const Color(0xFFE8C879),
                      onChanged: (val) => setState(() => _includePartner = val),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
              ],

              if (_includePartner || _onboardingPath == 'couple') ...[
                _buildSectionTitle('4. Partner Birth Details'),
                _buildCard([
                  _buildTextField(_partnerNameController, 'Partner Name', Icons.favorite_border, required: true),
                  const SizedBox(height: 16),
                  _buildPartnerGenderToggle(),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(child: _buildDatePickerField(_partnerDobController, 'Partner Birth Date', context)),
                      const SizedBox(width: 12),
                      Expanded(child: _buildTimePickerField(_partnerTobController, 'Partner Birth Time', context)),
                    ],
                  ),
                  const SizedBox(height: 16),
                  _buildTextField(_partnerPobController, 'Partner Birth Place (City)', Icons.location_on_outlined, required: true),
                ]),
                const SizedBox(height: 24),
              ],

              // Submit onboarding
              ElevatedButton(
                onPressed: _isLoading ? null : _submitOnboarding,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFE8C879),
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: _isLoading 
                    ? const CircularProgressIndicator(color: Colors.black)
                    : const Text('ALIGN STARS & ENTER DASHBOARD', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // UI Helpers
  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10, left: 4),
      child: Text(
        title,
        style: const TextStyle(color: Color(0xFFE8C879), fontSize: 16, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _buildCard(List<Widget> children) {
    return Card(
      color: const Color(0xFF14102C),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: Color(0xFF2A244E)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: children,
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String label, IconData icon, {bool required = false, bool isNumber = false}) {
    return TextFormField(
      controller: controller,
      keyboardType: isNumber ? TextInputType.number : TextInputType.text,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(color: Colors.grey),
        prefixIcon: Icon(icon, color: const Color(0xFF8E6FD6)),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      ),
      validator: (val) {
        if (required && (val == null || val.trim().isEmpty)) {
          return "This field is required.";
        }
        return null;
      },
    );
  }

  Widget _buildDatePickerField(TextEditingController controller, String label, BuildContext context) {
    return TextFormField(
      controller: controller,
      readOnly: true,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(color: Colors.grey),
        prefixIcon: const Icon(Icons.calendar_month, color: Color(0xFF8E6FD6)),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      ),
      onTap: () => _selectDate(context, controller),
      validator: (val) => (val == null || val.isEmpty) ? "Required" : null,
    );
  }

  Widget _buildTimePickerField(TextEditingController controller, String label, BuildContext context) {
    return TextFormField(
      controller: controller,
      readOnly: true,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(color: Colors.grey),
        prefixIcon: const Icon(Icons.access_time, color: Color(0xFF8E6FD6)),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      ),
      onTap: () => _selectTime(context, controller),
      validator: (val) => (val == null || val.isEmpty) ? "Required" : null,
    );
  }

  Widget _buildGenderToggle() {
    return Row(
      children: [
        const Text('Gender: ', style: TextStyle(color: Colors.grey)),
        const SizedBox(width: 12),
        _buildGenderChoice('Male', 'M'),
        const SizedBox(width: 8),
        _buildGenderChoice('Female', 'F'),
        const SizedBox(width: 8),
        _buildGenderChoice('Other', 'O'),
      ],
    );
  }

  Widget _buildGenderChoice(String label, String value) {
    final isSelected = _gender == value;
    return ChoiceChip(
      label: Text(label, style: TextStyle(color: isSelected ? Colors.black : Colors.white)),
      selected: isSelected,
      selectedColor: const Color(0xFFE8C879),
      backgroundColor: const Color(0xFF09071A),
      onSelected: (selected) {
        if (selected) setState(() => _gender = value);
      },
    );
  }

  Widget _buildPartnerGenderToggle() {
    return Row(
      children: [
        const Text('Partner Gender: ', style: TextStyle(color: Colors.grey)),
        const SizedBox(width: 12),
        _buildPartnerGenderChoice('Male', 'M'),
        const SizedBox(width: 8),
        _buildPartnerGenderChoice('Female', 'F'),
        const SizedBox(width: 8),
        _buildPartnerGenderChoice('Other', 'O'),
      ],
    );
  }

  Widget _buildPartnerGenderChoice(String label, String value) {
    final isSelected = _partnerGender == value;
    return ChoiceChip(
      label: Text(label, style: TextStyle(color: isSelected ? Colors.black : Colors.white)),
      selected: isSelected,
      selectedColor: const Color(0xFFE8C879),
      backgroundColor: const Color(0xFF09071A),
      onSelected: (selected) {
        if (selected) setState(() => _partnerGender = value);
      },
    );
  }

  Widget _buildChoiceButton({required String label, required bool isSelected, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFF8E6FD6).withOpacity(0.15) : Colors.transparent,
          border: Border.all(color: isSelected ? const Color(0xFF8E6FD6) : const Color(0xFF2A244E)),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(
          label,
          textAlign: TextAlign.center,
          style: TextStyle(
            color: isSelected ? const Color(0xFFE8C879) : Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    _dobController.dispose();
    _tobController.dispose();
    _pobController.dispose();
    _professionController.dispose();
    _customIssueController.dispose();
    _propertyCityController.dispose();
    _firstBabyDobController.dispose();
    _firstBabyAgeController.dispose();
    _secondBabyAgeController.dispose();
    _partnerNameController.dispose();
    _partnerDobController.dispose();
    _partnerTobController.dispose();
    _partnerPobController.dispose();
    super.dispose();
  }
}
