-- ============================================
-- 주간 발령 내역 조회
-- ============================================
-- 목적: 지난 주(월~일)의 발령사항을 추출하여 인원 현황 최신화
-- 테이블: hrtransferhistory2
-- ============================================

-- ▼▼▼ 조회 기간 설정 (여기만 수정하세요) ▼▼▼
SET @시작일 = '2025-11-10';  -- 조회 시작일 (월요일)
SET @종료일 = '2025-11-16';  -- 조회 종료일 (일요일)
-- ▲▲▲ 조회 기간 설정 ▲▲▲

SELECT
    employee_number AS 사번,
    name AS 직원명,
    assignment_date AS 발령일,
    assignment_type AS 발령유형,
    division AS 본부,
    team_name AS 팀명,
    project_name AS 프로젝트명,
    client_company AS 고객사,
    role AS 역할
FROM hrtransferhistory2
WHERE assignment_date >= @시작일
  AND assignment_date <= @종료일
ORDER BY assignment_date, name;
