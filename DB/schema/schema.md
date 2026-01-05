# HR 데이터베이스 스키마

## View 목록

| View 이름 | 설명 |
|-----------|------|
| basicinfoview | 직원 기본 정보 |
| careerview | 경력 정보 |
| hrtransferhistory | 발령 이력 (구버전) |
| hrtransferhistory2 | 발령 이력 (최신) |
| projectinfoview | 프로젝트 정보 |
| scholarshipview | 학자금 정보 |
| v_candidate_summary | 후보자 요약 |

---

## hrtransferhistory2 (발령 내역)

주요 발령 및 프로젝트 배정 내역을 조회하는 View입니다.

### 컬럼 구조

| 컬럼명 | 타입 | NULL | 설명 |
|--------|------|------|------|
| employee_number | varchar(10) | YES | 사번 |
| name | varchar(128) | YES | 직원명 |
| assignment_date | varchar(10) | YES | 발령일 |
| assignment_type | text | YES | 발령 유형 (전보, 승진, 입사 등) |
| end_date | varchar(10) | NO | 종료일 |
| project_duration | int(7) | YES | 프로젝트 기간 (일) |
| role | text | YES | 역할 (PL, 개발자 등) |
| division | text | YES | 본부 |
| team_code | varchar(10) | YES | 팀 코드 |
| team_name | text | YES | 팀명 |
| client_company | varchar(256) | YES | 고객사 |
| project_name | varchar(512) | YES | 프로젝트명 |
| project_code | varchar(32) | YES | 프로젝트 코드 |
| project_start_date | varchar(12) | YES | 프로젝트 시작일 |
| project_end_date | varchar(12) | YES | 프로젝트 종료일 |
| available_after_date | varchar(12) | NO | 이후 가용일 |

### 예제 쿼리

```sql
-- 지난 주 발령 내역 조회
SELECT
    employee_number AS 사번,
    name AS 직원명,
    assignment_date AS 발령일,
    assignment_type AS 발령유형,
    division AS 본부,
    team_name AS 팀명,
    project_name AS 프로젝트명,
    role AS 역할
FROM hrtransferhistory2
WHERE assignment_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY assignment_date DESC;
```

```sql
-- 특정 직원의 발령 이력
SELECT *
FROM hrtransferhistory2
WHERE name LIKE '%김철수%'
ORDER BY assignment_date DESC;
```

```sql
-- 본부별 현재 프로젝트 인원 현황
SELECT
    division AS 본부,
    COUNT(DISTINCT employee_number) AS 인원수
FROM hrtransferhistory2
WHERE end_date IS NULL OR end_date = ''
GROUP BY division
ORDER BY 인원수 DESC;
```

---

## basicinfoview (직원 기본 정보)

현재 재직 중인 직원의 기본 정보와 현재 프로젝트 정보를 조회하는 View입니다.

### 컬럼 구조

| 컬럼명 | 타입 | NULL | 설명 |
|--------|------|------|------|
| name_kor | varchar(128) | YES | 한글 이름 |
| name_eng | varchar(128) | YES | 영문 이름 |
| birth_date | varchar(10) | YES | 생년월일 |
| join_date | char(10) | YES | 입사일 |
| position_code | varchar(10) | YES | 직급 코드 |
| team_code | varchar(10) | YES | 팀 코드 |
| mobile_number | varchar(128) | YES | 휴대폰 번호 |
| telephone_primary | varchar(128) | YES | 유선 전화번호 |
| address | varchar(128) | YES | 주소 |
| email_address | varchar(128) | YES | 이메일 |
| member_id | varchar(10) | NO | 사번 |
| role | varchar(100) | YES | 역할 |
| corp | varchar(7) | NO | 법인 코드 |
| CORPGB | int(11) | NO | 법인 구분 |
| current_project_code | varchar(32) | YES | 현재 프로젝트 코드 |
| current_project_name | varchar(512) | YES | 현재 프로젝트명 |
| current_project_start_date | varchar(12) | YES | 현재 프로젝트 시작일 |
| current_project_end_date | varchar(12) | YES | 현재 프로젝트 종료일 |
| current_project_status | varchar(10) | YES | 현재 프로젝트 상태 |

### 예제 쿼리

```sql
-- 전체 재직자 명단
SELECT
    member_id AS 사번,
    name_kor AS 이름,
    team_code AS 팀코드,
    position_code AS 직급,
    join_date AS 입사일,
    current_project_name AS 현재프로젝트
FROM basicinfoview
ORDER BY join_date;
```

```sql
-- 특정 팀의 직원 목록
SELECT
    member_id AS 사번,
    name_kor AS 이름,
    email_address AS 이메일,
    mobile_number AS 연락처
FROM basicinfoview
WHERE team_code = 'TEAM001'
ORDER BY name_kor;
```

```sql
-- 프로젝트 종료 예정 직원 (이번 달)
SELECT
    member_id AS 사번,
    name_kor AS 이름,
    current_project_name AS 프로젝트명,
    current_project_end_date AS 종료예정일
FROM basicinfoview
WHERE current_project_end_date LIKE CONCAT(DATE_FORMAT(CURDATE(), '%Y-%m'), '%')
ORDER BY current_project_end_date;
```

---

## projectinfoview (프로젝트 정보)

프로젝트의 기본 정보와 현황을 조회하는 View입니다.

### 컬럼 구조

| 컬럼명 | 타입 | NULL | 설명 |
|--------|------|------|------|
| project_code | varchar(32) | NO | 프로젝트 코드 |
| project_name | varchar(512) | NO | 프로젝트명 |
| start_date | varchar(12) | YES | 시작일 |
| end_date | varchar(12) | YES | 종료일 |
| customer | varchar(512) | YES | 고객사 |
| project_address | varchar(512) | YES | 프로젝트 주소 |
| team_code | varchar(10) | YES | 담당 팀 코드 |
| team_name | varchar(128) | YES | 담당 팀명 |
| project_leader | varchar(64) | YES | PL 사번 |
| project_leader_name | varchar(128) | YES | PL 이름 |
| initial_major_job | text | YES | 초기 주요 업무 |
| active_status | varchar(10) | YES | 활성 상태 |
| project_type | varchar(44) | YES | 프로젝트 유형 |
| test_type | varchar(30) | YES | 테스트 유형 |
| initial_skill_set | text | YES | 초기 기술 스택 |
| team_size | varchar(12) | YES | 팀 규모 |
| project_domain | varchar(10) | YES | 프로젝트 도메인 |
| major_job | mediumtext | YES | 주요 업무 |
| skill_set | mediumtext | YES | 기술 스택 |

### 예제 쿼리

```sql
-- 진행 중인 프로젝트 목록
SELECT
    project_code AS 프로젝트코드,
    project_name AS 프로젝트명,
    customer AS 고객사,
    project_leader_name AS PL,
    team_name AS 담당팀,
    start_date AS 시작일,
    end_date AS 종료일,
    team_size AS 인원
FROM projectinfoview
WHERE active_status = 'Y'
ORDER BY start_date DESC;
```

```sql
-- 특정 고객사의 프로젝트 이력
SELECT
    project_name AS 프로젝트명,
    start_date AS 시작일,
    end_date AS 종료일,
    project_leader_name AS PL,
    team_size AS 인원
FROM projectinfoview
WHERE customer LIKE '%삼성%'
ORDER BY start_date DESC;
```

```sql
-- 이번 달 종료 예정 프로젝트
SELECT
    project_code AS 코드,
    project_name AS 프로젝트명,
    customer AS 고객사,
    end_date AS 종료일,
    project_leader_name AS PL,
    team_size AS 인원
FROM projectinfoview
WHERE end_date LIKE CONCAT(DATE_FORMAT(CURDATE(), '%Y-%m'), '%')
  AND active_status = 'Y'
ORDER BY end_date;
```

```sql
-- PL별 담당 프로젝트 수
SELECT
    project_leader_name AS PL,
    COUNT(*) AS 프로젝트수
FROM projectinfoview
WHERE active_status = 'Y'
GROUP BY project_leader, project_leader_name
ORDER BY 프로젝트수 DESC;
```

---

## careerview (경력 정보)

(스키마 정보 추가 예정)
