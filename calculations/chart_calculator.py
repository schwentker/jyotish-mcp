#!/usr/bin/env python3
import sys
import json
import swisseph as swe
from datetime import datetime
import os

# Set ephemeris path
ephe_path = os.path.join(os.path.dirname(__file__), 'ephemeris_data')
swe.set_ephe_path(ephe_path)

def calculate_chart(data):
    """Calculate birth chart positions"""
    # Parse datetime
    dt = datetime.fromisoformat(data['datetime'].replace('Z', '+00:00'))
    
    # Convert to Julian day
    jd = swe.julday(dt.year, dt.month, dt.day, 
                    dt.hour + dt.minute/60.0 + dt.second/3600.0)
    
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
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    for name, planet_id in planets.items():
        result = swe.calc_ut(jd, planet_id)
        # result is ((longitude, speed, distance, ...), flags)
        longitude = result[0][0]
        
        # Convert to sign and degree
        sign_num = int(longitude / 30)
        degree = longitude % 30
        
        positions[name] = {
            'longitude': longitude,
            'sign': signs[sign_num],
            'degree': degree
        }
    
    # Calculate Ketu (opposite of Rahu)
    rahu_long = positions['Rahu']['longitude']
    ketu_long = (rahu_long + 180) % 360
    ketu_sign_num = int(ketu_long / 30)
    
    positions['Ketu'] = {
        'longitude': ketu_long,
        'sign': signs[ketu_sign_num],
        'degree': ketu_long % 30
    }
    
    return {
        'chart_id': data.get('name', 'unnamed'),
        'datetime': data['datetime'],
        'positions': positions
    }

if __name__ == '__main__':
    try:
        # Read input from command line
        input_data = json.loads(sys.argv[1])
        result = calculate_chart(input_data)
        print(json.dumps(result))
    except Exception as e:
        import traceback
        print(json.dumps({'error': str(e), 'traceback': traceback.format_exc()}), file=sys.stderr)
        sys.exit(1)
