import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Comprehensive Emoji Regex Pattern
emoji_pattern = re.compile(
    r'[\U0001F600-\U0001F64F]'  # emoticons
    r'|[\U0001F300-\U0001F5FF]'  # symbols & pictographs
    r'|[\U0001F680-\U0001F6FF]'  # transport & map symbols
    r'|[\U0001F1E0-\U0001F1FF]'  # flags
    r'|[\U0001F900-\U0001F9FF]'  # supplemental symbols
    r'|[\U0001FA70-\U0001FAFF]'  # symbols & pictographs extended
    r'|[\u2600-\u26FF]'          # misc symbols (☀️, 🕉️, 🔱, 🌕, 📅, 🔔, ⚠️, ✨, ⚖️, etc.)
    r'|[\u2700-\u27BF]'          # dingbats
    r'|[\u2300-\u23FF]'          # technical symbols (⏰, ⏱️, etc.)
    r'|[\u2B50\u2B55]'          # stars / circles
    r'|[\uFE0F\uFE0E]'          # variation selectors
    r'|[\u200D]'                 # ZWJ
)

matches = emoji_pattern.findall(content)
print(f"Total emoji matches found: {len(matches)}")

lines = content.split('\n')
emoji_lines = []
for idx, line in enumerate(lines):
    found = emoji_pattern.findall(line)
    if found:
        emoji_lines.append((idx + 1, line.strip()))

print(f"Total lines containing emojis: {len(emoji_lines)}")
print("\nSample lines with emojis:")
for lno, text in emoji_lines[:25]:
    clean_print = text[:110].encode('ascii', 'ignore').decode('ascii')
    print(f"Line {lno}: {clean_print}")
