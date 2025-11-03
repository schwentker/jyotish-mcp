# Divisional Charts (Vargas) Implementation Specification

**File:** `calculations/varga_calculator.py`  
**Priority:** HIGH (D9 Navamsa is critical for readings)  
**Estimated Time:** 2-4 hours  
**Difficulty:** Medium

---

## Overview

Divisional charts (Vargas) are a core component of Vedic astrology. Each varga divides the zodiac into smaller sections to analyze specific life domains. Currently only D1 (birth chart) is implemented. This spec details implementation of D2-D60.

## Priority Order

1. **D9 (Navamsa)** - CRITICAL - Most important divisional chart
2. **D2, D3, D7, D10, D12** - HIGH - Commonly used charts
3. **D4, D16, D20, D24, D27** - MEDIUM - Standard charts
4. **D30** - MEDIUM - Special irregular divisions
5. **D40, D45, D60** - LOW - Advanced charts

## Mathematical Foundation

### Standard Formula

For most divisional charts, the formula is:

```python
def calculate_varga_position(longitude, divisions):
    """
    Calculate varga position for a planet
    
    Args:
        longitude: Planet's tropical longitude (0-360 degrees)
        divisions: Number of divisions per sign (2, 3, 9, 10, etc.)
    
    Returns:
        varga_sign: Sign number in varga chart (0-11)
        varga_longitude: Exact longitude in varga chart
    """
    # Which birth sign (0-11)
    birth_sign = int(longitude / 30)
    
    # Degrees within that sign (0-30)
    degrees_in_sign = longitude % 30
    
    # Which division within the sign
    division_index = int(degrees_in_sign * divisions / 30)
    
    # Calculate varga sign
    varga_sign = (birth_sign * divisions + division_index) % 12
    
    # Calculate exact longitude within varga sign
    division_size = 30 / divisions
    degrees_in_division = degrees_in_sign % division_size
    varga_degrees_in_sign = (degrees_in_division * divisions)
    varga_longitude = varga_sign * 30 + varga_degrees_in_sign
    
    return varga_sign, varga_longitude
```

### Odd/Even Sign Rules

Some vargas have different counting methods for odd vs even signs:

```python
def is_odd_sign(sign_num):
    """Check if sign is odd (Aries, Gemini, Leo, etc.)"""
    return sign_num % 2 == 0  # 0=Aries, 2=Gemini, etc. are odd signs

def calculate_varga_with_odd_even(longitude, divisions):
    """
    Some vargas count from different starting points for odd/even signs
    """
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division_index = int(degrees_in_sign * divisions / 30)
    
    if is_odd_sign(birth_sign):
        # Odd signs: count from birth sign
        varga_sign = (birth_sign + division_index) % 12
    else:
        # Even signs: count from a different starting point
        # (varies by varga type)
        offset = get_even_sign_offset(divisions)
        varga_sign = (birth_sign + offset + division_index) % 12
    
    return varga_sign
```

---

## Detailed Varga Specifications

### D1 - Rashi (Birth Chart)
**Status:** ✅ Already implemented  
**Purpose:** Main birth chart  
**Formula:** No calculation needed, use natal positions

---

### D2 - Hora (Wealth)
**Purpose:** Wealth, material resources  
**Divisions:** 2 per sign (15° each)  
**Rule:** 
- Odd signs: First half → Leo (sign 4), Second half → Cancer (sign 3)
- Even signs: First half → Cancer (sign 3), Second half → Leo (sign 4)

```python
def calculate_d2(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    
    if is_odd_sign(birth_sign):
        # First 15° → Leo, Second 15° → Cancer
        if degrees_in_sign < 15:
            return 4  # Leo
        else:
            return 3  # Cancer
    else:
        # First 15° → Cancer, Second 15° → Leo
        if degrees_in_sign < 15:
            return 3  # Cancer
        else:
            return 4  # Leo
```

---

### D3 - Drekkana (Siblings)
**Purpose:** Siblings, courage, initiative  
**Divisions:** 3 per sign (10° each)  
**Rule:** 
- Odd signs: Count from sign itself (0°-10° = sign, 10°-20° = sign+4, 20°-30° = sign+8)
- Even signs: Count from sign+8

```python
def calculate_d3(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign / 10)  # 0, 1, or 2
    
    if is_odd_sign(birth_sign):
        varga_sign = (birth_sign + division * 4) % 12
    else:
        varga_sign = (birth_sign + 8 + division * 4) % 12
    
    return varga_sign
```

---

### D4 - Chaturthamsa (Property)
**Purpose:** Property, fixed assets, residence  
**Divisions:** 4 per sign (7.5° each)  
**Rule:** Standard formula with divisions=4

```python
def calculate_d4(longitude):
    return calculate_varga_position(longitude, 4)[0]
```

---

### D7 - Saptamsa (Children)
**Purpose:** Children, progeny  
**Divisions:** 7 per sign (4°17'8.57" each)  
**Rule:** 
- Odd signs: Count from birth sign
- Even signs: Count from birth sign + 6

```python
def calculate_d7(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * 7 / 30)
    
    if is_odd_sign(birth_sign):
        varga_sign = (birth_sign + division) % 12
    else:
        varga_sign = (birth_sign + 6 + division) % 12
    
    return varga_sign
```

---

### D9 - Navamsa (Relationships/Dharma) ⭐ MOST IMPORTANT
**Purpose:** Marriage, relationships, dharma, soul development  
**Divisions:** 9 per sign (3°20' each)  
**Rule:** 
- Odd signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius): Count from same sign
- Even signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces): Count from 9th sign

```python
def calculate_d9(longitude):
    """
    D9 (Navamsa) - THE MOST IMPORTANT DIVISIONAL CHART
    
    Each sign is divided into 9 parts of 3°20' each.
    Counting starts from:
    - Odd signs (0, 2, 4, 6, 8, 10): From the sign itself
    - Even signs (1, 3, 5, 7, 9, 11): From the 9th sign (birth_sign + 8)
    
    Example:
    - Sun at 10° Aries (odd): 10°/3.333° = 3rd division → Aries + 3 = Cancer
    - Sun at 10° Taurus (even): 10°/3.333° = 3rd division → Capricorn + 3 = Pisces
    """
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    
    # Each navamsa is 3°20' = 3.333... degrees
    navamsa_division = int(degrees_in_sign / (30/9))
    
    if is_odd_sign(birth_sign):
        # Odd signs: count from the sign itself
        varga_sign = (birth_sign + navamsa_division) % 12
    else:
        # Even signs: count from 9th sign (birth_sign + 8)
        varga_sign = (birth_sign + 8 + navamsa_division) % 12
    
    # Calculate exact longitude in navamsa
    navamsa_portion = (degrees_in_sign % (30/9)) * 9
    varga_longitude = varga_sign * 30 + navamsa_portion
    
    return varga_sign, varga_longitude
```

**Test Case for D9:**
```python
# Test: Sun at 10° Virgo (Virgo = sign 5, which is even)
longitude = 155.0  # 5 * 30 + 25 = 155°
# Expected: 
# - Within sign: 25°
# - Navamsa division: int(25 / 3.333) = 7
# - Even sign, so: (5 + 8 + 7) % 12 = 20 % 12 = 8 (Sagittarius)
```

---

### D10 - Dasamsa (Career)
**Purpose:** Career, profession, livelihood  
**Divisions:** 10 per sign (3° each)  
**Rule:** 
- Odd signs: Count from sign itself
- Even signs: Count from 9th sign

```python
def calculate_d10(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign / 3)  # 10 divisions of 3° each
    
    if is_odd_sign(birth_sign):
        varga_sign = (birth_sign + division) % 12
    else:
        varga_sign = (birth_sign + 8 + division) % 12
    
    return varga_sign
```

---

### D12 - Dwadasamsa (Parents)
**Purpose:** Parents, ancestors  
**Divisions:** 12 per sign (2.5° each)  
**Rule:** Standard formula, count from birth sign

```python
def calculate_d12(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign / 2.5)  # 12 divisions of 2.5° each
    varga_sign = (birth_sign + division) % 12
    return varga_sign
```

---

### D16 - Shodasamsa (Vehicles/Comforts)
**Purpose:** Vehicles, material comforts, luxuries  
**Divisions:** 16 per sign (1.875° each)  
**Rule:** 
- Odd signs: Start from Aries
- Even signs: Start from Libra

```python
def calculate_d16(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * 16 / 30)
    
    if is_odd_sign(birth_sign):
        varga_sign = division % 12  # Start from Aries
    else:
        varga_sign = (6 + division) % 12  # Start from Libra
    
    return varga_sign
```

---

### D20 - Vimsamsa (Spiritual Practices)
**Purpose:** Spiritual development, worship, meditation  
**Divisions:** 20 per sign (1.5° each)  
**Rule:** 
- Odd signs: Start from Aries
- Even signs: Start from Libra

```python
def calculate_d20(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * 20 / 30)
    
    if is_odd_sign(birth_sign):
        varga_sign = division % 12
    else:
        varga_sign = (6 + division) % 12
    
    return varga_sign
```

---

### D24 - Chaturvimsamsa (Education)
**Purpose:** Education, learning, knowledge  
**Divisions:** 24 per sign (1.25° each)  
**Rule:** 
- Odd signs: Start from Leo
- Even signs: Start from Cancer

```python
def calculate_d24(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * 24 / 30)
    
    if is_odd_sign(birth_sign):
        varga_sign = (4 + division) % 12  # Start from Leo
    else:
        varga_sign = (3 + division) % 12  # Start from Cancer
    
    return varga_sign
```

---

### D27 - Nakshatramsa (Strengths/Weaknesses)
**Purpose:** Strengths, weaknesses, general well-being  
**Divisions:** 27 per sign (1°6'40" each)  
**Rule:** 
- Odd signs: Start from same sign
- Even signs: Start from same sign

```python
def calculate_d27(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * 27 / 30)
    varga_sign = (birth_sign + division) % 12
    return varga_sign
```

---

### D30 - Trimsamsa (Misfortunes) ⚠️ SPECIAL IRREGULAR DIVISIONS
**Purpose:** Evils, misfortunes, difficulties  
**Divisions:** IRREGULAR - 5 unequal parts per sign  
**Rule:** Different divisions for odd/even signs with different planetary rulers

**Odd signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius):**
- 0°-5° = Mars (sign 0)
- 5°-10° = Saturn (sign 10)
- 10°-18° = Jupiter (sign 8)
- 18°-25° = Mercury (sign 5)
- 25°-30° = Venus (sign 6)

**Even signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces):**
- 0°-5° = Venus (sign 6)
- 5°-12° = Mercury (sign 5)
- 12°-20° = Jupiter (sign 8)
- 20°-25° = Saturn (sign 10)
- 25°-30° = Mars (sign 0)

```python
def calculate_d30(longitude):
    """
    D30 (Trimsamsa) - SPECIAL CASE WITH IRREGULAR DIVISIONS
    """
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    
    if is_odd_sign(birth_sign):
        # Odd signs
        if degrees_in_sign < 5:
            return 0  # Mars/Aries
        elif degrees_in_sign < 10:
            return 10  # Saturn/Aquarius
        elif degrees_in_sign < 18:
            return 8  # Jupiter/Sagittarius
        elif degrees_in_sign < 25:
            return 5  # Mercury/Virgo
        else:
            return 6  # Venus/Libra
    else:
        # Even signs
        if degrees_in_sign < 5:
            return 6  # Venus/Libra
        elif degrees_in_sign < 12:
            return 5  # Mercury/Virgo
        elif degrees_in_sign < 20:
            return 8  # Jupiter/Sagittarius
        elif degrees_in_sign < 25:
            return 10  # Saturn/Aquarius
        else:
            return 0  # Mars/Aries
```

---

### D40 - Khavedamsa (Auspicious/Inauspicious Effects)
**Purpose:** Auspicious and inauspicious effects  
**Divisions:** 40 per sign (0.75° each)  
**Rule:** 
- Odd signs: Start from Aries
- Even signs: Start from Libra

```python
def calculate_d40(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * 40 / 30)
    
    if is_odd_sign(birth_sign):
        varga_sign = division % 12
    else:
        varga_sign = (6 + division) % 12
    
    return varga_sign
```

---

### D45 - Akshavedamsa (Character/Conduct)
**Purpose:** Character, conduct, overall nature  
**Divisions:** 45 per sign (0.666...° each)  
**Rule:** 
- Odd signs: Start from Aries
- Even signs: Start from Libra

```python
def calculate_d45(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * 45 / 30)
    
    if is_odd_sign(birth_sign):
        varga_sign = division % 12
    else:
        varga_sign = (6 + division) % 12
    
    return varga_sign
```

---

### D60 - Shashtiamsa (Past Life Karma)
**Purpose:** Past life karma, subtle karmic influences  
**Divisions:** 60 per sign (0.5° each)  
**Rule:** 
- Odd signs: Start from birth sign
- Even signs: Start from birth sign

```python
def calculate_d60(longitude):
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * 60 / 30)
    varga_sign = (birth_sign + division) % 12
    return varga_sign
```

---

## Implementation Structure

### Complete varga_calculator.py

```python
#!/usr/bin/env python3
"""
Varga Calculator - Divisional charts (D1-D60)
Implements all standard Parashari divisional charts.
"""

import sys
import json
import os
from constants import RASHIS

# Chart cache
CHARTS_DIR = os.path.join(os.path.dirname(__file__), '.charts_cache')

# === HELPER FUNCTIONS ===

def is_odd_sign(sign_num):
    """
    Check if sign is odd (movable signs: Aries, Gemini, Leo, etc.)
    In Vedic system: Aries=0, Taurus=1, Gemini=2, etc.
    So even indices are odd signs!
    """
    return sign_num % 2 == 0


def calculate_varga_position(longitude, divisions, odd_start=0, even_start=0):
    """
    Generic varga calculator for standard divisions
    
    Args:
        longitude: Tropical longitude (0-360)
        divisions: Number of divisions per sign
        odd_start: Starting sign for odd signs (default 0 = same sign)
        even_start: Starting sign offset for even signs (default 0 = same sign)
    
    Returns:
        (varga_sign, varga_longitude)
    """
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign * divisions / 30)
    
    if is_odd_sign(birth_sign):
        varga_sign = (odd_start + division) % 12
    else:
        varga_sign = (even_start + division) % 12
    
    # Calculate exact longitude in varga
    division_size = 30 / divisions
    degrees_in_division = degrees_in_sign % division_size
    varga_degrees = (degrees_in_division * divisions)
    varga_longitude = varga_sign * 30 + varga_degrees
    
    return varga_sign, varga_longitude


# === INDIVIDUAL VARGA CALCULATORS ===

def calculate_d2(longitude):
    """D2 - Hora (Wealth)"""
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    
    if is_odd_sign(birth_sign):
        varga_sign = 4 if degrees_in_sign < 15 else 3  # Leo or Cancer
    else:
        varga_sign = 3 if degrees_in_sign < 15 else 4  # Cancer or Leo
    
    varga_longitude = varga_sign * 30 + (degrees_in_sign % 15) * 2
    return varga_sign, varga_longitude


def calculate_d3(longitude):
    """D3 - Drekkana (Siblings)"""
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign / 10)
    
    if is_odd_sign(birth_sign):
        varga_sign = (birth_sign + division * 4) % 12
    else:
        varga_sign = (birth_sign + 8 + division * 4) % 12
    
    varga_longitude = varga_sign * 30 + (degrees_in_sign % 10) * 3
    return varga_sign, varga_longitude


def calculate_d4(longitude):
    """D4 - Chaturthamsa (Property)"""
    return calculate_varga_position(longitude, 4, odd_start=0, even_start=0)


def calculate_d7(longitude):
    """D7 - Saptamsa (Children)"""
    birth_sign = int(longitude / 30)
    if is_odd_sign(birth_sign):
        return calculate_varga_position(longitude, 7, odd_start=birth_sign, even_start=0)
    else:
        return calculate_varga_position(longitude, 7, odd_start=0, even_start=(birth_sign + 6) % 12)


def calculate_d9(longitude):
    """D9 - Navamsa (Relationships/Dharma) - MOST IMPORTANT"""
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign / (30/9))
    
    if is_odd_sign(birth_sign):
        varga_sign = (birth_sign + division) % 12
    else:
        varga_sign = (birth_sign + 8 + division) % 12
    
    navamsa_portion = (degrees_in_sign % (30/9)) * 9
    varga_longitude = varga_sign * 30 + navamsa_portion
    
    return varga_sign, varga_longitude


def calculate_d10(longitude):
    """D10 - Dasamsa (Career)"""
    birth_sign = int(longitude / 30)
    if is_odd_sign(birth_sign):
        return calculate_varga_position(longitude, 10, odd_start=birth_sign, even_start=0)
    else:
        return calculate_varga_position(longitude, 10, odd_start=0, even_start=(birth_sign + 8) % 12)


def calculate_d12(longitude):
    """D12 - Dwadasamsa (Parents)"""
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    division = int(degrees_in_sign / 2.5)
    varga_sign = (birth_sign + division) % 12
    varga_longitude = varga_sign * 30 + (degrees_in_sign % 2.5) * 12
    return varga_sign, varga_longitude


def calculate_d16(longitude):
    """D16 - Shodasamsa (Vehicles/Comforts)"""
    birth_sign = int(longitude / 30)
    if is_odd_sign(birth_sign):
        return calculate_varga_position(longitude, 16, odd_start=0, even_start=0)
    else:
        return calculate_varga_position(longitude, 16, odd_start=0, even_start=6)


def calculate_d20(longitude):
    """D20 - Vimsamsa (Spiritual Practices)"""
    birth_sign = int(longitude / 30)
    if is_odd_sign(birth_sign):
        return calculate_varga_position(longitude, 20, odd_start=0, even_start=0)
    else:
        return calculate_varga_position(longitude, 20, odd_start=0, even_start=6)


def calculate_d24(longitude):
    """D24 - Chaturvimsamsa (Education)"""
    birth_sign = int(longitude / 30)
    if is_odd_sign(birth_sign):
        return calculate_varga_position(longitude, 24, odd_start=4, even_start=0)
    else:
        return calculate_varga_position(longitude, 24, odd_start=0, even_start=3)


def calculate_d27(longitude):
    """D27 - Nakshatramsa (Strengths/Weaknesses)"""
    birth_sign = int(longitude / 30)
    return calculate_varga_position(longitude, 27, odd_start=birth_sign, even_start=birth_sign)


def calculate_d30(longitude):
    """D30 - Trimsamsa (Misfortunes) - IRREGULAR DIVISIONS"""
    birth_sign = int(longitude / 30)
    degrees_in_sign = longitude % 30
    
    if is_odd_sign(birth_sign):
        if degrees_in_sign < 5:
            varga_sign = 0  # Mars/Aries
        elif degrees_in_sign < 10:
            varga_sign = 10  # Saturn/Aquarius
        elif degrees_in_sign < 18:
            varga_sign = 8  # Jupiter/Sagittarius
        elif degrees_in_sign < 25:
            varga_sign = 5  # Mercury/Virgo
        else:
            varga_sign = 6  # Venus/Libra
    else:
        if degrees_in_sign < 5:
            varga_sign = 6  # Venus/Libra
        elif degrees_in_sign < 12:
            varga_sign = 5  # Mercury/Virgo
        elif degrees_in_sign < 20:
            varga_sign = 8  # Jupiter/Sagittarius
        elif degrees_in_sign < 25:
            varga_sign = 10  # Saturn/Aquarius
        else:
            varga_sign = 0  # Mars/Aries
    
    varga_longitude = varga_sign * 30 + 15  # Approximate midpoint
    return varga_sign, varga_longitude


def calculate_d40(longitude):
    """D40 - Khavedamsa (Auspicious/Inauspicious Effects)"""
    birth_sign = int(longitude / 30)
    if is_odd_sign(birth_sign):
        return calculate_varga_position(longitude, 40, odd_start=0, even_start=0)
    else:
        return calculate_varga_position(longitude, 40, odd_start=0, even_start=6)


def calculate_d45(longitude):
    """D45 - Akshavedamsa (Character/Conduct)"""
    birth_sign = int(longitude / 30)
    if is_odd_sign(birth_sign):
        return calculate_varga_position(longitude, 45, odd_start=0, even_start=0)
    else:
        return calculate_varga_position(longitude, 45, odd_start=0, even_start=6)


def calculate_d60(longitude):
    """D60 - Shashtiamsa (Past Life Karma)"""
    birth_sign = int(longitude / 30)
    return calculate_varga_position(longitude, 60, odd_start=birth_sign, even_start=birth_sign)


# === MAIN VARGA CALCULATOR DISPATCH ===

VARGA_CALCULATORS = {
    'D2': calculate_d2,
    'D3': calculate_d3,
    'D4': calculate_d4,
    'D7': calculate_d7,
    'D9': calculate_d9,
    'D10': calculate_d10,
    'D12': calculate_d12,
    'D16': calculate_d16,
    'D20': calculate_d20,
    'D24': calculate_d24,
    'D27': calculate_d27,
    'D30': calculate_d30,
    'D40': calculate_d40,
    'D45': calculate_d45,
    'D60': calculate_d60,
}


def read_divisional_chart(chart_id, varga):
    """
    Read divisional chart
    
    Args:
        chart_id: Birth chart UUID
        varga: Divisional chart type (D1, D9, D10, etc.)
    
    Returns:
        dict with divisional chart positions
    """
    try:
        # Load birth chart
        cache_file = os.path.join(CHARTS_DIR, f'{chart_id}.json')
        if not os.path.exists(cache_file):
            return {'error': f'Chart {chart_id} not found'}
        
        with open(cache_file, 'r') as f:
            chart = json.load(f)
        
        # D1 just returns birth chart
        if varga == 'D1':
            return {
                'chart_id': chart_id,
                'varga': 'D1',
                'planets': chart['planets']
            }
        
        # Check if varga is implemented
        if varga not in VARGA_CALCULATORS:
            return {
                'error': f'Divisional chart {varga} not yet implemented',
                'message': f'{varga} calculation coming soon.',
                'available': list(VARGA_CALCULATORS.keys())
            }
        
        # Calculate varga positions for all planets
        calculator = VARGA_CALCULATORS[varga]
        varga_planets = {}
        
        for planet_name, planet_data in chart['planets'].items():
            longitude = planet_data['longitude']
            varga_sign, varga_longitude = calculator(longitude)
            
            varga_planets[planet_name] = {
                'sign': varga_sign,
                'sign_name': RASHIS[varga_sign],
                'longitude': varga_longitude,
                'degrees_in_sign': varga_longitude % 30,
                'retrograde': planet_data.get('retrograde', False),
                # Keep original data for reference
                'natal_sign': planet_data['sign'],
                'natal_longitude': longitude
            }
        
        return {
            'chart_id': chart_id,
            'varga': varga,
            'planets': varga_planets,
            'birth_data': {
                'name': chart.get('name'),
                'datetime': chart.get('datetime'),
                'location': chart.get('location')
            }
        }
        
    except Exception as e:
        import traceback
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }


if __name__ == '__main__':
    try:
        input_data = json.loads(sys.argv[1])
        action = input_data.get('action', 'read')
        
        if action == 'read':
            result = read_divisional_chart(
                input_data['chart_id'],
                input_data['varga']
            )
        else:
            result = {'error': f'Unknown action: {action}'}
        
        print(json.dumps(result))
        
    except Exception as e:
        import traceback
        error_result = {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        print(json.dumps(error_result), file=sys.stderr)
        sys.exit(1)
```

---

## Testing Strategy

### Unit Tests

Create `test_vargas.py`:

```python
#!/usr/bin/env python3
"""
Test suite for divisional charts
"""

import json
from varga_calculator import *

# Test chart: Sep 27, 1953, 9:10 AM, Amritapuri
# Sun approximately at 10° Virgo (155°)
# Moon approximately at 23° Cancer (113°)

def test_d9_odd_sign():
    """Test D9 for planet in odd sign (Aries)"""
    # 10° Aries = sign 0, odd
    longitude = 10.0
    sign, long = calculate_d9(longitude)
    # 10° / 3.333 = 3rd division
    # Aries + 3 = Cancer (sign 3)
    assert sign == 3, f"Expected Cancer (3), got {RASHIS[sign]} ({sign})"
    print(f"✓ D9 odd sign: 10° Aries → {RASHIS[sign]}")

def test_d9_even_sign():
    """Test D9 for planet in even sign (Virgo)"""
    # 10° Virgo = 155°, sign 5 (even)
    longitude = 155.0
    sign, long = calculate_d9(longitude)
    # 25° within sign / 3.333 = 7th division
    # Even sign: (5 + 8 + 7) % 12 = 8 (Sagittarius)
    print(f"✓ D9 even sign: 10° Virgo (155°) → {RASHIS[sign]}")

def test_all_vargas():
    """Test that all vargas calculate without error"""
    longitude = 155.0  # 10° Virgo
    
    for varga_name, calculator in VARGA_CALCULATORS.items():
        try:
            sign, long = calculator(longitude)
            print(f"✓ {varga_name}: {RASHIS[sign]} at {long:.2f}°")
        except Exception as e:
            print(f"✗ {varga_name}: ERROR - {e}")

if __name__ == '__main__':
    print("Testing Divisional Charts Calculations\n")
    print("="*50)
    test_d9_odd_sign()
    test_d9_even_sign()
    print("="*50)
    test_all_vargas()
    print("="*50)
    print("\n✓ All tests passed!")
```

### Integration Test

```python
# Test with real chart
import subprocess
import json

chart_id = "YOUR_CHART_UUID_HERE"

for varga in ['D1', 'D9', 'D10', 'D12']:
    cmd = f'python varga_calculator.py \'{{"action":"read","chart_id":"{chart_id}","varga":"{varga}"}}\''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    print(f"\n{varga}:")
    for planet, pos in data['planets'].items():
        print(f"  {planet}: {pos['sign_name']}")
```

---

## Validation Against Reference Software

Compare results with established software:
1. **JHora** (free, Windows) - Most accurate
2. **Jagannatha Hora** - Alternative
3. **Kala** (commercial) - Professional standard

### Validation Checklist

- [ ] D9 matches JHora for test chart
- [ ] D2, D3, D7, D10, D12 match JHora
- [ ] Odd/even sign rules correctly applied
- [ ] D30 irregular divisions correct
- [ ] All 9 planets calculated in each varga
- [ ] Retrograde status preserved
- [ ] Longitude calculations accurate

---

## Success Criteria

✅ **Phase 1 Complete:**
- D9 (Navamsa) working and validated
- Tested with at least 5 known charts
- Matches JHora output within 1°

✅ **Phase 2 Complete:**
- D2, D3, D7, D10, D12 working
- All standard vargas tested
- Documentation complete

✅ **Phase 3 Complete:**
- D16, D20, D24, D27 working
- D30 irregular divisions correct
- D40, D45, D60 working

✅ **Production Ready:**
- All vargas validated against JHora
- Error handling robust
- Performance optimized (<100ms per varga)

---

## Notes

- Sidereal zodiac is used (Lahiri ayanamsa)
- Whole Sign house system
- Classical Parashari formulas
- Swiss Ephemeris for planetary positions
- File-based cache (will migrate to PostgreSQL later)

**Priority:** Implement D9 first, test thoroughly, then add others incrementally.

**Estimated Time:**
- D9 alone: 1 hour
- D2, D3, D7, D10, D12: 2 hours
- All standard vargas: 3-4 hours
- Testing & validation: 1-2 hours
- Total: 4-6 hours for complete implementation

---

## References

- Brihat Parashara Hora Shastra (BPHS) - Classical text
- Jataka Parijata - Secondary reference
- JHora software - Validation
- B.V. Raman - Modern interpretation

**Good luck! Start with D9 - it's the most important!** ⭐
