-- ============================================
-- 부서별/팀별 자산 현황 조회
-- ============================================
-- 목적: 특정 본부/팀의 자산 보유 현황 파악
-- 테이블: asset_assignments, assets, basicinfoview
-- ============================================
-- NOTE: 현재 자산 관련 테이블이 없습니다.
-- 아래는 자산 테이블이 생성된 후 사용할 템플릿입니다.
-- ============================================

-- 특정 팀의 자산 목록 (예: 특정 팀코드)
/*
SELECT
    b.name_kor AS 사용자,
    a.asset_type AS 자산유형,
    a.asset_name AS 자산명,
    a.serial_number AS 시리얼번호,
    aa.assigned_date AS 배정일
FROM asset_assignments aa
INNER JOIN assets a ON aa.asset_id = a.asset_id
INNER JOIN basicinfoview b ON aa.employee_number = b.member_id
WHERE b.team_code = 'TEAM001'  -- 팀코드 변경
  AND aa.returned_date IS NULL
ORDER BY a.asset_type, b.name_kor;
*/


-- 팀별 자산 보유 현황 집계
/*
SELECT
    b.team_code AS 팀코드,
    a.asset_type AS 자산유형,
    COUNT(*) AS 보유수량
FROM asset_assignments aa
INNER JOIN assets a ON aa.asset_id = a.asset_id
INNER JOIN basicinfoview b ON aa.employee_number = b.member_id
WHERE aa.returned_date IS NULL
GROUP BY b.team_code, a.asset_type
ORDER BY b.team_code, a.asset_type;
*/


-- 본부별 총 자산 현황
/*
SELECT
    -- 본부 정보가 basicinfoview에 없다면 hrtransferhistory2와 조인 필요
    a.asset_type AS 자산유형,
    COUNT(*) AS 총수량,
    SUM(a.price) AS 총자산가치
FROM asset_assignments aa
INNER JOIN assets a ON aa.asset_id = a.asset_id
WHERE aa.returned_date IS NULL
GROUP BY a.asset_type
ORDER BY 총자산가치 DESC;
*/
