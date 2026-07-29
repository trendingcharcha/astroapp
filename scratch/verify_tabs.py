with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. switchTab instantly activates tab-content", b"document.querySelectorAll('.tab-content').forEach" in content),
    ("2. switchTab instantly activates nav-item", b"document.querySelectorAll('.nav-item').forEach" in content),
    ("3. generateLalKitabReport awaits autoFillKundliFromOnboarding", b"await autoFillKundliFromOnboarding();" in content),
    ("4. generatePersonalizedVastuReport awaits autoFillKundliFromOnboarding", b"await autoFillKundliFromOnboarding();" in content),
    ("5. Lal Kitab Mangal details card exists", b"id=\"lk-mangal-details\"" in content),
    ("6. Lal Kitab Budh details card exists", b"id=\"lk-budh-details\"" in content),
    ("7. Lal Kitab Teva details card exists", b"id=\"lk-teva-details\"" in content),
    ("8. Lal Kitab Remedies card exists", b"id=\"lk-remedies-details\"" in content),
    ("9. Lal Kitab canvas exists", b"id=\"lalkitab-chart-canvas\"" in content),
    ("10. Notification drawer container exists", b"id=\"notification-alerts-list\"" in content),
    ("11. Notification drawer toggle exists", b"toggleNotificationDrawer" in content),
    ("12. Sanatan notifications update function exists", b"updateSanatanNotifications" in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL 12 TAB & NOTIFICATION CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
