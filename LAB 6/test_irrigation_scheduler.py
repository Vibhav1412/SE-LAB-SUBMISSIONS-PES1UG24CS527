"""
Test suite for irrigation_scheduler.py
Covers both line coverage and branch coverage (>90%, achieving 100%).
"""

import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# =====================================================================
# Unit Tests for should_irrigate()
# =====================================================================

def test_wet_soil_no_irrigation():
    """Moisture >= 60 suppresses irrigation (upper threshold boundary)."""
    assert should_irrigate(70, 0, "seedling") is False
    assert should_irrigate(60, 0, "seedling") is False


def test_heavy_rain_no_irrigation():
    """Rain >= 10mm suppresses irrigation across all crop stages."""
    assert should_irrigate(50, 12, "seedling") is False
    assert should_irrigate(50, 10, "seedling") is False


def test_seedling_dry_irrigation():
    """Seedling stage with moisture < 45 needs irrigation."""
    assert should_irrigate(30, 2, "seedling") is True
    assert should_irrigate(44, 2, "seedling") is True


def test_seedling_sufficient_moisture_no_irrigation():
    """Seedling stage with moisture >= 45 does not need irrigation."""
    assert should_irrigate(45, 2, "seedling") is False
    assert should_irrigate(50, 2, "seedling") is False


def test_flowering_dry_irrigation():
    """Flowering stage with moisture < 55 needs irrigation."""
    assert should_irrigate(50, 2, "flowering") is True
    assert should_irrigate(54, 2, "flowering") is True


def test_flowering_sufficient_moisture_no_irrigation():
    """Flowering stage with moisture >= 55 does not need irrigation."""
    assert should_irrigate(55, 2, "flowering") is False
    assert should_irrigate(58, 2, "flowering") is False


def test_other_stage_moderate_rain_no_irrigation():
    """Other stages with rain >= 5mm suppress irrigation."""
    assert should_irrigate(30, 5, "vegetative") is False
    assert should_irrigate(30, 6, "vegetative") is False


def test_other_stage_dry_irrigation():
    """Other stages with moisture < 40 and rain < 5mm need irrigation."""
    assert should_irrigate(35, 2, "vegetative") is True
    assert should_irrigate(39, 4, "vegetative") is True


def test_other_stage_sufficient_moisture_no_irrigation():
    """Other stages with moisture >= 40 do not need irrigation."""
    assert should_irrigate(40, 2, "vegetative") is False
    assert should_irrigate(45, 2, "vegetative") is False


# =====================================================================
# Unit Tests for water_volume()
# =====================================================================

def test_water_volume_zero_or_negative_area():
    """Area <= 0 must raise ValueError."""
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(-10, "flowering", 20)


def test_water_volume_stages():
    """Test base litres by crop stage."""
    # Seedling: base 2 L/m2
    assert water_volume(10, "seedling", 20) == 20
    # Flowering: base 5 L/m2
    assert water_volume(10, "flowering", 20) == 50
    # Other stage: base 4 L/m2
    assert water_volume(10, "vegetative", 20) == 40


def test_water_volume_temperature_adjustments():
    """Test temperature multiplier thresholds."""
    # Hot (> 35C): 1.5x multiplier
    assert water_volume(10, "seedling", 36) == 30.0
    # Cold (< 10C): 0.5x multiplier
    assert water_volume(10, "seedling", 9) == 10.0
    # Nominal boundaries: exactly 35C and 10C have no multiplier
    assert water_volume(10, "seedling", 35) == 20.0
    assert water_volume(10, "seedling", 10) == 20.0


# =====================================================================
# Unit Tests for schedule()
# =====================================================================

def test_schedule_empty_zones():
    """Empty zones list returns empty plan."""
    assert schedule([], 100) == []


def test_schedule_all_zones_within_budget():
    """Normal scheduling when all zones fit within budget."""
    zones = [
        ("ZoneA", 10, 30, 0, "seedling", 20),      # need = 20L
        ("ZoneB", 10, 20, 0, "vegetative", 20),    # need = 40L
    ]
    assert schedule(zones, 100) == ["ZoneA", "ZoneB"]


def test_schedule_skips_non_irrigated_zones():
    """Zones where should_irrigate evaluates to False are skipped."""
    zones = [
        ("ZoneA", 10, 70, 0, "seedling", 20),      # skipped
        ("ZoneB", 10, 20, 0, "seedling", 20),      # scheduled
    ]
    assert schedule(zones, 100) == ["ZoneB"]


def test_schedule_budget_exceeded_break():
    """Scheduling terminates when zone requirement exceeds remaining budget."""
    zones = [
        ("ZoneA", 10, 30, 0, "seedling", 20),   # 20L <= 40L -> added, budget = 20L
        ("ZoneB", 10, 30, 0, "flowering", 25),  # 50L > 20L -> break
        ("ZoneC", 5, 20, 0, "seedling", 20),    # not reached
    ]
    assert schedule(zones, 40) == ["ZoneA"]


def test_schedule_exact_budget_match():
    """Zone requirement matches available budget exactly."""
    zones = [
        ("ZoneA", 10, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 20) == ["ZoneA"]
