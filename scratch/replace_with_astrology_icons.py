import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== REPLACING ALL GENERIC ICONS WITH VEDIC ASTROLOGY SVG ICONS ===")

# Definition of authentic Astro SVG icons

# 1. Kundli Chart Grid SVG Icon (Diamond Chart Layout)
ASTRO_ICON_KUNDLI = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 3l18 18M21 3L3 21"/><polygon points="12 3 21 12 12 21 3 12"/></svg>'

# 2. Sun & Solar Rays SVG Icon (Surya / Ascendant Power)
ASTRO_ICON_SUN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'

# 3. Crescent Moon & Star SVG Icon (Chandra / Nakshatra)
ASTRO_ICON_MOON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/><path d="M19 3v4M21 5h-4"/></svg>'

# 4. Planetary Orbit / Ringed Planet SVG Icon (Graha / Dasha)
ASTRO_ICON_PLANET = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="6"/><path d="M2.05 13a10.5 10.5 0 0 1 19.9 0M2.05 11a10.5 10.5 0 0 0 19.9 0"/></svg>'

# 5. Faceted Gemstone / Ratna SVG Icon (Power Stone)
ASTRO_ICON_GEMSTONE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="6 3 18 3 22 9 12 21 2 9 6 3"/><line x1="11" y1="3" x2="8" y2="9"/><line x1="13" y1="3" x2="16" y2="9"/><line x1="2" y1="9" x2="22" y2="9"/><line x1="12" y1="21" x2="8" y2="9"/><line x1="12" y1="21" x2="16" y2="9"/></svg>'

# 6. Sacred Vastu Compass / Star Yantra SVG Icon
ASTRO_ICON_COMPASS = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>'

# 7. Constellation 4-Point Star SVG Icon (Nakshatra Star)
ASTRO_ICON_STAR = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'

# 8. Twin Star Cosmic Marriage Union SVG Icon
ASTRO_ICON_UNION = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/><polygon points="12 2 13.5 5 16.5 5.5 14 8 14.8 11 12 9.5 9.2 11 10 8 7.5 5.5 10.5 5 12 2"/></svg>'

# Replace Bottom Navigation Icons with Astrology Icons
nav_replacements = [
  (r'id="nav-home"[\s\S]*?<svg[\s\S]*?</svg>', f'id="nav-home">{ASTRO_ICON_SUN}'),
  (r'id="nav-kundli"[\s\S]*?<svg[\s\S]*?</svg>', f'id="nav-kundli">{ASTRO_ICON_KUNDLI}'),
  (r'id="nav-lalkitab"[\s\S]*?<svg[\s\S]*?</svg>', f'id="nav-lalkitab">{ASTRO_ICON_PLANET}'),
  (r'id="nav-matching"[\s\S]*?<svg[\s\S]*?</svg>', f'id="nav-matching">{ASTRO_ICON_UNION}'),
  (r'id="nav-vastu"[\s\S]*?<svg[\s\S]*?</svg>', f'id="nav-vastu">{ASTRO_ICON_COMPASS}'),
  (r'id="nav-coach"[\s\S]*?<svg[\s\S]*?</svg>', f'id="nav-coach">{ASTRO_ICON_STAR}'),
  (r'id="nav-settings"[\s\S]*?<svg[\s\S]*?</svg>', f'id="nav-settings">{ASTRO_ICON_GEMSTONE}')
]

for pat, repl in nav_replacements:
    content = re.sub(pat, repl, content, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY UPDATED ALL BOTTOM NAVIGATION ICONS TO AUTHENTIC VEDIC ASTROLOGY SVGS!")
