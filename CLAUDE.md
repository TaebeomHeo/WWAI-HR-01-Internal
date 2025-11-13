# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WWAI-HR-01-Internal is an HR management system with three core domains:

1. **인사 (HR/Personnel Management)** - Personnel tracking, project assignments, and organizational structure
2. **급여 (Payroll)** - Historical payroll tracking by department/team/executive levels
3. **총무 (General Affairs)** - Asset management, inventory tracking, and resource planning

## Requirements

All requirements are documented in Korean in the `Requirements/` directory:

- `Requirements/인사2.md` - Personnel management requirements
  - Weekly intranet extraction of personnel changes and project withdrawals
  - Real-time personnel status updates

- `Requirements/급여.md` - Payroll requirements
  - Historical payroll queries by department/team/executive level for specific time periods
  - Project Leader (PL) list tracking per month
  - Currently Excel-based workflow

- `Requirements/총무.md` - General affairs requirements
  - Asset management (currently Excel-based with check-in/check-out tracking)
  - Inventory status tracking
  - Team-level asset visibility (e.g., "Show all assets for Team XX in Division 1")
  - Inventory-based decision making and predictions
  - Expiration date predictions
  - New project asset purchase forecasting

## Architecture Notes

### Current State
- Requirements are defined but implementation has not started
- Existing workflows are Excel-based, requiring migration to a centralized system
- Korean language is used throughout requirements and will likely be used in the UI

### Key Integration Points
- Intranet data extraction for personnel updates (weekly sync)
- Historical data migration from Excel spreadsheets
- Department/team/executive organizational hierarchy tracking
- Project-based resource allocation and tracking
