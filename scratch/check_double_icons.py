import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for adjacent icons
adjacent_icons = re.findall(r'(<(?:svg|i|span class=["\'][^"\']*icon[^"\']*["\'])[\s\S]*?</(?:svg|i|span>))\s*(<(?:svg|i|span class=["\'][^"\']*icon[^"\']*["\'])[\s\S]*?</(?:svg|i|span>))', content, re.IGNORECASE)

print(f"Total adjacent icon matches: {len(adjacent_icons)}")
for idx, (icon1, icon2) in enumerate(adjacent_icons):
    print(f"Match {idx+1}:")
    print(" Icon 1:", icon1[:60])
    print(" Icon 2:", icon2[:60])
