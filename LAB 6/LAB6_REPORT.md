# Lab 6: Code and Branch Coverage Analysis Report

**Course:** Software Engineering Lab (SE Lab)  
**Student Name:** Vibhav M  
**SRN:** PES1UG24CS527  
**Assigned Topic:** Irrigation Scheduler (`L6_L7_37_irrigation_scheduler`)  
**Module Under Test:** `irrigation_scheduler.py`  

---

## 1. Executive Summary

This report documents the code and branch coverage analysis for the **Irrigation Scheduler** Python module. Code coverage and branch coverage techniques were applied using Python's `coverage` tool and the `pytest` test framework. 

Starting from an initial coverage of **29% line coverage** and **24% branch coverage**, comprehensive test suites were designed and implemented to reach:
- **100% Line (Code) Coverage** (38/38 statements)
- **100% Branch Coverage** (28/28 branches, 0 missing branches)

---

## 2. Concept Analysis: Line Coverage vs. Branch Coverage

| Metric | Definition | Limitation |
| :--- | :--- | :--- |
| **Line Coverage** | Measures the percentage of executable statements executed at least once during test execution. | Can give a false sense of security. Even if 100% of lines are touched, untested logical branches and boolean sub-expressions remain hidden. |
| **Branch Coverage** | Measures whether every control structure (e.g., `if`, `elif`, `else`, `for`) evaluated to both `True` and `False` outcomes. | Requires designing tests that specifically target boundary values and alternate logical conditions. |

### Concrete Example from `irrigation_scheduler.py`
In `CodeCoverageTest_irrigation_scheduler.py`, all statements in `schedule()` were executed by feeding a list of zones that terminated via `break`. 
- **Line Coverage** reported **100%**.
- However, **Branch Coverage** revealed missing branch `35->43`, meaning the loop had never completed naturally or handled an empty zone list.
- In `BranchCoverageTest_irrigation_scheduler.py`, targeted boundary and edge case tests were introduced to verify both loop completion without breaking and empty list handling, achieving **100% Branch Coverage**.

---

## 3. Coverage Progression & Metrics Summary

| Milestone | Test File | Statements Covered | Line Coverage (%) | Branches Covered | Branch Coverage (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Initial Baseline** | `test_irrigation_scheduler.py` (Starter) | 11 / 38 | **29%** | 6 / 28 | **24%** |
| **Phase 1: Code Coverage** | `CodeCoverageTest_irrigation_scheduler.py` | 38 / 38 | **100%** | 27 / 28 | **98%** |
| **Phase 2: Branch Coverage** | `BranchCoverageTest_irrigation_scheduler.py` | 38 / 38 | **100%** | 28 / 28 | **100%** |
| **Final Unified Suite** | `test_irrigation_scheduler.py` (Final) | 38 / 38 | **100%** | 28 / 28 | **100%** |

---

## 4. Test Suite Design Matrix

### 4.1 `should_irrigate(moisture, rain_mm, stage)`
*Logic: High moisture (>=60) or heavy rain (>=10) suppresses irrigation. Seedlings irrigate if moisture < 45. Flowering irrigates if moisture < 55. Other stages irrigate if rain < 5 and moisture < 40.*

| Test ID | Function / Purpose | Input `(moisture, rain, stage)` | Expected Output | Decision Branch Evaluated |
| :--- | :--- | :--- | :---: | :--- |
| **TC-IRR-01** | High moisture suppression | `(70, 0, "seedling")` | `False` | `moisture >= 60` -> `True` |
| **TC-IRR-02** | High moisture boundary | `(60, 0, "seedling")` | `False` | `moisture >= 60` -> `True` (exact boundary) |
| **TC-IRR-03** | Moisture below boundary | `(59, 15, "seedling")` | `False` | `moisture >= 60` -> `False`, enters rain check |
| **TC-IRR-04** | Heavy rain suppression | `(50, 12, "seedling")` | `False` | `rain_mm >= 10` -> `True` |
| **TC-IRR-05** | Heavy rain boundary | `(50, 10, "seedling")` | `False` | `rain_mm >= 10` -> `True` (exact boundary) |
| **TC-IRR-06** | Rain below heavy boundary | `(30, 9, "seedling")` | `True` | `rain_mm >= 10` -> `False`, enters seedling logic |
| **TC-IRR-07** | Seedling dry | `(30, 2, "seedling")` | `True` | `stage == "seedling"` -> `True`, `moisture < 45` -> `True` |
| **TC-IRR-08** | Seedling boundary (44%) | `(44, 2, "seedling")` | `True` | `moisture < 45` -> `True` (upper boundary) |
| **TC-IRR-09** | Seedling boundary (45%) | `(45, 2, "seedling")` | `False` | `moisture < 45` -> `False` (exact boundary) |
| **TC-IRR-10** | Seedling moist | `(50, 2, "seedling")` | `False` | `moisture < 45` -> `False` |
| **TC-IRR-11** | Flowering dry | `(50, 2, "flowering")` | `True` | `stage == "flowering"` -> `True`, `moisture < 55` -> `True` |
| **TC-IRR-12** | Flowering boundary (54%)| `(54, 2, "flowering")` | `True` | `moisture < 55` -> `True` (upper boundary) |
| **TC-IRR-13** | Flowering boundary (55%)| `(55, 2, "flowering")` | `False` | `moisture < 55` -> `False` (exact boundary) |
| **TC-IRR-14** | Flowering moist | `(58, 2, "flowering")` | `False` | `moisture < 55` -> `False` |
| **TC-IRR-15** | Other stage rain boundary | `(20, 5, "vegetative")` | `False` | `rain_mm >= 5` -> `True` (exact boundary) |
| **TC-IRR-16** | Other stage moderate rain | `(30, 6, "vegetative")` | `False` | `rain_mm >= 5` -> `True` |
| **TC-IRR-17** | Other stage dry | `(35, 2, "vegetative")` | `True` | `moisture < 40` -> `True` |
| **TC-IRR-18** | Other stage boundary (39%)| `(39, 4, "vegetative")` | `True` | `moisture < 40` -> `True` (upper boundary) |
| **TC-IRR-19** | Other stage boundary (40%)| `(40, 2, "vegetative")` | `False` | `moisture < 40` -> `False` (exact boundary) |
| **TC-IRR-20** | Other stage moist | `(48, 2, "vegetative")` | `False` | `moisture < 40` -> `False` |

---

### 4.2 `water_volume(area_m2, stage, temp_c)`
*Logic: Raises ValueError if area <= 0. Base rate: seedling=2, flowering=5, other=4 L/m2. Temp > 35 -> x1.5; Temp < 10 -> x0.5.*

| Test ID | Function / Purpose | Input `(area, stage, temp)` | Expected Output | Decision Branch Evaluated |
| :--- | :--- | :--- | :---: | :--- |
| **TC-VOL-01** | Zero area validation | `(0, "seedling", 20)` | `ValueError("invalid area")` | `area_m2 <= 0` -> `True` |
| **TC-VOL-02** | Negative area validation | `(-5, "flowering", 20)` | `ValueError("invalid area")` | `area_m2 <= 0` -> `True` |
| **TC-VOL-03** | Valid minimum area | `(1, "seedling", 20)` | `2` | `area_m2 <= 0` -> `False` |
| **TC-VOL-04** | Seedling base rate | `(10, "seedling", 20)` | `20` | `stage == "seedling"` -> `True` |
| **TC-VOL-05** | Flowering base rate | `(10, "flowering", 20)` | `50` | `stage == "flowering"` -> `True` |
| **TC-VOL-06** | Other stage base rate | `(10, "vegetative", 20)`| `40` | `else` branch |
| **TC-VOL-07** | High temp adjustment | `(10, "seedling", 36)` | `30.0` | `temp_c > 35` -> `True` (1.5x) |
| **TC-VOL-08** | High temp boundary | `(10, "seedling", 35)` | `20.0` | `temp_c > 35` -> `False` (exact boundary) |
| **TC-VOL-09** | Low temp adjustment | `(10, "seedling", 9)` | `10.0` | `temp_c < 10` -> `True` (0.5x) |
| **TC-VOL-10** | Low temp boundary | `(10, "seedling", 10)` | `20.0` | `temp_c < 10` -> `False` (exact boundary) |
| **TC-VOL-11** | Nominal temperature | `(10, "seedling", 22)` | `20.0` | `10 <= temp <= 35` -> no adjustment |

---

### 4.3 `schedule(zones, budget)`
*Logic: Iterates through zones, filters out non-irrigated zones, checks budget, deducts water, builds schedule list.*

| Test ID | Function / Purpose | Input `(zones, budget)` | Expected Output | Decision Branch Evaluated |
| :--- | :--- | :--- | :---: | :--- |
| **TC-SCH-01** | Empty zones list | `([], 100)` | `[]` | `for` loop 0 iterations (`35->43`) |
| **TC-SCH-02** | All zones skipped | `[(Z1, 10, 75, 0, "seedling", 20)]` | `[]` | `not should_irrigate` -> `True` (`continue`) |
| **TC-SCH-03** | Normal schedule | `[(Z1, 10, 30, ...), (Z2, 10, 20, ...)]` | `["Z1", "Z2"]` | All fit budget, loop finishes naturally |
| **TC-SCH-04** | Exact budget match | `[(Z1, 10, 30, "seedling", 20)], budget=20` | `["Z1"]` | `need > budget` -> `False` on equality |
| **TC-SCH-05** | Budget exhausted break | `[(Z1, 20L), (Z2, 50L)], budget=40` | `["Z1"]` | `need > budget` -> `True` (`break`) |
| **TC-SCH-06** | First zone exceeds budget | `[(Z1, 250L)], budget=100` | `[]` | Immediate break on iteration 1 |

---

## 5. Verification Commands

### Line Coverage Analysis
```bash
coverage run -m pytest CodeCoverageTest_irrigation_scheduler.py
coverage report -m
```

### Branch Coverage Analysis
```bash
coverage run --branch -m pytest BranchCoverageTest_irrigation_scheduler.py
coverage report -m
```

### Complete Test Suite
```bash
coverage run --branch -m pytest test_irrigation_scheduler.py
coverage report -m
```

---

## 6. Deliverables Summary

- `CodeCoverageTest_irrigation_scheduler.py`: 100% Line Coverage test suite
- `BranchCoverageTest_irrigation_scheduler.py`: 100% Branch Coverage test suite
- `code_coverage_screenshot.png`: Visual terminal output of Line Coverage
- `branch_coverage_screenshot.png`: Visual terminal output of Branch Coverage
- `test_irrigation_scheduler.py`: Complete unified test suite
- `LAB6_REPORT.md`: Comprehensive coverage analysis and documentation
