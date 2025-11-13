# SELECT 기초

SELECT는 데이터베이스에서 데이터를 조회하는 가장 기본적인 명령어입니다.

## 1. 기본 문법

```sql
SELECT 컬럼명 FROM 테이블명;
```

## 2. 모든 컬럼 조회하기

`*` (asterisk)를 사용하면 테이블의 모든 컬럼을 조회합니다.

```sql
-- employees 테이블의 모든 데이터 조회
SELECT * FROM employees;
```

**결과 예시:**
```
emp_id | emp_name | department | salary | hire_date
-------|----------|------------|--------|------------
1      | 김철수    | 인사팀      | 5000000 | 2020-01-15
2      | 이영희    | 개발팀      | 6000000 | 2019-03-20
3      | 박민수    | 급여팀      | 5500000 | 2021-06-10
```

> 💡 **Tip**: `*`는 편리하지만, 필요한 컬럼만 명시하는 것이 성능상 좋습니다.

## 3. 특정 컬럼만 조회하기

필요한 컬럼만 콤마(`,`)로 구분하여 지정합니다.

```sql
-- 이름과 부서만 조회
SELECT emp_name, department
FROM employees;
```

**결과:**
```
emp_name | department
---------|------------
김철수    | 인사팀
이영희    | 개발팀
박민수    | 급여팀
```

### 여러 컬럼 조회

```sql
-- 이름, 부서, 급여 조회
SELECT emp_name, department, salary
FROM employees;
```

## 4. 컬럼 별칭(Alias) 사용하기

`AS` 키워드로 컬럼에 별칭을 붙일 수 있습니다.

```sql
-- 컬럼명을 한글로 표시
SELECT
    emp_name AS 직원명,
    department AS 부서,
    salary AS 급여
FROM employees;
```

**결과:**
```
직원명 | 부서   | 급여
-------|--------|--------
김철수 | 인사팀 | 5000000
이영희 | 개발팀 | 6000000
박민수 | 급여팀 | 5500000
```

### AS 생략 가능

```sql
-- AS 없이도 별칭 지정 가능
SELECT
    emp_name 직원명,
    department 부서,
    salary 급여
FROM employees;
```

> 💡 **Tip**: 별칭에 공백이 있으면 따옴표 필요: `salary AS "월 급여"`

## 5. 계산된 컬럼

조회할 때 계산을 수행할 수 있습니다.

```sql
-- 연봉 계산 (월급여 * 12)
SELECT
    emp_name AS 직원명,
    salary AS 월급여,
    salary * 12 AS 연봉
FROM employees;
```

**결과:**
```
직원명 | 월급여   | 연봉
-------|---------|----------
김철수 | 5000000 | 60000000
이영희 | 6000000 | 72000000
박민수 | 5500000 | 66000000
```

### 문자열 연결

```sql
-- 이름과 부서를 함께 표시
SELECT
    emp_name || ' (' || department || ')' AS 직원정보
FROM employees;
```

**결과:**
```
직원정보
-------------------
김철수 (인사팀)
이영희 (개발팀)
박민수 (급여팀)
```

> ⚠️ **주의**: 문자열 연결 연산자는 DB마다 다릅니다
> - PostgreSQL, SQLite: `||`
> - MySQL: `CONCAT()` 함수 사용
> - SQL Server: `+`

## 6. DISTINCT - 중복 제거

중복된 값을 제거하고 고유한 값만 조회합니다.

```sql
-- 모든 부서 목록 조회 (중복 제거)
SELECT DISTINCT department
FROM employees;
```

**결과:**
```
department
------------
인사팀
개발팀
급여팀
```

### 여러 컬럼 조합에서 중복 제거

```sql
-- 부서와 직급 조합에서 중복 제거
SELECT DISTINCT department, position
FROM employees;
```

## 7. LIMIT - 결과 개수 제한

조회 결과의 개수를 제한합니다.

```sql
-- 상위 5명만 조회
SELECT * FROM employees
LIMIT 5;
```

### OFFSET과 함께 사용

```sql
-- 6번째부터 5개 조회 (페이징)
SELECT * FROM employees
LIMIT 5 OFFSET 5;
```

> ⚠️ **주의**: LIMIT 문법은 DB마다 다릅니다
> - PostgreSQL, MySQL, SQLite: `LIMIT n`
> - SQL Server: `TOP n` (SELECT 바로 뒤)
> - Oracle: `ROWNUM` 사용

## 8. ORDER BY - 정렬

결과를 특정 컬럼 기준으로 정렬합니다.

```sql
-- 급여 기준 오름차순 정렬
SELECT emp_name, salary
FROM employees
ORDER BY salary;
```

### 내림차순 정렬 (DESC)

```sql
-- 급여 기준 내림차순 (높은 급여부터)
SELECT emp_name, salary
FROM employees
ORDER BY salary DESC;
```

### 여러 컬럼으로 정렬

```sql
-- 부서별로 묶고, 같은 부서 내에서는 급여 내림차순
SELECT department, emp_name, salary
FROM employees
ORDER BY department, salary DESC;
```

## 실습 문제

다음 문제를 직접 풀어보세요:

### 문제 1: 기본 조회
`employees` 테이블에서 모든 직원의 이름과 입사일을 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT emp_name, hire_date
FROM employees;
```
</details>

### 문제 2: 별칭 사용
직원 이름을 "성명", 급여를 "월급"이라는 별칭으로 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT
    emp_name AS 성명,
    salary AS 월급
FROM employees;
```
</details>

### 문제 3: 계산
각 직원의 이름, 월급여, 연봉(월급여 * 12)을 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT
    emp_name AS 이름,
    salary AS 월급여,
    salary * 12 AS 연봉
FROM employees;
```
</details>

### 문제 4: 정렬
모든 직원을 급여가 높은 순서대로 조회하세요. 상위 3명만 표시하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 3;
```
</details>

## 핵심 요약

✅ **SELECT**: 데이터 조회의 시작
✅ **FROM**: 어느 테이블에서 가져올지
✅ **AS**: 컬럼에 별칭 부여
✅ **DISTINCT**: 중복 제거
✅ **ORDER BY**: 정렬 (ASC 오름차순, DESC 내림차순)
✅ **LIMIT**: 결과 개수 제한

## 다음 단계

기본 조회를 익혔다면, 이제 조건을 추가하여 원하는 데이터만 필터링하는 방법을 배워봅시다!

👉 **[WHERE 조건으로 이동](./02-WHERE-조건.md)**
