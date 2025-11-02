import swisseph as swe
import sys

swe.set_ephe_path('./ephemeris_data')
jd = swe.julday(1990, 6, 15, 14.5)
sun = swe.calc_ut(jd, swe.SUN)
print(f"Sun: {sun[0]}")
