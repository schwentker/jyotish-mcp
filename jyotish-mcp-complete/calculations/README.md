# Jyotish Calculation Engine

Python-based astronomical and Jyotish calculations using Swiss Ephemeris.

## ✅ Verify Your Setup

After installing dependencies and downloading ephemeris files:

```bash
# Activate virtual environment
source venv/bin/activate

# Run verification test
python test_ephemeris.py
```

This will calculate Her's birth chart and verify Swiss Ephemeris is working!

## Setup

```bash
# Create virtual environment (use Python 3.12!)
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download Swiss Ephemeris data (HTTPS - fast!)
cd ephemeris_data
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sefstars.txt
cd ..
```

## Files

- **constants.py** - All Jyotish reference data ✅
- **test_ephemeris.py** - Verification test ✅
- **requirements.txt** - Python dependencies ✅
- **ephemeris_data/** - Swiss Ephemeris files (4 files needed)

**To be built:**
- ephemeris.py - Swiss Ephemeris wrapper
- chart_calculator.py - Main orchestrator
- nakshatras.py - Nakshatra calculator
- dashas.py - Vimshottari Dasha
- houses.py - Whole Sign houses
- database.py - PostgreSQL interface

## Quick Test

```python
import swisseph as swe
from constants import get_nakshatra_from_longitude

swe.set_ephe_path('./ephemeris_data')
swe.set_sid_mode(swe.SIDM_LAHIRI)

jd = swe.julday(1953, 9, 27, 3.669)
moon_long = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0]

nakshatra, pada, lord = get_nakshatra_from_longitude(moon_long)
print(f"Moon: {moon_long:.2f}° in {nakshatra} pada {pada}")
```

## Standards

- **Ayanamsa:** Lahiri
- **Houses:** Whole Sign
- **Aspects:** Traditional Parashari
- **Dasha:** Vimshottari
- **Nakshatras:** 27 (Abhijit excluded)

See [main README](../README.md) for complete standards.
