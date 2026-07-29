with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. Language toggle button inside Karma Assistant header", b"toggleAppLanguage()" in content and b"lang-toggle-btn" in content),
    ("2. Strict button left-alignment CSS rules present", b"#livechat-messages button" in content and b"text-align: left !important" in content),
    ("3. Grammar fix: 'I was in a hurry and forgot my morning tasks'", b"I was in a hurry and forgot my morning tasks" in content),
    ("4. Grammar fix: 'I am unable to perform the selective task today'", b"I am unable to perform the selective task today" in content),
    ("5. Grammar fix: 'I do not have the required task items'", b"I do not have the required task items" in content),
    ("6. Bilingual Hindi wizard step 1 support", b"startWizardStep1()" in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL GRAMMAR, LANG & ALIGNMENT CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
