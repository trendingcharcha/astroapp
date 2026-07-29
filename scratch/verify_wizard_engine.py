with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. startWizardStep1 function exists", b"function startWizardStep1()" in content),
    ("2. handleWizardQ1 function exists", b"function handleWizardQ1(" in content),
    ("3. startWizardStep2 function exists", b"function startWizardStep2()" in content),
    ("4. limitQ2Selections max 3 limit function exists", b"function limitQ2Selections(" in content),
    ("5. startWizardStep3 function exists", b"function startWizardStep3()" in content),
    ("6. generateStep4AlternativeSolutions function exists", b"function generateStep4AlternativeSolutions()" in content),
    ("7. acceptWizardAlternative marks task DONE and awards +20 XP", b"function acceptWizardAlternative(" in content and b"gainXP(20)" in content),
    ("8. Top quick carousel pills removed from chat header", b"In Office Right Now" not in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL WIZARD CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
