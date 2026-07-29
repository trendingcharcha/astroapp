with open('index.html', 'rb') as f:
    content = f.read()

dob_var = b'${date ||'

checks = [
    ('1. Date fallback abort (no new Date() fallback in generateChart)',
     b'CRITICAL: Never fallback to today' in content
     and b'year = now.getFullYear();\r\nmonth = now.getMonth() + 1;\r\nday = now.getDate();\r\nhour = now.getHours();\r\nmin = now.getMinutes();\r\n}' not in content),

    ('2. switchTab is async',
     b'async function switchTab(index, btn)' in content),

    ('3. switchTab awaits autoFillKundliFromOnboarding',
     b'await autoFillKundliFromOnboarding()' in content),

    ('4. switchTab awaits generateLalKitabReport',
     b'await generateLalKitabReport()' in content),

    ('5. Onboarding bad injection removed',
     b'} suggestionsDiv = document.getElementById' not in content),

    ('6. Coach Mission EN DOB/POB in predictionHTML',
     b'Date of Birth</strong> ' + dob_var in content
     and b'Place of Birth</strong> ${cityName' in content),

    ('7. Coach Mission HI DOB/POB in predictionHTML',
     '\u091c\u0928\u094d\u092e \u0924\u093f\u0925\u093f'.encode('utf-8') in content
     and b'| <strong>' + '\u091c\u0928\u094d\u092e \u0938\u094d\u0925\u093e\u0928'.encode('utf-8') in content),

    ('8. No 150ms setTimeout race condition in switchTab',
     b'setTimeout(() =>' not in content[
         content.find(b'async function switchTab'):
         content.find(b'async function switchTab') + 3000
     ]),

    ('9. Onboarding section closes properly after scrollTop',
     b'if (screen) screen.scrollTop = 0;\r\n}\r\n}\r\n}\r\n' in content),
]

all_passed = True
for name, result in checks:
    icon = 'PASS' if result else 'FAIL'
    if not result:
        all_passed = False
    print(f'{icon}: {name}')

print()
print('ALL CHECKS PASSED' if all_passed else 'SOME CHECKS FAILED - review above')
