"""
Branch Coverage Test Suite for Irrigation Scheduler Application
Target: Achieve 100% Branch Coverage and Boundary Value Coverage
Module Under Test: irrigation_scheduler.py
"""

import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# =====================================================================
# Branch Coverage Tests: should_irrigate()
# =====================================================================

class TestShouldIrrigateBranches:
    """Tests evaluating every decision outcome (True and False) in should_irrigate."""

    # 1. Branch: if moisture >= 60
    def test_moisture_at_upper_threshold_returns_false(self):
        """Boundary moisture == 60: triggers True branch -> returns False."""
        assert should_irrigate(60, 0, "seedling") is False

    def test_moisture_above_upper_threshold_returns_false(self):
        """Moisture > 60: triggers True branch -> returns False."""
        assert should_irrigate(85, 0, "seedling") is False

    def test_moisture_below_upper_threshold_continues(self):
        """Boundary moisture == 59: triggers False branch -> passes through."""
        # 59 with rain 15 should hit the next rain check
        assert should_irrigate(59, 15, "seedling") is False

    # 2. Branch: if rain_mm >= 10
    def test_rain_at_heavy_threshold_returns_false(self):
        """Boundary rain_mm == 10: triggers True branch -> returns False."""
        assert should_irrigate(30, 10, "seedling") is False

    def test_rain_above_heavy_threshold_returns_false(self):
        """Rain > 10: triggers True branch -> returns False."""
        assert should_irrigate(30, 25, "seedling") is False

    def test_rain_below_heavy_threshold_continues(self):
        """Boundary rain_mm == 9: triggers False branch -> passes through."""
        assert should_irrigate(30, 9, "seedling") is True

    # 3. Branch: if stage == "seedling"
    def test_seedling_stage_moisture_below_45_returns_true(self):
        """Seedling with moisture < 45 (boundary 44): returns True."""
        assert should_irrigate(44, 2, "seedling") is True

    def test_seedling_stage_moisture_at_45_returns_false(self):
        """Seedling with moisture == 45 (boundary): returns False."""
        assert should_irrigate(45, 2, "seedling") is False

    def test_seedling_stage_moisture_above_45_returns_false(self):
        """Seedling with moisture > 45 (e.g. 50): returns False."""
        assert should_irrigate(50, 2, "seedling") is False

    # 4. Branch: if stage == "flowering"
    def test_flowering_stage_moisture_below_55_returns_true(self):
        """Flowering with moisture < 55 (boundary 54): returns True."""
        assert should_irrigate(54, 2, "flowering") is True

    def test_flowering_stage_moisture_at_55_returns_false(self):
        """Flowering with moisture == 55 (boundary): returns False."""
        assert should_irrigate(55, 2, "flowering") is False

    def test_flowering_stage_moisture_above_55_returns_false(self):
        """Flowering with moisture > 55 (e.g. 58): returns False."""
        assert should_irrigate(58, 2, "flowering") is False

    # 5. Branch: other stage and rain_mm >= 5
    def test_other_stage_rain_at_threshold_returns_false(self):
        """Other stage with rain_mm == 5 (boundary): triggers True branch -> returns False."""
        assert should_irrigate(20, 5, "vegetative") is False

    def test_other_stage_rain_above_threshold_returns_false(self):
        """Other stage with rain_mm > 5 (e.g. 8): returns False."""
        assert should_irrigate(20, 8, "vegetative") is False

    def test_other_stage_rain_below_threshold_continues(self):
        """Other stage with rain_mm == 4 (boundary): passes to moisture check."""
        assert should_irrigate(35, 4, "vegetative") is True

    # 6. Branch: return moisture < 40
    def test_other_stage_moisture_below_40_returns_true(self):
        """Other stage with moisture < 40 (boundary 39): returns True."""
        assert should_irrigate(39, 2, "vegetative") is True

    def test_other_stage_moisture_at_40_returns_false(self):
        """Other stage with moisture == 40 (boundary): returns False."""
        assert should_irrigate(40, 2, "vegetative") is False

    def test_other_stage_moisture_above_40_returns_false(self):
        """Other stage with moisture > 40 (e.g. 48): returns False."""
        assert should_irrigate(48, 2, "vegetative") is False


# =====================================================================
# Branch Coverage Tests: water_volume()
# =====================================================================

class TestWaterVolumeBranches:
    """Tests evaluating every decision outcome and boundary condition in water_volume."""

    def test_area_zero_raises_value_error(self):
        """Boundary area == 0: triggers area <= 0 True branch."""
        with pytest.raises(ValueError, match="invalid area"):
            water_volume(0, "seedling", 20)

    def test_area_negative_raises_value_error(self):
        """Negative area: triggers area <= 0 True branch."""
        with pytest.raises(ValueError, match="invalid area"):
            water_volume(-5, "seedling", 20)

    def test_area_positive_continues(self):
        """Positive area: triggers area <= 0 False branch."""
        assert water_volume(1, "seedling", 20) == 2

    # Stage branches
    def test_stage_seedling_base_litres(self):
        """stage == 'seedling' sets base litres = 2."""
        assert water_volume(10, "seedling", 20) == 20

    def test_stage_flowering_base_litres(self):
        """stage == 'flowering' sets base litres = 5."""
        assert water_volume(10, "flowering", 20) == 50

    def test_stage_other_base_litres(self):
        """Any other stage falls to else branch, sets base litres = 4."""
        assert water_volume(10, "fruiting", 20) == 40

    # Temperature multiplier branches
    def test_temp_above_35_applies_multiplier(self):
        """temp_c > 35 (e.g. 36): applies 1.5x multiplier."""
        assert water_volume(10, "seedling", 36) == 30.0

    def test_temp_at_35_no_multiplier(self):
        """Boundary temp_c == 35: does not trigger > 35, normal rate."""
        assert water_volume(10, "seedling", 35) == 20.0

    def test_temp_below_10_applies_multiplier(self):
        """temp_c < 10 (e.g. 9): applies 0.5x multiplier."""
        assert water_volume(10, "seedling", 9) == 10.0

    def test_temp_at_10_no_multiplier(self):
        """Boundary temp_c == 10: does not trigger < 10, normal rate."""
        assert water_volume(10, "seedling", 10) == 20.0

    def test_temp_nominal_range_no_multiplier(self):
        """Temperature in [10, 35] normal range (e.g. 22): no multiplier."""
        assert water_volume(10, "seedling", 22) == 20.0


# =====================================================================
# Branch Coverage Tests: schedule()
# =====================================================================

class TestScheduleBranches:
    """Tests evaluating all execution pathways and branch decisions in schedule."""

    def test_empty_zones_returns_empty_plan(self):
        """Empty zones list: loop never executes (tests 35->43 loop exit branch)."""
        assert schedule([], 100) == []

    def test_all_zones_skipped_due_to_sufficient_moisture(self):
        """Zones with should_irrigate == False: tests continue branch."""
        zones = [
            ("Zone1", 10, 75, 0, "seedling", 20),
            ("Zone2", 15, 65, 0, "flowering", 20),
        ]
        assert schedule(zones, 100) == []

    def test_all_zones_scheduled_normal_loop_completion(self):
        """Multiple zones all irrigated and fit within budget: normal loop completion."""
        zones = [
            ("ZoneA", 10, 30, 0, "seedling", 20),      # need = 20L <= 100L -> budget = 80L
            ("ZoneB", 5, 40, 0, "flowering", 20),       # need = 25L <= 80L  -> budget = 55L
            ("ZoneC", 10, 20, 0, "vegetative", 20),     # need = 40L <= 55L  -> budget = 15L
        ]
        assert schedule(zones, 100) == ["ZoneA", "ZoneB", "ZoneC"]

    def test_schedule_exact_budget_match(self):
        """Need exactly equals remaining budget: tests need > budget False on equality."""
        zones = [
            ("ZoneA", 10, 30, 0, "seedling", 20),  # need = 20L
        ]
        assert schedule(zones, 20) == ["ZoneA"]

    def test_schedule_budget_exhausted_break(self):
        """Zone need exceeds budget: tests need > budget True branch (break)."""
        zones = [
            ("ZoneA", 10, 30, 0, "seedling", 20),   # need = 20L <= 50L -> budget = 30L
            ("ZoneB", 10, 30, 0, "flowering", 20),  # need = 50L > 30L  -> break!
            ("ZoneC", 5, 20, 0, "seedling", 20),    # skipped because loop broke
        ]
        assert schedule(zones, 50) == ["ZoneA"]

    def test_first_zone_exceeds_budget_immediately(self):
        """First zone need exceeds total budget: breaks immediately on first iteration."""
        zones = [
            ("ZoneA", 50, 30, 0, "flowering", 20),  # need = 250L > 100L -> break
        ]
        assert schedule(zones, 100) == []
