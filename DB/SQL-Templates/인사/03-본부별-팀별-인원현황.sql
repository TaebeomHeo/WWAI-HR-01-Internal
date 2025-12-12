-- ============================================
-- 본부별/팀별 인원 현황 조회
-- ============================================
-- 목적: 특정 시점의 본부별, 팀별 인원 현황 파악
-- 테이블: basicinfoview, hrtransferhistory2
-- ============================================

-- ▼▼▼ 기준일 설정 (여기만 수정하세요) ▼▼▼
SET @기준일 = '2025-11-19';  -- 조회 기준일
-- ▲▲▲ 기준일 설정 ▲▲▲

-- 팀별 재직자 수 (basicinfoview 기준 - 현재 시점)
SELECT
    team_code AS 팀코드,
    COUNT(*) AS 인원수
FROM basicinfoview
GROUP BY team_code
ORDER BY 인원수 DESC;


-- 본부별/팀별 프로젝트 투입 인원 (기준일 기준)
SELECT
    division AS 본부,
    team_name AS 팀명,
    COUNT(DISTINCT employee_number) AS 인원수
FROM hrtransferhistory2
WHERE assignment_date <= @기준일
  AND (end_date IS NULL OR end_date = '' OR end_date >= @기준일)
GROUP BY division, team_name
ORDER BY division, team_name;


-- 본부별 총합 (ROLLUP 사용)
/*
SELECT
    IFNULL(division, '전체합계') AS 본부,
    COUNT(DISTINCT employee_number) AS 인원수
FROM hrtransferhistory2
WHERE assignment_date <= @기준일
  AND (end_date IS NULL OR end_date = '' OR end_date >= @기준일)
GROUP BY division WITH ROLLUP
ORDER BY division;
*/
