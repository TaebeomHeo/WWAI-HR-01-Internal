# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**WWAI-HR-01-Internal** is an educational program designed to teach HR team members how to automate their workflows using database queries (SQL) and AI tools.

### Purpose

This is NOT a software development project. Instead, it's a **training and documentation repository** to help HR staff:
1. Learn SQL basics for querying HR databases
2. Use AI effectively to write and debug SQL queries
3. Automate repetitive tasks through database queries
4. Eventually progress to building automation agents (future phase)

### Target Audience

HR team members with:
- Little to no programming experience
- Currently using Excel for most workflows
- Need to query databases for: personnel management (인사), payroll (급여), and general affairs (총무)

## Project Structure

```
/
├── Onboarding/              # Start here - project introduction and learning roadmap
├── Guides/                  # Step-by-step learning materials
│   ├── 01-Setup/           # DBeaver installation and configuration
│   ├── 02-SQL-Basics/      # SQL fundamentals (SELECT, WHERE, JOIN, aggregations)
│   ├── 03-AI-Usage/        # How to work with AI for SQL queries
│   └── 04-Real-Cases/      # Real-world examples from HR workflows
├── Requirements/            # Original business requirements (in Korean)
├── SQL-Templates/           # Reusable SQL query templates
├── Database/                # Database schema documentation
└── Exercises/               # Practice problems
```

## Learning Path

Learners should follow this sequence:

1. **[Onboarding/README.md](Onboarding/README.md)** - Project overview and roadmap
2. **[Guides/01-Setup/](Guides/01-Setup/)** - Install DBeaver and connect to database
3. **[Guides/02-SQL-Basics/](Guides/02-SQL-Basics/)** - Learn SQL step-by-step
4. **[Guides/03-AI-Usage/](Guides/03-AI-Usage/)** - Learn to collaborate with AI
5. **[Guides/04-Real-Cases/](Guides/04-Real-Cases/)** - Apply to real HR scenarios

## Business Requirements

Requirements from actual HR workflows are documented in Korean in `Requirements/`:

- **인사2.md** - Personnel management
  - Weekly personnel changes extraction
  - Project assignment tracking
  - Headcount updates

- **급여.md** - Payroll
  - Historical payroll queries by department/team/executive
  - Monthly PL list tracking
  - Currently Excel-based

- **총무.md** - General affairs
  - Asset check-in/check-out tracking
  - Inventory management
  - Asset forecasting for new projects

## Documentation Style

- **Language**: All documentation is in Korean (target audience is Korean-speaking HR staff)
- **Level**: Beginner-friendly with step-by-step explanations
- **Format**: Markdown with code examples and practice problems
- **Approach**: Learn by doing with realistic examples

## Future Phases

After mastering SQL and AI collaboration:
- Phase 2: Subagent development for automation
- Phase 3: Automated reporting workflows
- Phase 4: Predictive analytics integration

## When Adding New Content

- Use clear, simple Korean
- Include practical examples from HR workflows
- Add practice problems with solutions
- Link back to basic concepts when introducing advanced topics
- Always provide AI prompting examples
