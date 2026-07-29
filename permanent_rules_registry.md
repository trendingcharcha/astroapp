# Astro AI App — Permanent Operational Rules & Directives

> [!IMPORTANT]
> These core directives are permanently locked into the operational workflow and must be enforced strictly across all present and future modifications without exception.

---

### Rule 1: 100% Dynamic & Authentic Astrology Calculations (Zero Dummy Data)
- **Zero Static Fallbacks**: Every prediction, remedy, Vastu direction, Lal Kitab Teva analysis, Coach Mission, Guna Milan score, and notification MUST be dynamically computed from the user's actual birth details (`user_name`, `user_dob`, `user_tob`, `user_pob`, `cachedPlacementsList`, `cachedLagnaSignNum`).
- **No `new Date()` Fallback for Birth Data**: Malformed date/time inputs must trigger an explicit user error and abort chart generation rather than silently falling back to today's date.
- **Pure Astronomical Math**: Kundli calculations must use Julian Day (JD), Lahiri Ayanamsa, and Keplerian planetary elements.

---

### Rule 2: Absolute API & Integration Preservation
- **Never Disturb Backend / APIs**: Do not alter, break, or remove existing Supabase integrations, OAuth listeners, database schemas (`public.profiles`, `public.feedbacks`), RLS policies, or core app architecture.
- **LocalStorage Schema Integrity**: Maintain consistent keys (`user_name`, `user_dob`, `user_tob`, `user_pob`, `user_gender`, `user_goal`, `app_language`, `karma_plan_start_date`, `user_xp`, `user_streak`) across all modules.

---

### Rule 3: Instant 100% Language Synchronization (No Page Refresh)
- Switching language (English ↔ Hindi) via any button or dropdown MUST immediately re-render all active screens, dynamic reports (Coach Mission, Kundli Enhanced Sections, Lal Kitab Report, Vastu Guidance), forms, selects, and notification cards without requiring a browser refresh.

---

### Rule 4: 100% Verification & Empirical Accuracy
- Never declare a task complete without executing syntax checks and verification scripts across all 7 tabs (Home, Kundli, Lal Kitab, Matching, Vastu, Coach, Settings) and the Notification Drawer.
- Fix all root causes at the source rather than applying superficial symptom patches.

---

### Rule 5: Premium Vedic Astro Aesthetics (No Emojis)
- Maintain clean, golden (`#E8C879`), purple (`#9B86ED`), and dark cosmic theme styling (`#0C0922`).
- Use glowing SVG icons for UI elements instead of emojis.
- Keep tone professional, sacred, authentic, and strictly focused on Vedic astrology.

---

### Rule 6: Mandatory User Feedback & Adaptive Live AI Task-Adapter Engine
- **Mandatory Feedback System**: Settings tab MUST contain the `openFeedbackModal()` form with mandatory fields (`full_name`, `email`, `phone`, `profession`, `rating`) synced directly to Supabase Cloud `public.feedbacks` database table.
- **Adaptive Task Negotiation**: Settings tab MUST contain `openLiveChatModal()`. When users are busy at work or miss a time window, the Live AI Assistant generates valid Sattvic office/desk alternatives with an interactive `[ ACCEPT & UPDATE TODAY'S TASK ]` button that updates the Home tab active tasks in real-time.
- **Header Navigation**: Both Feedback and Live Chat modals MUST feature prominent, accessible `← BACK` navigation buttons at top-left.

---

### Rule 7: Single Universal Supabase Cloud Backend (`https://doxskublvyyosrmecxic.supabase.co`)
- Single cloud database instance for all platforms (PC, Web URL, Mobile APK).

---

### Rule 8: Flutter Exclusive Mobile Packaging Engine
- **Flutter Only**: Flutter (`lib/main.dart`, `pubspec.yaml`, `android/`) is the sole, permanent standard for all Android APK (`.apk`) and App Bundle (`.aab`) release builds.
- **No Alternatives**: Never suggest, offer, or use any third-party alternative build tools or services (PWABuilder, TWA, external wrappers, etc.). All mobile builds must use Flutter exclusively.

