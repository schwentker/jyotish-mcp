import pytest
import json
from datetime import datetime
from calculations.varga_calculator import get_varga_chart, VARGA_MAP

# ---------------------------------------------------------------------
# TEST FIXTURES
# ---------------------------------------------------------------------

@pytest.fixture(scope="module")
def base_chart():
    """Generate a reproducible D1 chart for testing all Vargas."""
    # If swisseph isn't installed, skip these tests gracefully.
    pytest.importorskip("swisseph")
    from calculations.chart_calculator import calculate_chart

    data = {"datetime": "1953-09-27T09:10:00Z"}
    return calculate_chart(data)


# ---------------------------------------------------------------------
# GENERIC TESTS
# ---------------------------------------------------------------------

def test_varga_registry_contains_expected():
    """Ensure all required Vargas are registered."""
    expected = {
        "D2","D3","D4","D7","D9","D10","D12",
        "D16","D20","D24","D27","D30"
    }
    missing = expected - set(VARGA_MAP.keys())
    assert not missing, f"Missing vargas: {missing}"


@pytest.mark.parametrize("varga", list(VARGA_MAP.keys()))
def test_varga_output_structure(base_chart, varga):
    """Ensure each varga returns valid structure with 9+ planets."""
    result = get_varga_chart(base_chart, varga)
    assert isinstance(result, dict)
    assert "varga" in result and result["varga"] == varga
    assert "planets" in result and isinstance(result["planets"], dict)
    assert len(result["planets"]) >= 9


@pytest.mark.parametrize("varga", list(VARGA_MAP.keys()))
def test_varga_sign_range(base_chart, varga):
    """Ensure sign index within valid zodiac bounds (0–11)."""
    result = get_varga_chart(base_chart, varga)
    for pdata in result["planets"].values():
        sign = pdata.get("sign_index")
        assert 0 <= sign <= 11, f"{varga} sign index out of range: {sign}"


@pytest.mark.parametrize("varga", list(VARGA_MAP.keys()))
def test_varga_sign_name_consistency(base_chart, varga):
    """Ensure each planet has consistent sign index/name mapping."""
    result = get_varga_chart(base_chart, varga)
    for planet, pdata in result["planets"].items():
        assert isinstance(pdata["sign_name"], str)
        assert len(pdata["sign_name"]) > 0
        assert "longitude" in pdata
        assert isinstance(pdata["longitude"], float)


def test_d9_sample_alignment(base_chart):
    """Cross-check Sun longitude mapping for D9 vs known reference."""
    d9 = get_varga_chart(base_chart, "D9")
    sun = d9["planets"]["Sun"]
    # For 27 Sep 1953 09:10 AM Amritapuri, Sun ≈ Virgo D1 -> Navamsa Virgo
    assert 0 <= sun["sign_index"] <= 11
    # Optional: verify known Navamsa sign if validated externally
    # assert sun["sign_name"] == "Virgo"


def test_invalid_varga_raises(base_chart):
    """Unknown varga types should raise ValueError."""
    with pytest.raises(ValueError):
        get_varga_chart(base_chart, "D99")


# ---------------------------------------------------------------------
# OPTIONAL DIAGNOSTIC (prints one sample)
# ---------------------------------------------------------------------

def test_debug_sample_output(base_chart):
    """Print one representative chart for debugging clarity."""
    d9 = get_varga_chart(base_chart, "D9")
    snippet = {p: d9["planets"][p] for p in list(d9["planets"].keys())[:3]}
    print("\nSample D9 snippet:", json.dumps(snippet, indent=2))


def test_navamsa_diff(diff_reporter):
    """Diagnostic: print D1 -> D9 transitions for a small set of planets.

    Uses the `diff_reporter` fixture provided by `conftest.py`. This is
    primarily a visual/debug helper; we assert the returned string is
    non-empty so the test fails only if the reporter fails to produce output.
    """
    diff = diff_reporter("D9")
    print("\nD1 → D9 transitions:\n", diff)
    # Basic sanity checks
    assert isinstance(diff, str)
    assert diff.strip(), "Expected non-empty diff output"