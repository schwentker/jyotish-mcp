#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime
import swisseph as swe
from .varga_calculator import get_varga_chart

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------

# Set ephemeris path
ephe_path = os.path.join(os.path.dirname(__file__), 'ephemeris_data')
import os
ephe_path = os.getenv(
    "SWISSEPH_PATH",
    os.path.join(os.path.dirname(__file__), "ephemeris_data")
)

swe.set_ephe_path(ephe_path)

SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.TRUE_NODE,  # Mean or True Node depending on preference
}

# ---------------------------------------------------------------------
# CORE COMPUTATION
# ---------------------------------------------------------------------

def get_planet_positions(dt: datetime):
    """
    Compute raw planetary longitudes for all grahas (planets).
    Returns a dict of planet data: { 'Sun': {'longitude': .., 'sign': .., 'degree': ..}, ... }
    """
    jd = swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    )

    positions = {}
    for name, pid in PLANETS.items():
        result = swe.calc_ut(jd, pid)
        longitude = result[0][0]
        sign_num = int(longitude / 30)
        degree = longitude % 30
        positions[name] = {
            'longitude': longitude,
            'sign': SIGNS[sign_num],
            'degree': degree
        }

    # Add Ketu (always opposite Rahu)
    rahu_long = positions['Rahu']['longitude']
    ketu_long = (rahu_long + 180) % 360
    ketu_sign_num = int(ketu_long / 30)
    positions['Ketu'] = {
        'longitude': ketu_long,
        'sign': SIGNS[ketu_sign_num],
        'degree': ketu_long % 30
    }

    return positions


def calculate_chart(data):
    """
    Calculate base D1 (Rashi) chart positions.
    Input: dict with 'datetime' (ISO string)
    Output: chart dict with planetary positions
    """
    dt = datetime.fromisoformat(data['datetime'].replace('Z', '+00:00'))
    positions = get_planet_positions(dt)

    return {
        'chart_id': data.get('name', 'unnamed'),
        'varga': 'D1',
        'datetime': data['datetime'],
        'positions': positions
    }


def calculate_varga_chart(data, varga_type="D1"):
    """
    Dispatcher: calculates D1 or any divisional chart.
    Delegates to varga_calculator for D2–D60.
    """
    base_chart = calculate_chart(data)

    if varga_type == "D1":
        return base_chart
    else:
        # Convert base chart structure for varga projection
        return get_varga_chart(base_chart, varga_type)


# ---------------------------------------------------------------------
# CLI ENTRY POINT
# ---------------------------------------------------------------------

if __name__ == '__main__':
    """
    Command-line usage example:
    python -m calculations.chart_calculator '{"datetime":"1953-09-27T09:10:00Z","varga":"D9"}'
    """
    try:
        input_data = json.loads(sys.argv[1])

        varga_type = input_data.get('varga', 'D1')
        result = calculate_varga_chart(input_data, varga_type)

        print(json.dumps(result, indent=2))

    except Exception as e:
        import traceback
        print(json.dumps({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), file=sys.stderr)
        sys.exit(1)