-- ============================================
-- 월별 프로젝트 PL 리스트 조회
-- ============================================
-- 목적: 특정 월에 PL 역할을 수행한 인원 목록 추출
-- 테이블: hrtransferhistory2
-- ============================================

-- ▼▼▼ 조회 월 설정 (여기만 수정하세요) ▼▼▼
SET @월시작 = '2025-10-01';  -- 조회 월 첫째 날
SET @월종료 = '2025-10-31';  -- 조회 월 마지막 날
-- ▲▲▲ 조회 월 설정 ▲▲▲

-- 해당 월의 PL 리스트 (하루라도 PL이었으면 포함)
SELECT DISTINCT
    employee_number AS 사번,
    name AS PL이름,
    project_name AS 프로젝트명,
    client_company AS 고객사,
    division AS 본부,
    team_name AS 팀명,
    assignment_date AS 시작일,
    end_date AS 종료일
FROM hrtransferhistory2
WHERE role = 'PL'
  AND assignment_date <= @월종료
  AND (end_date >= @월시작 OR end_date IS NULL OR end_date = '')
ORDER BY name, assignment_date;


-- PL 명단만 (중복 제거)
/*
SELECT DISTINCT
    employee_number AS 사번,
    name AS PL이름
FROM hrtransferhistory2
WHERE role = 'PL'
  AND assignment_date <= @월종료
  AND (end_date >= @월시작 OR end_date IS NULL OR end_date = '')
ORDER BY name;
*/


-- 본부별 PL 수 집계
/*
SELECT
    division AS 본부,
    COUNT(DISTINCT employee_number) AS PL수
FROM hrtransferhistory2
WHERE role = 'PL'
  AND assignment_date <= @월종료
  AND (end_date >= @월시작 OR end_date IS NULL OR end_date = '')
GROUP BY division
ORDER BY PL수 DESC;
*/


-- 고객사별 PL 수 집계
/*
SELECT
    client_company AS 고객사,
    COUNT(DISTINCT employee_number) AS PL수
FROM hrtransferhistory2
WHERE role = 'PL'
  AND assignment_date <= @월종료
  AND (end_date >= @월시작 OR end_date IS NULL OR end_date = '')
  AND client_company IS NOT NULL
  AND client_company != ''
GROUP BY client_company
ORDER BY PL수 DESC;
*/
