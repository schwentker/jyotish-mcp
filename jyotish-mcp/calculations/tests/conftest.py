"""
conftest.py
-----------
Shared pytest fixtures for jyotish-mcp varga testing.

This module provides:
- `base_chart`: reusable D1 (Rashi) chart fixture
- `varga_chart_factory`: callable fixture to generate any D-chart
- `all_vargas`: param generator for looping tests
- Optional visual diff helper for debugging

Usage in tests:
    def test_navamsa(base_chart, varga_chart_factory):
        d9 = varga_chart_factory("D9")
        assert "Sun" in d9["planets"]
"""

import pytest
import json
from datetime import datetime
# Defer importing chart_calculator (which requires `swisseph`) until a fixture
# runs. This allows tests to be discovered even when the optional native
# dependency isn't installed; pytest can skip them cleanly.
from calculations.varga_calculator import get_varga_chart, VARGA_MAP


# ---------------------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------------------

@pytest.fixture(scope="session")
def test_datetime():
    """Canonical datetime for deterministic chart generation."""
    return "1953-09-27T09:10:00Z"  # Amma's birth time reference


@pytest.fixture(scope="session")
def base_chart(test_datetime):
    """Generate the base D1 chart once per test session."""
    # If swisseph isn't available, skip all tests that require real ephemeris
    pytest.importorskip("swisseph")

    # Now import the heavy chart calculator lazily
    from calculations.chart_calculator import calculate_chart

    data = {"datetime": test_datetime}
    chart = calculate_chart(data)
    assert "positions" in chart, "Base D1 chart must include planet positions"
    return chart


@pytest.fixture
def varga_chart_factory(base_chart):
    """
    Factory fixture that generates any requested varga chart.
    Example: varga_chart_factory("D9")
    """
    def _make(varga_type: str):
        return get_varga_chart(base_chart, varga_type)
    return _make


@pytest.fixture(scope="session")
def all_vargas():
    """Provide a list of all supported varga types from VARGA_MAP."""
    return list(VARGA_MAP.keys())


# ---------------------------------------------------------------------
# OPTIONAL UTILITIES
# ---------------------------------------------------------------------

def _compare_planet_signs(d1, dv, planet):
    """Helper: compare a planet's sign between D1 and Dn."""
    base = d1["positions"][planet]["sign"]
    varga = dv["planets"][planet]["sign_name"]
    return f"{planet}: {base} → {varga}"


@pytest.fixture
def diff_reporter(base_chart, varga_chart_factory):
    """
    Returns a helper function to print quick D1→Dn diffs for visual debugging.
    Example:
        diff = diff_reporter()
        print(diff("D9"))
    """
    def _diff(varga_type: str, limit: int = 5):
        dv = varga_chart_factory(varga_type)
        pairs = [
            _compare_planet_signs(base_chart, dv, p)
            for p in list(base_chart["positions"].keys())[:limit]
        ]
        return "\n".join(pairs)
    return _diff


# ---------------------------------------------------------------------
# AUTO-CONFIG
# ---------------------------------------------------------------------

def pytest_configure(config):
    """Add a custom marker for varga tests."""
    config.addinivalue_line("markers", "varga: mark a test as related to varga charts")


# Optional pretty printing toggle
@pytest.fixture(autouse=True, scope="session")
def set_json_indent():
    """Pretty-print JSON when debugging."""
    json.dumps({}, indent=2)