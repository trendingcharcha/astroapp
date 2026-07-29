import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== REPLACING ALL GENERIC UI SVGS WITH VEDIC ASTROLOGY SVGS ===")

# Define Astrology SVG Icon Library
ICONS = {
    'sun': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>',
    'moon': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/><path d="M19 3v4M21 5h-4"/></svg>',
    'kundli': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 3l18 18M21 3L3 21"/><polygon points="12 3 21 12 12 21 3 12"/></svg>',
    'planet': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="6"/><path d="M2.05 13a10.5 10.5 0 0 1 19.9 0M2.05 11a10.5 10.5 0 0 0 19.9 0"/></svg>',
    'gemstone': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="6 3 18 3 22 9 12 21 2 9 6 3"/><line x1="11" y1="3" x2="8" y2="9"/><line x1="13" y1="3" x2="16" y2="9"/><line x1="2" y1="9" x2="22" y2="9"/><line x1="12" y1="21" x2="8" y2="9"/><line x1="12" y1="21" x2="16" y2="9"/></svg>',
    'compass': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
    'star': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    'union': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/><polygon points="12 2 13.5 5 16.5 5.5 14 8 14.8 11 12 9.5 9.2 11 10 8 7.5 5.5 10.5 5 12 2"/></svg>',
    'trishul': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2v20M7 4v6a5 5 0 0 0 10 0V4M7 4L4 7M17 4l3 3M12 2l-3 3M12 2l3 3"/></svg>'
}

# 1. Update Card Category Icons inside JS functions
# Replace generic checkmarks/boxes in task icons with astrology SVGs
content = re.sub(
    r"category:\s*'vedic'[\s\S]*?icon:\s*'<svg[\s\S]*?</svg>'",
    f"category: 'vedic', title: titleVal, timeWindow: twVal, text: textVal, xp: xpVal, color: 'var(--gold)', icon: '{ICONS['sun']}'",
    content
)

# Replace generic icons in Lal Kitab tasks
content = re.sub(
    r"icon:\s*'<svg[^>]*><path d=\"M4 19\.5A2\.5 2\.5 0 0 1 6\.5 17H20\"[\s\S]*?</svg>'",
    f"icon: '{ICONS['planet']}'",
    content
)

# Replace generic icons in Vastu tasks
content = re.sub(
    r"icon:\s*'<svg[^>]*><path d=\"M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\"[\s\S]*?</svg>'",
    f"icon: '{ICONS['compass']}'",
    content
)

# Replace generic icons in Practical tasks
content = re.sub(
    r"icon:\s*'<svg[^>]*><circle cx=\"12\" cy=\"12\" r=\"5\"[\s\S]*?</svg>'",
    f"icon: '{ICONS['star']}'",
    content
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY REPLACED GENERIC CARD & TASK ICONS WITH VEDIC ASTROLOGY SVGS!")
