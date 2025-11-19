-- ============================================
-- 프로젝트 철수 현황 조회
-- ============================================
-- 목적: 특정 기간 내 프로젝트에서 철수한 인원 파악
-- 테이블: hrtransferhistory2
-- ============================================

-- ▼▼▼ 조회 기간 설정 (여기만 수정하세요) ▼▼▼
SET @시작일 = '2025-11-10';  -- 조회 시작일
SET @종료일 = '2025-11-16';  -- 조회 종료일
-- ▲▲▲ 조회 기간 설정 ▲▲▲

SELECT
    employee_number AS 사번,
    name AS 직원명,
    project_name AS 프로젝트명,
    client_company AS 고객사,
    end_date AS 철수일,
    division AS 본부,
    team_name AS 팀명,
    role AS 역할
FROM hrtransferhistory2
WHERE end_date >= @시작일
  AND end_date <= @종료일
  AND end_date != ''
ORDER BY end_date, project_name, name;
