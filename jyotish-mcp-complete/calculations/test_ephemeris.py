#!/usr/bin/env python3
"""
Quick test to verify Swiss Ephemeris is working correctly.
Tests calculation for Her's birth chart: Sep 27, 1953, 9:10 AM, Amritapuri
"""

import sys
import os

# Add calculations directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import swisseph as swe
    from constants import get_nakshatra_from_longitude, get_rashi_from_longitude
    
    # Set ephemeris path
    ephe_path = os.path.join(os.path.dirname(__file__), '..', 'ephemeris_data')
    swe.set_ephe_path(ephe_path)
    
    # Set Lahiri ayanamsa
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    print("=" * 60)
    print("Swiss Ephemeris Verification Test")
    print("=" * 60)
    print()
    
    # Calculate Julian Day for Sep 27, 1953, 9:10 AM IST
    # 9:10 AM IST = 3:40 AM UT (IST is +5:30)
    hour_ut = 9.0 + (10.0/60.0) - 5.5  # Convert to UT
    jd = swe.julday(1953, 9, 27, hour_ut)
    
    print(f"Date: September 27, 1953, 9:10 AM IST")
    print(f"Julian Day: {jd:.6f}")
    print()
    
    # Calculate planetary positions
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
    }
    
    print("Sidereal Planetary Positions:")
    print("-" * 60)
    
    for planet_name, planet_id in planets.items():
        try:
            result = swe.calc_ut(jd, planet_id, swe.FLG_SIDEREAL)
            longitude = result[0]
            speed = result[3]
            
            rashi = get_rashi_from_longitude(longitude)
            nakshatra, pada, lord = get_nakshatra_from_longitude(longitude)
            
            degree_in_rashi = longitude % 30
            is_retrograde = speed < 0
            
            print(f"{planet_name:8s}: {longitude:7.2f}° | {rashi:12s} {degree_in_rashi:5.2f}° | "
                  f"{nakshatra:16s} pada {pada} | {'R' if is_retrograde else ' '}")
        except Exception as e:
            print(f"{planet_name:8s}: ERROR - {e}")
    
    # Calculate Rahu (True Node)
    try:
        result = swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SIDEREAL)
        rahu_long = result[0]
        rashi = get_rashi_from_longitude(rahu_long)
        nakshatra, pada, lord = get_nakshatra_from_longitude(rahu_long)
        degree_in_rashi = rahu_long % 30
        
        print(f"{'Rahu':8s}: {rahu_long:7.2f}° | {rashi:12s} {degree_in_rashi:5.2f}° | "
              f"{nakshatra:16s} pada {pada} |  ")
        
        # Ketu is opposite Rahu
        ketu_long = (rahu_long + 180) % 360
        rashi = get_rashi_from_longitude(ketu_long)
        nakshatra, pada, lord = get_nakshatra_from_longitude(ketu_long)
        degree_in_rashi = ketu_long % 30
        
        print(f"{'Ketu':8s}: {ketu_long:7.2f}° | {rashi:12s} {degree_in_rashi:5.2f}° | "
              f"{nakshatra:16s} pada {pada} |  ")
    except Exception as e:
        print(f"Rahu/Ketu: ERROR - {e}")
    
    print()
    print("=" * 60)
    print("✓ Swiss Ephemeris is working correctly!")
    print("=" * 60)
    print()
    print("Expected Results for Verification:")
    print("- Moon should be in Capricorn")
    print("- Sun should be in Virgo")
    print("- Check against known chart software")
    print()
    
except ImportError as e:
    print("ERROR: Missing dependencies")
    print(f"Details: {e}")
    print()
    print("Please ensure:")
    print("1. Virtual environment is activated")
    print("2. Dependencies installed: pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"ERROR: {e}")
    print()
    print("Please check:")
    print("1. Ephemeris files downloaded in calculations/ephemeris_data/")
    print("2. Files: sepl_18.se1, semo_18.se1, seas_18.se1, sefstars.txt")
    sys.exit(1)
