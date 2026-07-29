import math

print("=== TESTING ASTRONOMICAL COMPUTATION ACCURACY FOR MULTIPLE USERS ===")

# Test dataset of 5 distinct users
test_users = [
    {
        "name": "Prateek Shrivastava",
        "dob": "1988-10-10",
        "tob": "06:05",
        "city": "Gorakhpur",
        "lat": 26.7606, "lng": 83.3732, "tz": 5.5,
        "goal": "debt"
    },
    {
        "name": "Ananya Sharma",
        "dob": "1996-04-14",
        "tob": "14:30",
        "city": "Delhi",
        "lat": 28.6139, "lng": 77.2090, "tz": 5.5,
        "goal": "job"
    },
    {
        "name": "Rohan Verma",
        "dob": "1991-11-25",
        "tob": "22:15",
        "city": "Mumbai",
        "lat": 19.0760, "lng": 72.8777, "tz": 5.5,
        "goal": "business"
    },
    {
        "name": "Siddharth Malhotra",
        "dob": "1985-01-16",
        "tob": "09:10",
        "city": "Bengaluru",
        "lat": 12.9716, "lng": 77.5946, "tz": 5.5,
        "goal": "property"
    },
    {
        "name": "Priya Patel",
        "dob": "2000-08-08",
        "tob": "18:45",
        "city": "Ahmedabad",
        "lat": 23.0225, "lng": 72.5714, "tz": 5.5,
        "goal": "marriage"
    }
]

sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
sign_lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

def get_julian_day(year, month, day, hour, minute, tz):
    utc_hour = hour + minute / 60.0 - tz
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100.0)
    b = 2 - a + math.floor(a / 4.0)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5 + (utc_hour / 24.0)
    return jd

def get_lahiri_ayanamsa(jd):
    d = jd - 2451545.0
    return 23.85 + 0.000038 * d

def get_ascendant(jd, lat, lng, ayanamsa):
    d = jd - 2451545.0
    gmst = (18.697374558 + 24.06570982441908 * d) % 24.0
    lmst = (gmst + lng / 15.0) % 24.0
    lst_deg = (lmst * 15.0) % 360.0
    rad_lat = math.radians(lat)
    rad_obliq = math.radians(23.4393)
    rad_lst = math.radians(lst_deg)
    
    asc_rad = math.atan2(math.cos(rad_lst), - (math.sin(rad_obliq) * math.tan(rad_lat) + math.cos(rad_obliq) * math.sin(rad_lst)))
    asc_deg = (math.degrees(asc_rad) + 360) % 360
    sidereal_asc = (asc_deg - ayanamsa + 360) % 360
    return sidereal_asc

print("\n--- ASTRONOMICAL COMPUTATION RESULTS ---")
for u in test_users:
    y, m, d = map(int, u["dob"].split("-"))
    hr, mn = map(int, u["tob"].split(":"))
    jd = get_julian_day(y, m, d, hr, mn, u["tz"])
    ayanamsa = get_lahiri_ayanamsa(jd)
    asc = get_ascendant(jd, u["lat"], u["lng"], ayanamsa)
    lagna_idx = int(asc // 30)
    lagna_deg = asc % 30
    lagna_name = sign_names[lagna_idx]
    lagna_lord = sign_lords[lagna_idx]
    
    print(f"User: {u['name']:22} | DOB: {u['dob']} {u['tob']} | Ascendant: {lagna_name:11} ({lagna_deg:5.2f}°) | Lord: {lagna_lord:7} | Goal: {u['goal']}")
