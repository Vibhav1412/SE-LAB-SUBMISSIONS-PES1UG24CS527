# L6_L7_37 — Irrigation Scheduler

## Lab 6: Code and Branch Coverage Analysis

### Student Details
- **Student Name:** Vibhav M
- **SRN:** PES1UG24CS527
- **Course:** Software Engineering Lab

---

### About the Project
A Python module designed to optimize agricultural water distribution by deciding when a field zone requires watering, calculating volume demands adjusted for crop stage and temperature, and creating an optimal schedule constrained by an overall water budget.

### Deliverables Checklist

| Deliverable | File | Description |
| :--- | :--- | :--- |
| **Code Coverage Test Suite** | `CodeCoverageTest_irrigation_scheduler.py` | Test suite achieving 100% line coverage |
| **Branch Coverage Test Suite** | `BranchCoverageTest_irrigation_scheduler.py` | Comprehensive test suite achieving 100% branch coverage |
| **Unified Test Suite** | `test_irrigation_scheduler.py` | Complete unit test suite |
| **Application Under Test** | `irrigation_scheduler.py` | Production code under test |
| **Code Coverage Terminal Output** | `code_coverage_screenshot.png` | Screenshot of terminal report for line coverage |
| **Branch Coverage Terminal Output** | `branch_coverage_screenshot.png` | Screenshot of terminal report for branch coverage |
| **Analysis Report** | `LAB6_REPORT.md` | Full breakdown of metrics, branch logic & design matrix |

---

### Running the Coverage Analysis

1. **Install Prerequisites:**
   ```bash
   pip install pytest coverage
   ```

2. **Run Code Coverage Analysis:**
   ```bash
   coverage run -m pytest CodeCoverageTest_irrigation_scheduler.py
   coverage report -m
   ```

3. **Run Branch Coverage Analysis:**
   ```bash
   coverage run --branch -m pytest BranchCoverageTest_irrigation_scheduler.py
   coverage report -m
   ```

4. **Run Unified Test Suite:**
   ```bash
   coverage run --branch -m pytest test_irrigation_scheduler.py
   coverage report -m
   ```

---

### Coverage Results

- **Line Coverage:** 100% (38/38 statements)
- **Branch Coverage:** 100% (28/28 branches, 0 missing)
- **Total Test Cases:** 35 passing tests in `BranchCoverageTest_irrigation_scheduler.py`, 14 in `CodeCoverageTest_irrigation_scheduler.py`, 17 in `test_irrigation_scheduler.py`
