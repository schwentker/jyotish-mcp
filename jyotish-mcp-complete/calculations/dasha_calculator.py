#!/usr/bin/env python3
"""
Dasha Calculator - Vimshottari Dasha system calculations
"""

import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Import constants
try:
    from constants import (
        DASHA_PERIODS,
        DASHA_SEQUENCE,
        NAKSHATRA_DASHA_LORDS,
        get_nakshatra_from_longitude
    )
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from constants import (
        DASHA_PERIODS,
        DASHA_SEQUENCE,
        NAKSHATRA_DASHA_LORDS,
        get_nakshatra_from_longitude
    )

# Chart cache directory
CHARTS_DIR = os.path.join(os.path.dirname(__file__), '.charts_cache')


def calculate_dasha_balance(moon_longitude):
    """
    Calculate the balance of Maha Dasha at birth
    
    Args:
        moon_longitude: Moon's longitude in degrees
    
    Returns:
        dict with planet, years, months, days remaining
    """
    # Get nakshatra
    nakshatra_name, pada, lord = get_nakshatra_from_longitude(moon_longitude)
    
    # Find nakshatra index (0-26)
    nakshatra_index = None
    for i, nak_data in enumerate(eval(str(NAKSHATRAS)) if isinstance(NAKSHATRAS, str) else NAKSHATRAS):
        if isinstance(nak_data, dict) and nak_data['name'] == nakshatra_name:
            nakshatra_index = i
            break
    
    if nakshatra_index is None:
        # Fallback: calculate from longitude
        nakshatra_index = int(moon_longitude / (360 / 27))
    
    # Get Dasha lord for this nakshatra
    dasha_lord = NAKSHATRA_DASHA_LORDS[nakshatra_index]
    
    # Calculate position within nakshatra (0-13.333 degrees)
    nakshatra_span = 360 / 27  # 13.333...
    nakshatra_start = nakshatra_index * nakshatra_span
    position_in_nak = moon_longitude - nakshatra_start
    
    # Calculate proportion traveled
    proportion_traveled = position_in_nak / nakshatra_span
    
    # Total years for this Dasha
    total_years = DASHA_PERIODS[dasha_lord]
    
    # Years elapsed
    years_elapsed = total_years * proportion_traveled
    
    # Balance remaining
    years_remaining = total_years - years_elapsed
    
    # Convert to years, months, days
    years = int(years_remaining)
    fractional_year = years_remaining - years
    months = int(fractional_year * 12)
    days = int((fractional_year * 12 - months) * 30)
    
    return {
        'planet': dasha_lord,
        'years': years,
        'months': months,
        'days': days,
        'total_days': int(years_remaining * 365.25)
    }


def generate_dasha_periods(birth_datetime, moon_longitude, num_years=120):
    """
    Generate complete Vimshottari Dasha periods
    
    Args:
        birth_datetime: Birth datetime string
        moon_longitude: Moon's longitude
        num_years: Number of years to generate (default 120)
    
    Returns:
        list of Maha Dasha periods with Antar Dashas
    """
    # Parse birth datetime
    if birth_datetime.endswith('Z'):
        birth_datetime = birth_datetime[:-1] + '+00:00'
    birth_dt = datetime.fromisoformat(birth_datetime)
    
    # Get birth balance
    balance = calculate_dasha_balance(moon_longitude)
    
    # Find starting Dasha lord index
    start_lord = balance['planet']
    start_index = DASHA_SEQUENCE.index(start_lord)
    
    # Start date adjusted for balance already elapsed
    current_date = birth_dt
    
    maha_dashas = []
    
    # Generate Maha Dashas
    for i in range(9):  # 9 planets in Vimshottari
        lord_index = (start_index + i) % 9
        lord = DASHA_SEQUENCE[lord_index]
        period_years = DASHA_PERIODS[lord]
        
        # For first Dasha, use remaining balance
        if i == 0:
            period_years = balance['years'] + balance['months']/12 + balance['days']/365.25
        
        period_days = int(period_years * 365.25)
        end_date = current_date + timedelta(days=period_days)
        
        # Generate Antar Dashas
        antar_dashas = []
        antar_start = current_date
        
        for j in range(9):
            antar_lord_index = (lord_index + j) % 9
            antar_lord = DASHA_SEQUENCE[antar_lord_index]
            
            # Antar period = (Maha period * Antar lord years) / 120
            antar_years = (period_years * DASHA_PERIODS[antar_lord]) / 120
            antar_days = int(antar_years * 365.25)
            antar_end = antar_start + timedelta(days=antar_days)
            
            antar_dashas.append({
                'planet': antar_lord,
                'start_date': antar_start.isoformat(),
                'end_date': antar_end.isoformat(),
                'duration_years': round(antar_years, 2)
            })
            
            antar_start = antar_end
        
        maha_dashas.append({
            'planet': lord,
            'start_date': current_date.isoformat(),
            'end_date': end_date.isoformat(),
            'duration_years': round(period_years, 2),
            'antar_dashas': antar_dashas
        })
        
        current_date = end_date
    
    return {
        'birth_balance': balance,
        'maha_dashas': maha_dashas[:9]  # All 9 Maha Dashas
    }


def get_current_dasha(chart_id, date=None):
    """
    Get current running Dasha periods
    
    Args:
        chart_id: Chart UUID
        date: Optional date (defaults to now)
    
    Returns:
        dict with current Maha, Antar, and Pratyantar Dashas
    """
    try:
        # Load chart
        cache_file = os.path.join(CHARTS_DIR, f'{chart_id}.json')
        if not os.path.exists(cache_file):
            return {'error': f'Chart {chart_id} not found'}
        
        with open(cache_file, 'r') as f:
            chart = json.load(f)
        
        # Get Moon position
        moon_long = chart['planets']['Moon']['longitude']
        birth_datetime = chart['datetime']
        
        # Generate Dasha periods
        dashas = generate_dasha_periods(birth_datetime, moon_long)
        
        # Determine current date
        if date:
            if date.endswith('Z'):
                date = date[:-1] + '+00:00'
            current_dt = datetime.fromisoformat(date)
        else:
            current_dt = datetime.now()
        
        # Find current Maha Dasha
        current_maha = None
        current_antar = None
        
        for maha in dashas['maha_dashas']:
            maha_start = datetime.fromisoformat(maha['start_date'].replace('Z', '+00:00'))
            maha_end = datetime.fromisoformat(maha['end_date'].replace('Z', '+00:00'))
            
            if maha_start <= current_dt <= maha_end:
                current_maha = maha
                
                # Find current Antar Dasha
                for antar in maha['antar_dashas']:
                    antar_start = datetime.fromisoformat(antar['start_date'].replace('Z', '+00:00'))
                    antar_end = datetime.fromisoformat(antar['end_date'].replace('Z', '+00:00'))
                    
                    if antar_start <= current_dt <= antar_end:
                        current_antar = antar
                        break
                
                break
        
        if not current_maha:
            return {'error': 'No current Dasha found for this date'}
        
        return {
            'current_date': current_dt.isoformat(),
            'maha_dasha': {
                'planet': current_maha['planet'],
                'start_date': current_maha['start_date'],
                'end_date': current_maha['end_date'],
                'duration_years': current_maha['duration_years']
            },
            'antar_dasha': current_antar if current_antar else None,
            'birth_balance': dashas['birth_balance']
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
            result = get_current_dasha(
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
