"""
Jyotish Constants and Reference Data

All traditional Vedic astrology constants used throughout the calculation engine.
Based on classical Parashari principles.
"""

from typing import Dict, List, Tuple

# === ZODIAC SIGNS (RASHIS) ===

RASHIS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

RASHI_LORDS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

RASHI_ELEMENTS = {
    "Aries": "Fire",
    "Taurus": "Earth",
    "Gemini": "Air",
    "Cancer": "Water",
    "Leo": "Fire",
    "Virgo": "Earth",
    "Libra": "Air",
    "Scorpio": "Water",
    "Sagittarius": "Fire",
    "Capricorn": "Earth",
    "Aquarius": "Air",
    "Pisces": "Water",
}

RASHI_QUALITIES = {
    "Aries": "Cardinal",
    "Taurus": "Fixed",
    "Gemini": "Mutable",
    "Cancer": "Cardinal",
    "Leo": "Fixed",
    "Virgo": "Mutable",
    "Libra": "Cardinal",
    "Scorpio": "Fixed",
    "Sagittarius": "Mutable",
    "Capricorn": "Cardinal",
    "Aquarius": "Fixed",
    "Pisces": "Mutable",
}

# === NAKSHATRAS (27 LUNAR MANSIONS) ===

# Each nakshatra spans 13°20' (13.333... degrees)
NAKSHATRA_SPAN = 13 + 1/3  # degrees

NAKSHATRAS = [
    {"name": "Ashwini", "lord": "Ketu", "deity": "Ashwini Kumaras", "start": 0.0},
    {"name": "Bharani", "lord": "Venus", "deity": "Yama", "start": 13.333333},
    {"name": "Krittika", "lord": "Sun", "deity": "Agni", "start": 26.666667},
    {"name": "Rohini", "lord": "Moon", "deity": "Brahma", "start": 40.0},
    {"name": "Mrigashira", "lord": "Mars", "deity": "Soma", "start": 53.333333},
    {"name": "Ardra", "lord": "Rahu", "deity": "Rudra", "start": 66.666667},
    {"name": "Punarvasu", "lord": "Jupiter", "deity": "Aditi", "start": 80.0},
    {"name": "Pushya", "lord": "Saturn", "deity": "Brihaspati", "start": 93.333333},
    {"name": "Ashlesha", "lord": "Mercury", "deity": "Serpents", "start": 106.666667},
    {"name": "Magha", "lord": "Ketu", "deity": "Pitris", "start": 120.0},
    {"name": "Purva Phalguni", "lord": "Venus", "deity": "Bhaga", "start": 133.333333},
    {"name": "Uttara Phalguni", "lord": "Sun", "deity": "Aryaman", "start": 146.666667},
    {"name": "Hasta", "lord": "Moon", "deity": "Savitar", "start": 160.0},
    {"name": "Chitra", "lord": "Mars", "deity": "Tvashtar", "start": 173.333333},
    {"name": "Swati", "lord": "Rahu", "deity": "Vayu", "start": 186.666667},
    {"name": "Vishakha", "lord": "Jupiter", "deity": "Indra-Agni", "start": 200.0},
    {"name": "Anuradha", "lord": "Saturn", "deity": "Mitra", "start": 213.333333},
    {"name": "Jyeshtha", "lord": "Mercury", "deity": "Indra", "start": 226.666667},
    {"name": "Mula", "lord": "Ketu", "deity": "Nirriti", "start": 240.0},
    {"name": "Purva Ashadha", "lord": "Venus", "deity": "Apas", "start": 253.333333},
    {"name": "Uttara Ashadha", "lord": "Sun", "deity": "Vishvadevas", "start": 266.666667},
    {"name": "Shravana", "lord": "Moon", "deity": "Vishnu", "start": 280.0},
    {"name": "Dhanishta", "lord": "Mars", "deity": "Vasus", "start": 293.333333},
    {"name": "Shatabhisha", "lord": "Rahu", "deity": "Varuna", "start": 306.666667},
    {"name": "Purva Bhadrapada", "lord": "Jupiter", "deity": "Aja Ekapada", "start": 320.0},
    {"name": "Uttara Bhadrapada", "lord": "Saturn", "deity": "Ahir Budhnya", "start": 333.333333},
    {"name": "Revati", "lord": "Mercury", "deity": "Pushan", "start": 346.666667},
]

# Each nakshatra has 4 padas of 3°20' each
PADA_SPAN = NAKSHATRA_SPAN / 4  # 3.333... degrees

# === PLANETS ===

PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",  # North Node
    "Ketu",  # South Node
]

# Swiss Ephemeris planet IDs
SWISSEPH_PLANETS = {
    "Sun": 0,
    "Moon": 1,
    "Mercury": 2,
    "Venus": 3,
    "Mars": 4,
    "Jupiter": 5,
    "Saturn": 6,
    "Rahu": 11,  # True Node
    "Ketu": -1,  # Calculated as Rahu + 180°
}

PLANET_SYMBOLS = {
    "Sun": "☉",
    "Moon": "☽",
    "Mars": "♂",
    "Mercury": "☿",
    "Jupiter": "♃",
    "Venus": "♀",
    "Saturn": "♄",
    "Rahu": "☊",
    "Ketu": "☋",
}

# Natural benefics and malefics
NATURAL_BENEFICS = ["Jupiter", "Venus", "Mercury", "Moon"]  # Mercury when alone
NATURAL_MALEFICS = ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]

# === VIMSHOTTARI DASHA SYSTEM ===

# Dasha periods in years
DASHA_PERIODS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

# Total cycle = 120 years
DASHA_TOTAL_YEARS = sum(DASHA_PERIODS.values())

# Sequence order
DASHA_SEQUENCE = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
]

# Nakshatra lords (for determining birth Dasha)
NAKSHATRA_DASHA_LORDS = [
    "Ketu",    # Ashwini
    "Venus",   # Bharani
    "Sun",     # Krittika
    "Moon",    # Rohini
    "Mars",    # Mrigashira
    "Rahu",    # Ardra
    "Jupiter", # Punarvasu
    "Saturn",  # Pushya
    "Mercury", # Ashlesha
    "Ketu",    # Magha
    "Venus",   # Purva Phalguni
    "Sun",     # Uttara Phalguni
    "Moon",    # Hasta
    "Mars",    # Chitra
    "Rahu",    # Swati
    "Jupiter", # Vishakha
    "Saturn",  # Anuradha
    "Mercury", # Jyeshtha
    "Ketu",    # Mula
    "Venus",   # Purva Ashadha
    "Sun",     # Uttara Ashadha
    "Moon",    # Shravana
    "Mars",    # Dhanishta
    "Rahu",    # Shatabhisha
    "Jupiter", # Purva Bhadrapada
    "Saturn",  # Uttara Bhadrapada
    "Mercury", # Revati
]

# === HOUSES ===

HOUSES = list(range(1, 13))

HOUSE_SIGNIFICATIONS = {
    1: "Self, Body, Personality, Appearance",
    2: "Wealth, Family, Speech, Food",
    3: "Courage, Siblings, Skills, Efforts",
    4: "Home, Mother, Happiness, Property",
    5: "Children, Intelligence, Creativity, Romance",
    6: "Enemies, Disease, Service, Obstacles",
    7: "Spouse, Partnerships, Business, Others",
    8: "Longevity, Transformation, Occult, Inheritance",
    9: "Dharma, Guru, Father, Fortune, Higher Learning",
    10: "Career, Status, Reputation, Authority",
    11: "Gains, Friends, Aspirations, Income",
    12: "Loss, Liberation, Foreign, Expenses, Spirituality",
}

# House types
KENDRAS = [1, 4, 7, 10]  # Angular houses (most powerful)
TRIKONAS = [1, 5, 9]      # Trinal houses (dharmic, auspicious)
DUSTHANAS = [6, 8, 12]    # Difficult houses
UPACHAYAS = [3, 6, 10, 11] # Growing houses (improve with time)

# === ASPECTS (GRAHA DRISHTI) ===

# All planets aspect 7th house from their position
UNIVERSAL_ASPECTS = [7]

# Special aspects (in addition to 7th)
SPECIAL_ASPECTS = {
    "Mars": [4, 8],      # Mars aspects 4th, 7th, 8th
    "Jupiter": [5, 9],   # Jupiter aspects 5th, 7th, 9th
    "Saturn": [3, 10],   # Saturn aspects 3rd, 7th, 10th
}

# === DIVISIONAL CHARTS (VARGAS) ===

DIVISIONAL_CHARTS = {
    "D1": {"name": "Rashi", "division": 1, "signification": "Body, Physical Life"},
    "D2": {"name": "Hora", "division": 2, "signification": "Wealth"},
    "D3": {"name": "Drekkana", "division": 3, "signification": "Siblings"},
    "D4": {"name": "Chaturthamsa", "division": 4, "signification": "Fortune"},
    "D7": {"name": "Saptamsa", "division": 7, "signification": "Children"},
    "D9": {"name": "Navamsa", "division": 9, "signification": "Dharma, Spouse"},
    "D10": {"name": "Dasamsa", "division": 10, "signification": "Career"},
    "D12": {"name": "Dwadasamsa", "division": 12, "signification": "Parents"},
    "D16": {"name": "Shodasamsa", "division": 16, "signification": "Vehicles"},
    "D20": {"name": "Vimsamsa", "division": 20, "signification": "Spirituality"},
    "D24": {"name": "Chaturvimsamsa", "division": 24, "signification": "Education"},
    "D27": {"name": "Nakshatramsa", "division": 27, "signification": "Strengths"},
    "D30": {"name": "Trimsamsa", "division": 30, "signification": "Misfortunes"},
    "D40": {"name": "Khavedamsa", "division": 40, "signification": "Auspicious/Inauspicious"},
    "D45": {"name": "Akshavedamsa", "division": 45, "signification": "Character"},
    "D60": {"name": "Shashtiamsa", "division": 60, "signification": "Karma"},
}

# Commonly used divisions (Phase 1 focus)
PRIMARY_VARGAS = ["D1", "D9"]

# Seven divisional charts (Saptha Varga)
SAPTHA_VARGA = ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]

# Sixteen divisional charts (Shodasha Varga)
SHODASHA_VARGA = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", 
                  "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]

# === PLANETARY RELATIONSHIPS ===

# Natural friendships
PLANET_FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
    "Rahu": ["Mercury", "Venus", "Saturn"],
    "Ketu": ["Mars", "Jupiter"],
}

PLANET_ENEMIES = {
    "Sun": ["Venus", "Saturn"],
    "Moon": ["None"],
    "Mars": ["Mercury"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Moon"],
    "Saturn": ["Sun", "Moon", "Mars"],
    "Rahu": ["Sun", "Moon", "Mars"],
    "Ketu": ["Sun", "Moon"],
}

# === EXALTATION & DEBILITATION ===

EXALTATION = {
    "Sun": {"sign": "Aries", "degree": 10.0},
    "Moon": {"sign": "Taurus", "degree": 3.0},
    "Mars": {"sign": "Capricorn", "degree": 28.0},
    "Mercury": {"sign": "Virgo", "degree": 15.0},
    "Jupiter": {"sign": "Cancer", "degree": 5.0},
    "Venus": {"sign": "Pisces", "degree": 27.0},
    "Saturn": {"sign": "Libra", "degree": 20.0},
    "Rahu": {"sign": "Taurus", "degree": None},  # Some say Gemini
    "Ketu": {"sign": "Scorpio", "degree": None},
}

DEBILITATION = {
    "Sun": {"sign": "Libra", "degree": 10.0},
    "Moon": {"sign": "Scorpio", "degree": 3.0},
    "Mars": {"sign": "Cancer", "degree": 28.0},
    "Mercury": {"sign": "Pisces", "degree": 15.0},
    "Jupiter": {"sign": "Capricorn", "degree": 5.0},
    "Venus": {"sign": "Virgo", "degree": 27.0},
    "Saturn": {"sign": "Aries", "degree": 20.0},
    "Rahu": {"sign": "Scorpio", "degree": None},
    "Ketu": {"sign": "Taurus", "degree": None},
}

# === AYANAMSA ===

AYANAMSA_LAHIRI = "Lahiri"  # Most commonly used

# === UTILITY FUNCTIONS ===

def get_rashi_from_longitude(longitude: float) -> str:
    """Convert absolute longitude (0-360) to rashi name"""
    rashi_index = int(longitude / 30)
    return RASHIS[rashi_index % 12]

def get_nakshatra_from_longitude(longitude: float) -> Tuple[str, int, str]:
    """
    Get nakshatra name, pada, and lord from longitude
    Returns: (nakshatra_name, pada_number, ruling_planet)
    """
    # Normalize to 0-360
    longitude = longitude % 360
    
    # Find nakshatra (each is 13.333... degrees)
    nakshatra_index = int(longitude / NAKSHATRA_SPAN)
    nakshatra = NAKSHATRAS[nakshatra_index]
    
    # Find pada within nakshatra
    position_in_nakshatra = longitude - nakshatra["start"]
    pada = int(position_in_nakshatra / PADA_SPAN) + 1
    
    return (nakshatra["name"], pada, nakshatra["lord"])

def get_house_from_longitude(longitude: float, ascendant_long: float) -> int:
    """
    Calculate house number using Whole Sign system
    House 1 = sign of ascendant
    """
    # Get rashi indices
    asc_rashi_index = int(ascendant_long / 30)
    planet_rashi_index = int(longitude / 30)
    
    # House is offset from ascendant rashi
    house = ((planet_rashi_index - asc_rashi_index) % 12) + 1
    
    return house

def normalize_longitude(longitude: float) -> float:
    """Normalize longitude to 0-360 range"""
    return longitude % 360
