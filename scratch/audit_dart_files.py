import os

lib_dir = os.path.join(os.getcwd(), 'lib')

print("=== AUDITING FLUTTER DART FILES FOR STATIC PLACEHOLDERS ===")

for root, dirs, files in os.walk(lib_dir):
    for file in files:
        if file.endswith('.dart'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"\n[FILE] {file} ({len(content)} bytes)")
            # Check for hardcoded strings that look like static predictions
            if "Kundli" in content or "WebView" in content:
                print(" - Integrates with Web App / WebView")
