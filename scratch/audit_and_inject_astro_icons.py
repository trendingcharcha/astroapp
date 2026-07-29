import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== INJECTING AUTHENTIC VEDIC ASTROLOGY SVG ICONS INTO ALL CARD HEADERS ===")

# Definition of SVG icons for Vastu Cards
vastu_icons = {
    'House & Living Vastu': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    'Business & Work Vastu': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#5dade2" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
    'Sleep & Bedroom Vastu': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ff6b6b" stroke-width="2"><path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/></svg>',
    'Food Eating Vastu': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2ecc71" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg>',
    'Bath & Purification Vastu': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
    'Travel & Expansion Directions': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#e67e22" stroke-width="2"><polygon points="12 2 15 9 22 12 15 15 12 22 9 15 2 12 9 9 12 2"/></svg>'
}

for title, svg in vastu_icons.items():
    pattern = rf'<span style="font-size:1\.4rem;"></span>\s*<h4[^>]*><span class="k-lbl-en">{re.escape(title)}</span>'
    replacement = f'<span style="display:inline-flex; align-items:center; justify-content:center;">{svg}</span>\n<h4 style="margin:0; color:#fff;"><span class="k-lbl-en">{title}</span>'
    content = re.sub(pattern, replacement, content)

# Remove any remaining empty spans `<span style="font-size:1.4rem;"></span>`
content = re.sub(r'<span style="font-size:1\.4rem;"></span>', '', content)

# Upgrade Bottom Navigation Bar with Distinct Gold-Glowing Vedic SVG Icons
nav_gold_icons = {
    'nav-home': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>',
    'nav-kundli': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 3l18 18M21 3L3 21"/><polygon points="12 3 21 12 12 21 3 12"/></svg>',
    'nav-lalkitab': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><circle cx="12" cy="12" r="6"/><path d="M2.05 13a10.5 10.5 0 0 1 19.9 0M2.05 11a10.5 10.5 0 0 0 19.9 0"/></svg>',
    'nav-matching': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>',
    'nav-vastu': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
    'nav-coach': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    'nav-settings': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="6 3 18 3 22 9 12 21 2 9 6 3"/><line x1="11" y1="3" x2="8" y2="9"/><line x1="13" y1="3" x2="16" y2="9"/><line x1="2" y1="9" x2="22" y2="9"/><line x1="12" y1="21" x2="8" y2="9"/><line x1="12" y1="21" x2="16" y2="9"/></svg>'
}

for nav_id, svg_code in nav_gold_icons.items():
    pat = rf'id="{nav_id}"[\s\S]*?<svg[\s\S]*?</svg>'
    repl = f'id="{nav_id}">{svg_code}'
    content = re.sub(pat, repl, content, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY INJECTED ASTROLOGY SVG ICONS INTO VASTU CARDS & BOTTOM NAV!")
