# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Course:** Software Engineering
**Student:** Vibhav (PES1UG25CS527), Section I
**Institution:** PES University, Dept. of CSE

## Problem Statement

**#37 — Group Travel Expense Simplification Engine**

A multi-currency expense-sharing utility that records uneven group expenses, converts foreign currencies via daily exchange rates, and computes minimum-transaction debt settlement graphs — so a group of travelers can settle up with the fewest possible payments instead of everyone paying everyone.

**Actors:** Group Traveler, Trip Admin, Exchange Rate Service (external)

## Repo Contents

| File | Description |
|---|---|
| `PES1UG25CS527_vibhav_SE_USECASE_REPORT.docx` / `.pdf` | Use-case flow specification for **UC-01: Log Expense** — preconditions, postconditions, main success scenario, and an alternate flow |
| `PES1UG24CS527_REQUIREMENTS_TABLE.xlsx` | Requirements table — 5 Functional Requirements (FR-001–FR-005) and 2 Non-Functional Requirements (NFR-001, NFR-002) |
| `UML_use_case_diagram.pdf` | UML use-case diagram with all actors, use cases, and `<<include>>` / `<<extend>>` relationships |

## Use Cases

- **Log Expense** — record an expense and split it among travelers *(includes Convert Currency)*
- **Convert Currency** — convert an entered amount to the trip's base currency using the day's exchange rate
- **Notify Balance Update** — alert affected travelers when balances change
- **View Balance** — check current amount owed / owed to a traveler
- **Manage Travelers** — Trip Admin adds/removes travelers and sets the base currency
- **Compute Debt Settlement** — calculates the minimum-transaction payoff graph *(can extend Manage Travelers)*

## Requirements Summary

| ID | Type | Priority | Summary |
|---|---|---|---|
| FR-001 | Functional | High | Compute the optimal debt settlement graph using min-flow algorithms to minimize peer-to-peer transactions |
| FR-002 | Functional | High | Log an expense with amount, currency, payer, and split list |
| FR-003 | Functional | High | Convert an expense to the trip's base currency using that day's exchange rate |
| FR-004 | Functional | High | Allow any traveler to view their current balance at any time |
| FR-005 | Functional | Medium | Let a Trip Admin manage travelers and set the base currency |
| NFR-001 | Non-Functional | High | Settlement engine must execute in under 100ms for 50 travelers / 500 expenses |
| NFR-002 | Non-Functional | High | ≥99.5% uptime; falls back to the last known exchange rate if the live feed is down |

Full descriptions, acceptance criteria, and rationale are in the requirements table.

## Use-Case Flow Highlight — Log Expense (UC-01)

**Main Success Scenario:** Traveler selects "Log Expense" → enters amount, currency, payer(s), and split list → system converts currency and validates the split sums to the total → expense is recorded in the shared ledger → balances recalculate → affected travelers are notified.

**Alternate Flow (4a):** If the currency isn't supported, the system shows an error and prompts for a valid currency; canceling instead discards the entry with no ledger update.

## Tools Used

Draw.io (UML diagram), Microsoft Word (use-case flow), Microsoft Excel (requirements table)
