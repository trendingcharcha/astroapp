with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. Ask AI Assistant pill on Home Dashboard header", b"Ask AI Assistant" in content),
    ("2. toggleVoiceInput speech recognition function exists", b"function toggleVoiceInput()" in content),
    ("3. Feedback topic filter tags present", b"fb-tag-btn" in content),
    ("4. downloadKundliPDF high-resolution preparation toast", b"Preparing High-Resolution B&W PDF Report" in content),
    ("5. checkKarmicStreakShield 7-day streak shield active", b"checkKarmicStreakShield()" in content and b"Shield Active" in content),
    ("6. scheduleNativeLocalNotifications schedules 1-day prior fast prep alerts", b"1-Day Prior Fast Preparation Alert" in content),
    ("7. FlutterNotificationBridge channel exposed", b"window.FlutterNotificationBridge" in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL SYSTEM ENHANCEMENTS PASSED!" if all_pass else "SOME CHECKS FAILED"))
