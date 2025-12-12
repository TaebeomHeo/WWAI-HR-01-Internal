-- ============================================
-- 특정 시점 본부별/팀별 인원 현황 조회
-- ============================================
-- 목적: 과거 특정 시점의 본부별/팀별 인원 현황 파악
-- 테이블: hrtransferhistory2
-- 참고: 인건비 데이터는 별도 급여 테이블 필요
-- ============================================

-- ▼▼▼ 기준일 설정 (여기만 수정하세요) ▼▼▼
SET @기준일 = '2025-10-31';  -- 조회 기준일
-- ▲▲▲ 기준일 설정 ▲▲▲

-- 기준일 시점의 본부별/팀별 인원
SELECT
    division AS 본부,
    team_name AS 팀명,
    COUNT(DISTINCT employee_number) AS 인원수
FROM hrtransferhistory2
WHERE assignment_date <= @기준일
  AND (end_date >= @기준일 OR end_date IS NULL OR end_date = '')
GROUP BY division, team_name
ORDER BY division, team_name;


-- 본부별 총합
/*
SELECT
    division AS 본부,
    COUNT(DISTINCT employee_number) AS 인원수
FROM hrtransferhistory2
WHERE assignment_date <= @기준일
  AND (end_date >= @기준일 OR end_date IS NULL OR end_date = '')
GROUP BY division
ORDER BY 인원수 DESC;
*/


-- 역할별 인원 현황
/*
SELECT
    division AS 본부,
    role AS 역할,
    COUNT(DISTINCT employee_number) AS 인원수
FROM hrtransferhistory2
WHERE assignment_date <= @기준일
  AND (end_date >= @기준일 OR end_date IS NULL OR end_date = '')
GROUP BY division, role
ORDER BY division, role;
*/


-- ============================================
-- NOTE: 인건비 현황 조회
-- ============================================
-- 인건비 데이터는 현재 View에 포함되어 있지 않습니다.
-- 급여 정보가 포함된 테이블이 추가되면 아래와 같은 쿼리를 작성할 수 있습니다:
--
-- SELECT
--     division AS 본부,
--     team_name AS 팀명,
--     COUNT(DISTINCT employee_number) AS 인원수,
--     SUM(salary) AS 총인건비,
--     AVG(salary) AS 평균인건비
-- FROM hrtransferhistory2 h
-- JOIN salary_table s ON h.employee_number = s.employee_number
-- WHERE h.assignment_date <= '2025-10-31'
--   AND (h.end_date >= '2025-10-31' OR h.end_date IS NULL OR h.end_date = '')
-- GROUP BY division, team_name
-- ORDER BY division, team_name;
-- ============================================
