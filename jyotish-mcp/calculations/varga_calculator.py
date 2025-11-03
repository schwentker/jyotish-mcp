"""
varga_calculator.py
-------------------

Implements divisional chart (varga) calculations for Vedic astrology.

Each varga divides the 30° span of a zodiac sign into 'n' equal parts,
then maps planetary longitudes into new sign positions according to
classical Parashari rules.

References:
- Brihat Parashara Hora Shastra (BPHS)
- Sanjay Rath, "Crux of Vedic Astrology"
"""

import math
import uuid

# If these are defined elsewhere, you can import instead:
SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# ---------------------------------------------------------------------
# GENERIC UTILITIES
# ---------------------------------------------------------------------

def _basic_varga_sign(planet_long: float, n: int) -> int:
    """
    Generic Parashari varga division formula.
    Works for most Vargas (D4, D7, D9, D10, etc.)
    """
    sign_num = int(planet_long / 30)
    within_sign = planet_long % 30
    division = int(within_sign * n / 30)
    varga_sign = (sign_num * n + division) % 12
    return varga_sign


def _chart_template(varga_type: str) -> dict:
    """Return base structure for varga chart JSON."""
    return {"chart_id": str(uuid.uuid4()), "varga": varga_type, "planets": {}}


# ---------------------------------------------------------------------
# INDIVIDUAL VARGA CALCULATIONS
# ---------------------------------------------------------------------

def calculate_d9(base_chart: dict) -> dict:
    """D9 Navamsa chart — Dharma / relationships."""
    result = _chart_template("D9")
    for planet, pdata in base_chart["positions"].items():
        longi = pdata["longitude"]
        varga_sign = _basic_varga_sign(longi, 9)
        result["planets"][planet] = {
            "sign_index": varga_sign,
            "sign_name": SIGNS[varga_sign],
            "longitude": longi
        }
    return result


def calculate_d2(base_chart: dict) -> dict:
    """D2 Hora chart — Wealth (special odd/even rule)."""
    result = _chart_template("D2")
    for planet, pdata in base_chart["positions"].items():
        longi = pdata["longitude"]
        sign_num = int(longi / 30)
        within = longi % 30

        # Odd signs → 0–15° Sun Hora (Leo), 15–30° Moon Hora (Cancer)
        # Even signs → reversed
        if sign_num % 2 == 0:  # odd sign numbers = even signs (0=Aries)
            if within < 15:
                varga_sign = 4  # Leo
            else:
                varga_sign = 3  # Cancer
        else:
            if within < 15:
                varga_sign = 3
            else:
                varga_sign = 4

        result["planets"][planet] = {
            "sign_index": varga_sign,
            "sign_name": SIGNS[varga_sign],
            "longitude": longi
        }
    return result


def calculate_d3(base_chart: dict) -> dict:
    """D3 Drekkana chart — Siblings."""
    result = _chart_template("D3")
    for planet, pdata in base_chart["positions"].items():
        longi = pdata["longitude"]
        sign_num = int(longi / 30)
        within = longi % 30
        drekkana_num = int(within / 10)
        if sign_num % 2 == 0:
            varga_sign = (sign_num + drekkana_num) % 12
        else:
            varga_sign = (sign_num + (2 - drekkana_num)) % 12

        result["planets"][planet] = {
            "sign_index": varga_sign,
            "sign_name": SIGNS[varga_sign],
            "longitude": longi
        }
    return result


def calculate_regular_varga(base_chart: dict, n: int, label: str) -> dict:
    """For standard even-divided Vargas: D4, D7, D10, D12, D16, D20, D24, D27."""
    result = _chart_template(label)
    for planet, pdata in base_chart["positions"].items():
        longi = pdata["longitude"]
        varga_sign = _basic_varga_sign(longi, n)
        result["planets"][planet] = {
            "sign_index": varga_sign,
            "sign_name": SIGNS[varga_sign],
            "longitude": longi
        }
    return result


def calculate_d30(base_chart: dict) -> dict:
    """D30 Trimsamsa chart — Misfortunes (irregular divisions)."""
    result = _chart_template("D30")
    for planet, pdata in base_chart["positions"].items():
        longi = pdata["longitude"]
        sign_num = int(longi / 30)
        within = longi % 30

        # Trimsamsa divisions depend on odd/even sign
        # Odd signs: 0–5° Mars, 5–10° Saturn, 10–18° Jupiter, 18–25° Mercury, 25–30° Venus
        # Even signs reversed order
        if sign_num % 2 == 0:  # odd signs
            if within < 5:
                varga_sign = 0  # Aries (Mars)
            elif within < 10:
                varga_sign = 10  # Aquarius (Saturn)
            elif within < 18:
                varga_sign = 8   # Sagittarius (Jupiter)
            elif within < 25:
                varga_sign = 2   # Gemini (Mercury)
            else:
                varga_sign = 1   # Taurus (Venus)
        else:
            if within < 5:
                varga_sign = 1
            elif within < 10:
                varga_sign = 2
            elif within < 18:
                varga_sign = 8
            elif within < 25:
                varga_sign = 10
            else:
                varga_sign = 0

        result["planets"][planet] = {
            "sign_index": varga_sign,
            "sign_name": SIGNS[varga_sign],
            "longitude": longi
        }
    return result


# ---------------------------------------------------------------------
# DISPATCH MAP
# ---------------------------------------------------------------------

VARGA_MAP = {
    "D2": calculate_d2,
    "D3": calculate_d3,
    "D4": lambda c: calculate_regular_varga(c, 4, "D4"),
    "D7": lambda c: calculate_regular_varga(c, 7, "D7"),
    "D9": calculate_d9,
    "D10": lambda c: calculate_regular_varga(c, 10, "D10"),
    "D12": lambda c: calculate_regular_varga(c, 12, "D12"),
    "D16": lambda c: calculate_regular_varga(c, 16, "D16"),
    "D20": lambda c: calculate_regular_varga(c, 20, "D20"),
    "D24": lambda c: calculate_regular_varga(c, 24, "D24"),
    "D27": lambda c: calculate_regular_varga(c, 27, "D27"),
    "D30": calculate_d30,
    # You can later add D40, D45, D60 etc.
}


# ---------------------------------------------------------------------
# MAIN DISPATCHER
# ---------------------------------------------------------------------

def get_varga_chart(base_chart: dict, varga_type: str) -> dict:
    """
    Dispatcher for all divisional charts.
    base_chart: output from chart_calculator.calculate_chart()
    varga_type: e.g. "D9"
    """
    varga_type = varga_type.upper()
    if varga_type not in VARGA_MAP:
        raise ValueError(f"Unsupported varga type: {varga_type}")
    return VARGA_MAP[varga_type](base_chart)