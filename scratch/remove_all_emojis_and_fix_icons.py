import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Comprehensive regex matching all Unicode Emoji characters
emoji_pattern = re.compile(
    r'[\U0001F600-\U0001F64F]'  # emoticons
    r'|[\U0001F300-\U0001F5FF]'  # symbols & pictographs
    r'|[\U0001F680-\U0001F6FF]'  # transport & map symbols
    r'|[\U0001F1E0-\U0001F1FF]'  # flags
    r'|[\U0001F900-\U0001F9FF]'  # supplemental symbols
    r'|[\U0001FA70-\U0001FAFF]'  # symbols & pictographs extended
    r'|[\u2600-\u26FF]'          # misc symbols (☀️, 🕉️, 🔱, 🌕, 📅, 🔔, ⚠️, ✨, ⚖️, ☁️, etc.)
    r'|[\u2700-\u27BF]'          # dingbats
    r'|[\u2300-\u23FF]'          # technical symbols (⏳, ⏰, ⏱️, etc.)
    r'|[\u2B50\u2B55]'          # stars / circles
    r'|[\uFE0F\uFE0E]'          # variation selectors
    r'|[\u200D]'                 # ZWJ
)

# Remove all emojis
cleaned = emoji_pattern.sub('', content)

# 2. Fix double whitespace or trailing spaces caused by emoji removal
cleaned = re.sub(r' +', ' ', cleaned)
cleaned = re.sub(r'(\n +)+', '\n', cleaned)

# 3. Check for any double SVG icons placed side-by-side (e.g. <svg>...</svg>\s*<svg>...</svg>)
double_svg_pattern = re.compile(r'(<svg[\s\S]*?</svg>)\s*(<svg[\s\S]*?</svg>)', re.IGNORECASE)

def replace_double_svg(match):
    # Keep only the first SVG icon
    return match.group(1)

cleaned = double_svg_pattern.sub(replace_double_svg, cleaned)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(cleaned)

print("SUCCESSFULLY REMOVED ALL EMOJIS AND DOUBLE ICONS FROM INDEX.HTML!")
