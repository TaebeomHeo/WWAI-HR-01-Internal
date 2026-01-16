# Project Analysis Report: WWAI-HR-01-Internal

## 1. Executive Summary

**WWAI-HR-01-Internal** is a specialized educational repository designed to upskill HR professionals at **WiseWires** (inferred from DB user/references). The project's primary goal is to transition HR workflows from manual Excel-based processes to automated Database-driven processes using SQL and AI tools.

**Key Findings:**
*   **Nature**: Education & Documentation (Not a software product).
*   **Target Audience**: HR staff with no programming background.
*   **Core Technology**: MariaDB (SQL), DBeaver (Client), Claude AI (Assistant).
*   **Data Integrity**: Scripts reveal active monitoring of data consistency between assignment history (`hrtransferhistory2`) and project info (`projectinfoview`), specifically for Project Leaders (PL).

## 2. Project Structure & Content Analysis

### 2.1 File Structure
The project is organized logically for learning:
```
/
├── Onboarding/        # Introduction
├── Guides/            # Step-by-step Tutorials
│   ├── 01-Setup       # Environment setup (DBeaver)
│   ├── 02-SQL-Basics  # SQL Syntax (SELECT, WHERE, JOIN)
│   ├── 03-AI-Usage    # AI Prompting guides
│   └── 04-Real-Cases  # Practical Application
├── DB/                # ALL Database resources
│   ├── src/           # Utility & Maintenance Scripts (*.py)
│   ├── schema/        # Schema Documentation
│   └── SQL-Templates/ # Ready-to-use Queries
│       ├── 인사 (HR)
│       ├── 급여 (Payroll)
│       └── 총무 (Admin)
├── Requirements/      # Business Needs (Korean)

```

### 2.2 Pedagogical Approach
*   **Template-First Learning**: Instead of writing from scratch, learners start by modifying variables (e.g., `@시작일`, `@종료일`) in pre-written templates.
*   **DBeaver Integration**: The SQL templates use DBeaver-specific variable syntax, making it easy for non-developers to run parameterized queries without understanding stored procedures.
*   **Real-World Context**: All examples use actual HR terminology and scenarios (e.g., "Weekly Personnel Changes", "Project PL Lists"), making the learning immediately applicable.

## 3. Technical & Database Analysis

### 3.1 Database Schema (MariaDB)
The schema is complex, reflecting a mature HR system.
*   **`basicinfo` / `basicinfoview`**: Core employee data. Contains sensitive PII (Resident numbers seem hashed/not present, but has phone/address).
*   **`hrtransferhistory2`**: The "Fact Table" for employee movements. Captures when someone moves teams, projects, or roles.
*   **`projectinfo` / `projectinfoview`**: Project metadata.
*   **`careerinfo`**: Past experience history.

### 3.2 Data Logic & Queries
*   **Date Handling**: Queries heavily rely on date ranges (`start_date`, `end_date`) to determine active status.
    *   *Observation*: `end_date IS NULL OR end_date = ''` is a common pattern to check for "currently active", covering both NULLs and empty strings (legacy data artifact).
*   **Project Leader (PL) Tracking**:
    *   `SQL-Templates/급여/01-월별-PL-리스트.sql` extracts PLs based on the `role` column in `hrtransferhistory2`.
    *   `pl_crosscheck_by_empnum.py` highlights a discrepancy: PLs are defined in *both* `hrtransferhistory2` (assignment based) and `projectinfoview` (project metadata). The script checks for consistency between these two sources, implying data synchronization issues exist.

### 3.3 Python Utilities
The generic python scripts serve two purposes:
1.  **Maintenance**: `db_schema_exporter.py` automatically generates the markdown documentation from the live DB schema.
2.  **Verification**: `pl_crosscheck_by_empnum.py` validates data integrity.
3.  **Experimental**: `hr_db_query_tool.py` is a simple text-to-SQL prototype, suggesting a future goal of building a natural language interface for HR.

## 4. Requirements Mapping

| Domain | Business Requirement (from `Requirements/`) | Implemented Solution (`SQL-Templates/`) | Status |
| :--- | :--- | :--- | :--- |
| **인사 (HR)** | Weekly personnel changes & headcount extraction | `01-주간-발령내역-조회.sql`<br>`03-본부별-팀별-인원현황.sql` | ✅ **Covered** |
| **급여 (Payroll)** | Historical payroll/PL list by dept/team | `01-월별-PL-리스트.sql`<br>`02-본부별-팀별-인원현황.sql` | ✅ **Covered** |
| **총무 (Admin)** | Asset tracking & purchase prediction | `01-자산-반출반입-현황.sql`<br>`03-재고-현황-및-예측.sql` | ⚠️ **Partially Covered** (Prediction logic is likely simple SQL aggregation, not ML) |

## 5. Recommendations

1.  **Data Consistency**: The discrepancy between `hrtransferhistory2` and `projectinfoview` regarding PLs needs to be resolved at the source or clearly documented which is the "Source of Truth".
2.  **Security**: The repository contains hardcoded database credentials in Python scripts (`wiseadmin140!`). **Strongly recommended to move these to environment variables or a separate config file immediately.**
3.  **Automation**: The `hr_db_query_tool.py` is a good start. It could be expanded into a proper Chatbot interface (e.g., via Streamlit) for easier access by non-technical staff.
