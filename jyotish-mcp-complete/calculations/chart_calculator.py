#!/usr/bin/env python3
"""
Chart Calculator - Main orchestrator for birth chart calculations
Handles chart creation, reading, and listing operations
"""

import sys
import json
import swisseph as swe
from datetime import datetime
import os
import uuid
from pathlib import Path

# Set ephemeris path
ephe_path = os.path.join(os.path.dirname(__file__), 'ephemeris_data')
swe.set_ephe_path(ephe_path)
swe.set_sid_mode(swe.SIDM_LAHIRI)  # Lahiri ayanamsa

# Import constants
try:
    from constants import (
        RASHIS, 
        NAKSHATRAS, 
        get_nakshatra_from_longitude,
        get_rashi_from_longitude,
        get_house_from_longitude
    )
except ImportError:
    # Fallback if not imported as module
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from constants import (
        RASHIS,
        NAKSHATRAS,
        get_nakshatra_from_longitude,
        get_rashi_from_longitude,
        get_house_from_longitude
    )

# Simple file-based storage (will migrate to PostgreSQL later)
CHARTS_DIR = os.path.join(os.path.dirname(__file__), '.charts_cache')
os.makedirs(CHARTS_DIR, exist_ok=True)


def calculate_chart(data):
    """
    Calculate complete birth chart
    
    Args:
        data: dict with datetime, latitude, longitude, timezone, name (optional)
    
    Returns:
        dict with chart_id and all planetary positions
    """
    try:
        # Parse datetime
        dt_str = data['datetime']
        if dt_str.endswith('Z'):
            dt_str = dt_str[:-1] + '+00:00'
        dt = datetime.fromisoformat(dt_str)
        
        # Convert to Julian day (UT)
        jd = swe.julday(
            dt.year, dt.month, dt.day,
            dt.hour + dt.minute/60.0 + dt.second/3600.0
        )
        
        # Calculate ascendant
        lat = data['latitude']
        lon = data['longitude']
        
        # Get houses (returns tuple of cusps and ascmc)
        houses_result = swe.houses(jd, lat, lon, b'P')  # Placidus for calculation
        ascendant_tropical = houses_result[1][0]  # ARMC
        
        # Convert to sidereal
        ayanamsa = swe.get_ayanamsa_ut(jd)
        ascendant_sidereal = (ascendant_tropical - ayanamsa) % 360
        
        # Calculate planetary positions
        planets = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mars': swe.MARS,
            'Mercury': swe.MERCURY,
            'Jupiter': swe.JUPITER,
            'Venus': swe.VENUS,
            'Saturn': swe.SATURN,
            'Rahu': swe.TRUE_NODE,
        }
        
        positions = {}
        
        for name, planet_id in planets.items():
            result = swe.calc_ut(jd, planet_id, swe.FLG_SIDEREAL)
            longitude = result[0][0]  # First element of position tuple
            speed = result[0][3]
            
            rashi = get_rashi_from_longitude(longitude)
            nakshatra, pada, nak_lord = get_nakshatra_from_longitude(longitude)
            house = get_house_from_longitude(longitude, ascendant_sidereal)
            
            positions[name] = {
                'longitude': round(longitude, 6),
                'rashi': rashi,
                'degree_in_rashi': round(longitude % 30, 2),
                'nakshatra': nakshatra,
                'nakshatra_pada': pada,
                'nakshatra_lord': nak_lord,
                'house': house,
                'is_retrograde': speed < 0
            }
        
        # Calculate Ketu (opposite of Rahu)
        rahu_long = positions['Rahu']['longitude']
        ketu_long = (rahu_long + 180) % 360
        
        positions['Ketu'] = {
            'longitude': round(ketu_long, 6),
            'rashi': get_rashi_from_longitude(ketu_long),
            'degree_in_rashi': round(ketu_long % 30, 2),
            'nakshatra': get_nakshatra_from_longitude(ketu_long)[0],
            'nakshatra_pada': get_nakshatra_from_longitude(ketu_long)[1],
            'nakshatra_lord': get_nakshatra_from_longitude(ketu_long)[2],
            'house': get_house_from_longitude(ketu_long, ascendant_sidereal),
            'is_retrograde': False
        }
        
        # Generate chart ID
        chart_id = str(uuid.uuid4())
        
        # Build chart data
        chart_data = {
            'chart_id': chart_id,
            'name': data.get('name', 'Unnamed'),
            'datetime': data['datetime'],
            'latitude': lat,
            'longitude': lon,
            'timezone': data.get('timezone', 'UTC'),
            'ascendant': {
                'longitude': round(ascendant_sidereal, 6),
                'rashi': get_rashi_from_longitude(ascendant_sidereal),
                'degree': round(ascendant_sidereal % 30, 2)
            },
            'planets': positions,
            'ayanamsa': round(ayanamsa, 6),
            'julian_day': jd
        }
        
        # Save to file cache
        cache_file = os.path.join(CHARTS_DIR, f'{chart_id}.json')
        with open(cache_file, 'w') as f:
            json.dump(chart_data, f, indent=2)
        
        return chart_data
        
    except Exception as e:
        import traceback
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }


def read_chart(chart_id):
    """Read a chart from cache by ID"""
    try:
        cache_file = os.path.join(CHARTS_DIR, f'{chart_id}.json')
        if not os.path.exists(cache_file):
            return {'error': f'Chart {chart_id} not found'}
        
        with open(cache_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {'error': str(e)}


def list_charts():
    """List all saved charts"""
    try:
        charts = []
        for filename in os.listdir(CHARTS_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(CHARTS_DIR, filename), 'r') as f:
                    chart = json.load(f)
                    charts.append({
                        'chart_id': chart['chart_id'],
                        'name': chart['name'],
                        'datetime': chart['datetime']
                    })
        return {'charts': charts}
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    try:
        # Read input from command line
        input_data = json.loads(sys.argv[1])
        
        action = input_data.get('action', 'create')
        
        if action == 'create':
            result = calculate_chart(input_data)
        elif action == 'read':
            result = read_chart(input_data['chart_id'])
        elif action == 'list':
            result = list_charts()
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
