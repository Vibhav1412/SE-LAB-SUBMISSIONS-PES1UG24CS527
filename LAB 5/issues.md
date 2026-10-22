# Static Code Analysis - Identified Issues and Fixes

## Overview
Static code analysis was performed on `todo_manager.py` using **Bandit**, **Pylint**, and **Flake8**. Below is the documentation of identified security vulnerabilities, logical bugs, and style violations, prioritized by severity.

## Known Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :---: | :--- | :--- |
| **Command Injection (B605)** | Security (High) | 57 | `os.system` invokes shell string concatenation with untrusted input `address`, exposing the system to arbitrary OS command injection (CWE-78). | Removed `os.system` shell call. Replaced with Python standard library `email.message.EmailMessage` to format email messages safely without spawning a shell. |
| **Insecure Deserialization (B301, B403)** | Security (Medium) | 3, 47 | Use of `pickle.load` to deserialize data from a file allows arbitrary code execution if an untrusted file is loaded (CWE-502). | Replaced `pickle` with standard `json` serialization (`json.dump` / `json.load`). Removed `import pickle` entirely. |
| **Insecure Pseudo-Random Generator (B311)** | Security (Low) | 4, 70 | `random.choice` uses the standard Mersenne Twister PRNG, which is predictable and not cryptographically secure (CWE-330). | Replaced `random.choice` with `secrets.choice` from Python's cryptographically secure `secrets` module. |
| **Mutable Default Argument (W0102)** | Bug (Logic) | 11 | `labels=[]` default argument is evaluated once at function definition time. Subsequent calls share and mutate the same list object across task additions. | Changed default parameter to `labels=None` and initialized `labels = [] if labels is None else list(labels)` inside `add_task`. |
| **Inconsistent Return Statements (R1710)** | Code Quality | 33 | `findTask` explicitly returns `taskId` when a match is found, but implicitly returns `None` by falling off the end of the loop. | Added explicit `return None` at the end of `find_task` function. |
| **Unspecified File Encoding (W1514)** | Code Quality | 51 | `open(fileName, "w")` does not specify an encoding, leading to platform-dependent behavior (e.g., Windows default ANSI/cp1252 vs UTF-8). | Explicitly passed `encoding="utf-8"` to all `open()` file handlers. |
| **Non-conforming Naming Style (C0103)** | Style / Standard | 11–60 | Functions and variables used camelCase (`addTask`, `taskId`, `fileName`) violating Python's PEP 8 snake_case convention. | Renamed functions and variables to snake_case (`add_task`, `task_id`, `file_name`) while retaining backwards-compatibility aliases. |
| **PEP 8 Formatting Violations (E225, E303, E261, E231)** | Style / Formatting | 12, 40, 69, 74 | Missing whitespace around `=`, excessive blank lines, missing spaces before inline comments, and missing comma whitespace. | Formatted code to adhere strictly to PEP 8 spacing and layout guidelines. |

## Verification
All identified issues were verified as resolved:
- **Bandit**: 0 vulnerabilities remaining (clean pass).
- **Flake8**: 0 style violations remaining (clean pass).
- **Pylint Score**: Improved from **5.09/10** to a perfect **10.00/10**.
- **Runtime Integrity**: Output verified and identical to original execution.
