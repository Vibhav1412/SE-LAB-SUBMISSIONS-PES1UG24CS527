"""
Code Coverage Test Suite for Irrigation Scheduler Application
Target: Achieve >90% (100%) Line / Code Coverage
Module Under Test: irrigation_scheduler.py
"""

import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# =====================================================================
# Code Coverage Tests: should_irrigate()
# =====================================================================

def test_code_cov_high_moisture():
    """Execute line 2-3: moisture >= 60 returns False."""
    assert should_irrigate(70, 0, "seedling") is False


def test_code_cov_heavy_rain():
    """Execute line 4-5: rain_mm >= 10 returns False."""
    assert should_irrigate(50, 15, "seedling") is False


def test_code_cov_seedling_irrigate():
    """Execute lines 6-8: stage == 'seedling' and moisture < 45 returns True."""
    assert should_irrigate(30, 2, "seedling") is True


def test_code_cov_seedling_no_irrigate():
    """Execute line 9: stage == 'seedling' and moisture >= 45 returns False."""
    assert should_irrigate(50, 2, "seedling") is False


def test_code_cov_flowering():
    """Execute lines 10-11: stage == 'flowering' returns moisture < 55."""
    assert should_irrigate(50, 2, "flowering") is True


def test_code_cov_other_stage_moderate_rain():
    """Execute lines 12-13: rain_mm >= 5 returns False for other stages."""
    assert should_irrigate(30, 6, "vegetative") is False


def test_code_cov_other_stage_low_rain():
    """Execute line 14: other stages return moisture < 40."""
    assert should_irrigate(35, 2, "vegetative") is True


# =====================================================================
# Code Coverage Tests: water_volume()
# =====================================================================

def test_code_cov_invalid_area_raises_value_error():
    """Execute lines 18-19: area_m2 <= 0 raises ValueError."""
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)


def test_code_cov_seedling_stage_volume():
    """Execute lines 20-21: stage == 'seedling' sets base litres = 2."""
    assert water_volume(10, "seedling", 20) == 20


def test_code_cov_flowering_stage_volume():
    """Execute lines 22-23: stage == 'flowering' sets base litres = 5."""
    assert water_volume(10, "flowering", 20) == 50


def test_code_cov_other_stage_volume():
    """Execute lines 24-25: else sets base litres = 4."""
    assert water_volume(10, "vegetative", 20) == 40


def test_code_cov_high_temp_multiplier():
    """Execute lines 26-27: temp_c > 35 multiplies litres by 1.5."""
    assert water_volume(10, "seedling", 40) == 30.0


def test_code_cov_low_temp_multiplier():
    """Execute lines 28-29: temp_c < 10 multiplies litres by 0.5."""
    assert water_volume(10, "seedling", 5) == 10.0


# =====================================================================
# Code Coverage Tests: schedule()
# =====================================================================

def test_code_cov_schedule_execution():
    """
    Execute lines 34-43:
    - lines 34-35: plan initialized and loop over zones
    - lines 36-37: zone not requiring irrigation is skipped (continue)
    - line 38: need calculated
    - line 39-40: budget exceeded breaks loop
    - lines 41-42: budget deducted and name appended to plan
    - line 43: return plan
    """
    zones = [
        ("ZoneA", 10, 30, 0, "seedling", 20),     # needs 20L <= 100L -> added, budget = 80L
        ("ZoneB", 10, 80, 0, "seedling", 20),     # should_irrigate is False -> skipped (continue)
        ("ZoneC", 20, 30, 0, "flowering", 20),    # needs 100L > 80L -> breaks loop
    ]
    assert schedule(zones, 100) == ["ZoneA"]
