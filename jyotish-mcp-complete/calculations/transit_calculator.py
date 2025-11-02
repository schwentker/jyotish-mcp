#!/usr/bin/env python3
"""
Transit Calculator - Current planetary positions and transits
"""

import sys
import json
import os
import swisseph as swe
from datetime import datetime

# Set ephemeris path
ephe_path = os.path.join(os.path.dirname(__file__), 'ephemeris_data')
swe.set_ephe_path(ephe_path)
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Import constants
try:
    from constants import (
        get_nakshatra_from_longitude,
        get_rashi_from_longitude,
        get_house_from_longitude
    )
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from constants import (
        get_nakshatra_from_longitude,
        get_rashi_from_longitude,
        get_house_from_longitude
    )

# Chart cache
CHARTS_DIR = os.path.join(os.path.dirname(__file__), '.charts_cache')


def calculate_transits(chart_id, date=None):
    """
    Calculate current transits relative to birth chart
    
    Args:
        chart_id: Birth chart UUID
        date: Optional date (ISO format), defaults to now
    
    Returns:
        dict with current transit positions and house placements
    """
    try:
        # Load birth chart
        cache_file = os.path.join(CHARTS_DIR, f'{chart_id}.json')
        if not os.path.exists(cache_file):
            return {'error': f'Chart {chart_id} not found'}
        
        with open(cache_file, 'r') as f:
            birth_chart = json.load(f)
        
        # Get birth ascendant for house calculations
        birth_ascendant = birth_chart['ascendant']['longitude']
        
        # Determine transit date
        if date:
            if date.endswith('Z'):
                date = date[:-1] + '+00:00'
            transit_dt = datetime.fromisoformat(date)
        else:
            transit_dt = datetime.now()
        
        # Convert to Julian day
        jd = swe.julday(
            transit_dt.year, transit_dt.month, transit_dt.day,
            transit_dt.hour + transit_dt.minute/60.0 + transit_dt.second/3600.0
        )
        
        # Calculate current planetary positions
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
        
        transits = {}
        
        for name, planet_id in planets.items():
            result = swe.calc_ut(jd, planet_id, swe.FLG_SIDEREAL)
            longitude = result[0][0]
            speed = result[0][3]
            
            rashi = get_rashi_from_longitude(longitude)
            nakshatra, pada, nak_lord = get_nakshatra_from_longitude(longitude)
            house = get_house_from_longitude(longitude, birth_ascendant)
            
            # Get birth position for comparison
            birth_pos = birth_chart['planets'][name]
            birth_house = birth_pos['house']
            birth_rashi = birth_pos['rashi']
            
            transits[name] = {
                'longitude': round(longitude, 6),
                'rashi': rashi,
                'degree_in_rashi': round(longitude % 30, 2),
                'nakshatra': nakshatra,
                'nakshatra_pada': pada,
                'house': house,
                'is_retrograde': speed < 0,
                'birth_house': birth_house,
                'birth_rashi': birth_rashi,
                'house_from_birth': house,
                'speed': round(speed, 6)
            }
        
        # Calculate Ketu
        rahu_long = transits['Rahu']['longitude']
        ketu_long = (rahu_long + 180) % 360
        
        transits['Ketu'] = {
            'longitude': round(ketu_long, 6),
            'rashi': get_rashi_from_longitude(ketu_long),
            'degree_in_rashi': round(ketu_long % 30, 2),
            'nakshatra': get_nakshatra_from_longitude(ketu_long)[0],
            'nakshatra_pada': get_nakshatra_from_longitude(ketu_long)[1],
            'house': get_house_from_longitude(ketu_long, birth_ascendant),
            'is_retrograde': False,
            'birth_house': birth_chart['planets']['Ketu']['house'],
            'birth_rashi': birth_chart['planets']['Ketu']['rashi'],
            'house_from_birth': get_house_from_longitude(ketu_long, birth_ascendant),
            'speed': 0
        }
        
        return {
            'transit_date': transit_dt.isoformat(),
            'transits': transits,
            'birth_chart_id': chart_id
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
        action = input_data.get('action', 'current')
        
        if action == 'current':
            result = calculate_transits(
                input_data['chart_id'],
                input_data.get('date')
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
