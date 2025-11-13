# WHERE 조건

WHERE 절은 특정 조건에 맞는 데이터만 필터링하여 조회합니다.

## 1. 기본 문법

```sql
SELECT 컬럼명
FROM 테이블명
WHERE 조건;
```

## 2. 비교 연산자

### 같음 (=)

```sql
-- 인사팀 직원만 조회
SELECT *
FROM employees
WHERE department = '인사팀';
```

### 같지 않음 (!=, <>)

```sql
-- 인사팀이 아닌 직원 조회
SELECT *
FROM employees
WHERE department != '인사팀';

-- 또는
WHERE department <> '인사팀';
```

### 크다 (>), 작다 (<)

```sql
-- 급여가 5,500,000 이상인 직원
SELECT emp_name, salary
FROM employees
WHERE salary >= 5500000;

-- 2020년 이전 입사자
SELECT emp_name, hire_date
FROM employees
WHERE hire_date < '2020-01-01';
```

## 3. 논리 연산자

### AND - 모든 조건을 만족

```sql
-- 인사팀이면서 급여가 5,000,000 이상인 직원
SELECT *
FROM employees
WHERE department = '인사팀'
  AND salary >= 5000000;
```

### OR - 하나 이상의 조건을 만족

```sql
-- 인사팀 또는 급여팀 직원
SELECT *
FROM employees
WHERE department = '인사팀'
   OR department = '급여팀';
```

### NOT - 조건을 반대로

```sql
-- 인사팀이 아닌 직원
SELECT *
FROM employees
WHERE NOT department = '인사팀';
```

### 복합 조건

```sql
-- 인사팀 또는 급여팀이면서, 급여가 5,500,000 이상
SELECT *
FROM employees
WHERE (department = '인사팀' OR department = '급여팀')
  AND salary >= 5500000;
```

> 💡 **Tip**: 괄호 `()`를 사용하여 우선순위를 명확히 하세요!

## 4. BETWEEN - 범위 조건

```sql
-- 급여가 5,000,000 ~ 6,000,000 사이
SELECT *
FROM employees
WHERE salary BETWEEN 5000000 AND 6000000;

-- 위 쿼리는 다음과 같음:
WHERE salary >= 5000000 AND salary <= 6000000;
```

### 날짜 범위

```sql
-- 2020년에 입사한 직원
SELECT *
FROM employees
WHERE hire_date BETWEEN '2020-01-01' AND '2020-12-31';
```

## 5. IN - 여러 값 중 하나

```sql
-- 인사팀, 급여팀, 총무팀 직원
SELECT *
FROM employees
WHERE department IN ('인사팀', '급여팀', '총무팀');

-- 위 쿼리는 다음과 같음:
WHERE department = '인사팀'
   OR department = '급여팀'
   OR department = '총무팀';
```

### NOT IN - 제외

```sql
-- 인사팀, 급여팀이 아닌 직원
SELECT *
FROM employees
WHERE department NOT IN ('인사팀', '급여팀');
```

## 6. LIKE - 패턴 매칭

### 기본 와일드카드

- `%`: 0개 이상의 문자
- `_`: 정확히 1개의 문자

```sql
-- 이름이 '김'으로 시작하는 직원
SELECT *
FROM employees
WHERE emp_name LIKE '김%';

-- 이름에 '영'이 포함된 직원
SELECT *
FROM employees
WHERE emp_name LIKE '%영%';

-- 이름이 '이'로 시작하고 3글자인 직원
SELECT *
FROM employees
WHERE emp_name LIKE '이__';
```

### 실무 예시

```sql
-- 이메일이 gmail인 직원
SELECT *
FROM employees
WHERE email LIKE '%@gmail.com';

-- 전화번호가 010으로 시작
SELECT *
FROM employees
WHERE phone LIKE '010%';
```

## 7. IS NULL / IS NOT NULL

NULL은 '값이 없음'을 의미합니다. `= NULL`이 아닌 `IS NULL`을 사용해야 합니다!

```sql
-- 퇴사일이 없는 직원 (재직 중)
SELECT *
FROM employees
WHERE resign_date IS NULL;

-- 이메일이 등록된 직원
SELECT *
FROM employees
WHERE email IS NOT NULL;
```

> ⚠️ **주의**: `WHERE email = NULL` (X) / `WHERE email IS NULL` (O)

## 8. 문자열 조건

### 대소문자 구분

```sql
-- 정확히 'HR'팀 (대소문자 구분)
SELECT *
FROM employees
WHERE department = 'HR';

-- 대소문자 무시 (DB에 따라 다름)
-- PostgreSQL:
WHERE LOWER(department) = LOWER('hr');
-- MySQL (기본적으로 대소문자 무시):
WHERE department = 'hr';
```

## 실습 문제

### 문제 1: 기본 필터링
급여가 6,000,000 이상인 직원의 이름과 급여를 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT emp_name, salary
FROM employees
WHERE salary >= 6000000;
```
</details>

### 문제 2: AND 조건
개발팀이면서 2020년 이후에 입사한 직원을 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT *
FROM employees
WHERE department = '개발팀'
  AND hire_date >= '2020-01-01';
```
</details>

### 문제 3: OR와 괄호
(인사팀 또는 급여팀) 중에서 급여가 5,500,000 이상인 직원을 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT *
FROM employees
WHERE (department = '인사팀' OR department = '급여팀')
  AND salary >= 5500000;
```
</details>

### 문제 4: IN 사용
직급이 '사원', '대리', '과장'인 직원을 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT *
FROM employees
WHERE position IN ('사원', '대리', '과장');
```
</details>

### 문제 5: LIKE 패턴
이름이 '박'으로 시작하는 직원을 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT *
FROM employees
WHERE emp_name LIKE '박%';
```
</details>

### 문제 6: BETWEEN
2020년 1월 1일부터 2021년 12월 31일 사이에 입사한 직원을 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT *
FROM employees
WHERE hire_date BETWEEN '2020-01-01' AND '2021-12-31';
```
</details>

### 문제 7: IS NULL
퇴사일이 NULL인 (재직 중인) 직원의 수를 조회하세요.

<details>
<summary>정답 보기</summary>

```sql
SELECT COUNT(*)
FROM employees
WHERE resign_date IS NULL;
```
</details>

## 조건 조합 예시

### 복잡한 조건 예시

```sql
-- 다음 조건을 모두 만족하는 직원:
-- 1. 인사팀, 급여팀, 또는 총무팀
-- 2. 급여 5,000,000 이상
-- 3. 2019년 이후 입사
-- 4. 재직 중
SELECT *
FROM employees
WHERE department IN ('인사팀', '급여팀', '총무팀')
  AND salary >= 5000000
  AND hire_date >= '2019-01-01'
  AND resign_date IS NULL
ORDER BY hire_date DESC;
```

## 핵심 요약

✅ **WHERE**: 조건으로 데이터 필터링
✅ **비교 연산자**: =, !=, >, <, >=, <=
✅ **논리 연산자**: AND, OR, NOT
✅ **BETWEEN**: 범위 조건
✅ **IN**: 여러 값 중 하나
✅ **LIKE**: 패턴 매칭 (%, _)
✅ **IS NULL**: NULL 체크 (= NULL이 아님!)

## 다음 단계

조건을 활용한 필터링을 익혔다면, 이제 여러 테이블의 데이터를 연결하는 JOIN을 배워봅시다!

👉 **[JOIN 활용으로 이동](./03-JOIN-활용.md)**
