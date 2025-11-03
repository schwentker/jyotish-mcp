# Jyotish Calculation Engine

Python-based astronomical and Jyotish calculations using Swiss Ephemeris.

## Overview

This directory contains the core calculation engine for Vedic astrology computations:

- **Astronomical calculations:** Swiss Ephemeris integration for precise planetary positions
- **Jyotish algorithms:** Nakshatras, Dashas, Vargas, Aspects, Yogas
- **Database interface:** PostgreSQL storage for charts and calculations

## Structure

```
calculations/
├── constants.py           # Jyotish reference data (rashis, nakshatras, etc.)
├── ephemeris.py          # Swiss Ephemeris wrapper (TBD)
├── nakshatras.py         # Nakshatra calculations (TBD)
├── houses.py             # House system (Whole Sign) (TBD)
├── dashas.py             # Vimshottari Dasha calculator (TBD)
├── vargas.py             # Divisional charts (TBD)
├── aspects.py            # Planetary aspects (TBD)
├── yogas.py              # Classical yoga identification (TBD)
├── chart_calculator.py   # Main orchestrator (TBD)
├── database.py           # Database interface (TBD)
├── models.py             # SQLAlchemy models (TBD)
└── ephemeris_data/       # Swiss Ephemeris files (download separately)
```

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download Swiss Ephemeris data
mkdir -p ephemeris_data
cd ephemeris_data
wget ftp://ftp.astro.com/pub/swisseph/ephe/sepl_18.se1
wget ftp://ftp.astro.com/pub/swisseph/ephe/semo_18.se1
wget ftp://ftp.astro.com/pub/swisseph/ephe/seas_18.se1
```

## Quick Test

```python
import swisseph as swe
from constants import get_nakshatra_from_longitude

# Initialize
swe.set_ephe_path('./ephemeris_data')
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Calculate Moon position (example: Sep 27, 1953, 9:10 AM IST)
jd = swe.julday(1953, 9, 27, 3.669)  # 9:10 AM - 5:30 = 3:40 AM UT
moon_long = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0]

# Get nakshatra
nakshatra, pada, lord = get_nakshatra_from_longitude(moon_long)
print(f"Moon at {moon_long:.2f}° in {nakshatra} pada {pada}, ruled by {lord}")
```

## Development

```bash
# Format code
black .

# Lint
ruff check .

# Type check
mypy .

# Run tests
pytest -v
```

## Calculation Standards

All calculations follow traditional Parashari Vedic astrology:

- **Ayanamsa:** Lahiri (Chitrapaksha)
- **House System:** Whole Sign
- **Aspects:** Traditional full aspects (7th for all, special for Mars/Jupiter/Saturn)
- **Dasha System:** Vimshottari (120-year cycle)
- **Nakshatras:** 27 lunar mansions
- **Vargas:** D1-D60 divisional charts

See main [README.md](../README.md) for detailed standards.

## Validation

All calculations validated against:
- JHora (Windows freeware)
- Established commercial software
- Classical text examples

Tolerance: ±1 arc-minute for planetary positions

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE) for details.

Note: Swiss Ephemeris requires separate licensing for commercial use.
