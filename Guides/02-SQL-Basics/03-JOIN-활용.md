# JOIN 활용

JOIN은 여러 테이블의 데이터를 연결하여 조회하는 방법입니다. 실무에서 가장 많이 사용되는 중요한 기능입니다.

## 왜 JOIN이 필요한가?

데이터베이스는 데이터 중복을 피하기 위해 여러 테이블로 나누어 저장합니다.

### 예시 테이블 구조

**employees (직원) 테이블:**
```
emp_id | emp_name | dept_id | salary
-------|----------|---------|--------
1      | 김철수    | 10      | 5000000
2      | 이영희    | 20      | 6000000
3      | 박민수    | 10      | 5500000
```

**departments (부서) 테이블:**
```
dept_id | dept_name
--------|----------
10      | 인사팀
20      | 개발팀
30      | 총무팀
```

직원의 부서명을 알려면 두 테이블을 **연결**해야 합니다!

## 1. INNER JOIN - 교집합

양쪽 테이블에 모두 존재하는 데이터만 조회합니다.

### 기본 문법

```sql
SELECT 컬럼들
FROM 테이블1
INNER JOIN 테이블2
    ON 테이블1.연결컬럼 = 테이블2.연결컬럼;
```

### 실제 예시

```sql
-- 직원과 부서 정보를 함께 조회
SELECT
    e.emp_name,
    e.salary,
    d.dept_name
FROM employees e
INNER JOIN departments d
    ON e.dept_id = d.dept_id;
```

**결과:**
```
emp_name | salary  | dept_name
---------|---------|----------
김철수    | 5000000 | 인사팀
이영희    | 6000000 | 개발팀
박민수    | 5500000 | 인사팀
```

> 💡 **Tip**: `e`와 `d`는 테이블 별칭입니다. 길게 쓰지 않아도 됩니다!

### 테이블 별칭 사용

```sql
-- 별칭으로 간결하게 작성
SELECT
    e.emp_name AS 직원명,
    d.dept_name AS 부서명
FROM employees e          -- employees를 e로 줄임
INNER JOIN departments d  -- departments를 d로 줄임
    ON e.dept_id = d.dept_id;
```

## 2. LEFT JOIN - 왼쪽 테이블 기준

왼쪽 테이블의 모든 데이터를 가져오고, 오른쪽 테이블은 매칭되는 것만 가져옵니다.

### 기본 문법

```sql
SELECT 컬럼들
FROM 테이블1  -- 왼쪽 (기준)
LEFT JOIN 테이블2  -- 오른쪽
    ON 테이블1.연결컬럼 = 테이블2.연결컬럼;
```

### 예시 상황

**employees 테이블:**
```
emp_id | emp_name | dept_id
-------|----------|--------
1      | 김철수    | 10
2      | 이영희    | 20
3      | 박민수    | NULL     -- 부서 미배정
```

```sql
-- 모든 직원 조회 (부서가 없어도 표시)
SELECT
    e.emp_name,
    d.dept_name
FROM employees e
LEFT JOIN departments d
    ON e.dept_id = d.dept_id;
```

**결과:**
```
emp_name | dept_name
---------|----------
김철수    | 인사팀
이영희    | 개발팀
박민수    | NULL      -- 부서 정보 없음
```

### LEFT JOIN 활용: 매칭 안 된 데이터 찾기

```sql
-- 부서가 배정되지 않은 직원 찾기
SELECT
    e.emp_name
FROM employees e
LEFT JOIN departments d
    ON e.dept_id = d.dept_id
WHERE d.dept_id IS NULL;
```

## 3. INNER JOIN vs LEFT JOIN 비교

| 구분 | INNER JOIN | LEFT JOIN |
|------|------------|-----------|
| 결과 | 양쪽 모두 매칭되는 것만 | 왼쪽 모두 + 오른쪽 매칭되는 것 |
| 사용 시기 | 정확히 매칭되는 것만 필요 | 왼쪽 기준으로 모두 보고 싶을 때 |

### 시각적 비교

```
INNER JOIN (교집합):
┌─────────┐       ┌─────────┐
│ Table A │ ╲   ╱ │ Table B │
│         │  ╲ ╱  │         │
│         │   X   │         │
│         │  ╱ ╲  │         │
│         │ ╱   ╲ │         │
└─────────┘       └─────────┘
        오직 매칭되는 부분만

LEFT JOIN (왼쪽 전체):
┌─────────┐       ┌─────────┐
│█████████│ ╲   ╱ │ Table B │
│█████████│  ╲ ╱  │         │
│█████████│   X   │         │
│█████████│  ╱ ╲  │         │
│█████████│ ╱   ╲ │         │
└─────────┘       └─────────┘
  왼쪽 전체 + 매칭되는 부분
```

## 4. 여러 테이블 JOIN

3개 이상의 테이블도 연결할 수 있습니다.

### 예시: 직원 + 부서 + 프로젝트

**테이블 구조:**
```
employees:        departments:      projects:
emp_id            dept_id           project_id
emp_name          dept_name         project_name
dept_id                             emp_id (담당자)
```

```sql
-- 직원, 소속 부서, 담당 프로젝트를 함께 조회
SELECT
    e.emp_name AS 직원명,
    d.dept_name AS 부서명,
    p.project_name AS 프로젝트명
FROM employees e
INNER JOIN departments d
    ON e.dept_id = d.dept_id
LEFT JOIN projects p
    ON e.emp_id = p.emp_id;
```

**결과:**
```
직원명 | 부서명  | 프로젝트명
-------|---------|------------------
김철수 | 인사팀  | 채용시스템 개선
이영희 | 개발팀  | AI 챗봇 개발
박민수 | 인사팀  | NULL (담당 프로젝트 없음)
```

## 5. JOIN과 WHERE 함께 사용

```sql
-- 인사팀 직원의 프로젝트 목록
SELECT
    e.emp_name,
    p.project_name
FROM employees e
INNER JOIN departments d
    ON e.dept_id = d.dept_id
LEFT JOIN projects p
    ON e.emp_id = p.emp_id
WHERE d.dept_name = '인사팀';
```

## 6. 같은 테이블 JOIN (Self JOIN)

같은 테이블을 자기 자신과 JOIN할 수도 있습니다.

### 예시: 직원과 상사 관계

**employees 테이블:**
```
emp_id | emp_name | manager_id
-------|----------|------------
1      | 김부장    | NULL
2      | 이과장    | 1
3      | 박대리    | 2
```

```sql
-- 직원과 그의 상사 이름 함께 조회
SELECT
    e.emp_name AS 직원,
    m.emp_name AS 상사
FROM employees e
LEFT JOIN employees m
    ON e.manager_id = m.emp_id;
```

**결과:**
```
직원   | 상사
-------|------
김부장 | NULL
이과장 | 김부장
박대리 | 이과장
```

## 실습 문제

### 문제 1: 기본 INNER JOIN
직원 테이블(employees)과 부서 테이블(departments)을 연결하여,
모든 직원의 이름과 부서명을 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT
    e.emp_name,
    d.dept_name
FROM employees e
INNER JOIN departments d
    ON e.dept_id = d.dept_id;
```
</details>

### 문제 2: LEFT JOIN
모든 직원의 이름과 부서명을 조회하되, 부서가 배정되지 않은 직원도 포함하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT
    e.emp_name,
    d.dept_name
FROM employees e
LEFT JOIN departments d
    ON e.dept_id = d.dept_id;
```
</details>

### 문제 3: JOIN + WHERE
개발팀 직원의 이름과 급여를 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT
    e.emp_name,
    e.salary
FROM employees e
INNER JOIN departments d
    ON e.dept_id = d.dept_id
WHERE d.dept_name = '개발팀';
```
</details>

### 문제 4: 3개 테이블 JOIN
직원, 부서, 프로젝트 정보를 모두 연결하여 조회하세요.
(프로젝트가 없는 직원도 포함)

<details>
<summary>정답 보기</summary>

```sql
SELECT
    e.emp_name,
    d.dept_name,
    p.project_name
FROM employees e
INNER JOIN departments d
    ON e.dept_id = d.dept_id
LEFT JOIN projects p
    ON e.emp_id = p.emp_id;
```
</details>

## 실무 팁

### 1. 항상 테이블 별칭 사용하기

```sql
-- 나쁜 예: 별칭 없이
SELECT employees.emp_name, departments.dept_name
FROM employees
INNER JOIN departments ON employees.dept_id = departments.dept_id;

-- 좋은 예: 별칭 사용
SELECT e.emp_name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```

### 2. JOIN 조건을 명확히

```sql
-- 나쁜 예: 조건 불명확
FROM employees e
INNER JOIN departments d;  -- ON 절 없음!

-- 좋은 예: 명확한 조건
FROM employees e
INNER JOIN departments d
    ON e.dept_id = d.dept_id;
```

### 3. 어떤 JOIN을 사용할지 판단

- **INNER JOIN**: "확실히 매칭되는 것만" → 엄격
- **LEFT JOIN**: "왼쪽은 무조건 다" → 포괄적

## 핵심 요약

✅ **INNER JOIN**: 양쪽 모두 매칭되는 것만
✅ **LEFT JOIN**: 왼쪽 전체 + 오른쪽 매칭되는 것
✅ **ON 절**: JOIN 조건 명시
✅ **테이블 별칭**: 간결한 코드 작성
✅ **여러 JOIN**: 3개 이상도 가능
✅ **Self JOIN**: 같은 테이블끼리도 가능

## 다음 단계

JOIN으로 데이터를 연결하는 방법을 배웠다면, 이제 집계함수로 통계를 내는 방법을 배워봅시다!

👉 **[집계함수로 이동](./04-집계함수.md)**
