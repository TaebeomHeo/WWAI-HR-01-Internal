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
├── DB/                      # Database related resources
│   ├── src/                # Utility Python scripts
│   ├── schema/             # Database schema documentation
│   └── SQL-Templates/      # Reusable SQL query templates
│       ├── 인사/            # Personnel queries
│       ├── 급여/            # Payroll queries
│       └── 총무/            # General affairs
└── Exercises/               # Practice problems
```

## SQL Templates 사용법

SQL-Templates 폴더에는 실무에서 바로 사용할 수 있는 쿼리 템플릿이 있습니다.

### 사용 방법

1. DBeaver에서 원하는 SQL 파일을 엽니다
2. 파일 상단의 **변수 설정 부분**을 찾습니다 (▼▼▼ 표시)
3. 날짜나 조건 값을 원하는 값으로 수정합니다
4. 전체 쿼리를 실행합니다

### 예시

```sql
-- ▼▼▼ 조회 기간 설정 (여기만 수정하세요) ▼▼▼
SET @시작일 = '2025-11-10';  -- 조회 시작일
SET @종료일 = '2025-11-16';  -- 조회 종료일
-- ▲▲▲ 조회 기간 설정 ▲▲▲

SELECT ...
WHERE assignment_date >= @시작일
  AND assignment_date <= @종료일
```

### 템플릿 목록

**인사**
- `01-주간-발령내역-조회.sql` - 주간 발령 내역
- `02-프로젝트-철수-현황.sql` - 프로젝트 종료/철수 현황
- `03-본부별-팀별-인원현황.sql` - 본부/팀별 인원
- `04-재직자-명단.sql` - 전체 재직자 명단

**급여**
- `01-월별-PL-리스트.sql` - 월별 PL 목록
- `02-본부별-팀별-인원현황.sql` - 인건비 현황용 인원

**총무**
- `01-자산-반출반입-현황.sql` - 자산 반출/반입
- `02-부서별-팀별-자산현황.sql` - 부서별 자산
- `03-재고-현황-및-예측.sql` - 재고 및 구매 예측

## Database 연결 정보

DBeaver 연결 설정:
- **Host**: 61.37.80.105
- **Port**: 3306
- **Database**: dbwisewiresdb
- **User**: wisewires
- **Driver**: MariaDB

> 비밀번호는 팀 내부 공유 문서를 참조하세요.

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
