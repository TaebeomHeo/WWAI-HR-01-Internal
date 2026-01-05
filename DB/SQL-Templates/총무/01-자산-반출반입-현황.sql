-- ============================================
-- 자산 반출/반입 현황 조회
-- ============================================
-- 목적: 자산의 반출/반입 이력 및 현황 파악
-- 테이블: asset_movements, assets, basicinfoview
-- ============================================
-- NOTE: 현재 자산 관련 테이블이 없습니다.
-- 아래는 자산 테이블이 생성된 후 사용할 템플릿입니다.
-- ============================================

-- 최근 1개월 반출/반입 현황
/*
SELECT
    am.movement_type AS 구분,
    am.movement_date AS 일자,
    b.name_kor AS 직원명,
    b.team_code AS 팀코드,
    a.asset_type AS 자산유형,
    a.asset_name AS 자산명,
    a.serial_number AS 시리얼번호,
    am.from_location AS 출발지,
    am.to_location AS 도착지,
    am.notes AS 비고
FROM asset_movements am
INNER JOIN assets a ON am.asset_id = a.asset_id
INNER JOIN basicinfoview b ON am.employee_number = b.member_id
WHERE am.movement_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
ORDER BY am.movement_date DESC, am.movement_type;
*/


-- 현재 반출 중인 자산 (미반납)
/*
SELECT
    b.name_kor AS 사용자,
    b.team_code AS 팀코드,
    a.asset_type AS 자산유형,
    a.asset_name AS 자산명,
    a.serial_number AS 시리얼번호,
    aa.assigned_date AS 반출일,
    DATEDIFF(CURDATE(), aa.assigned_date) AS 사용일수
FROM asset_assignments aa
INNER JOIN assets a ON aa.asset_id = a.asset_id
INNER JOIN basicinfoview b ON aa.employee_number = b.member_id
WHERE aa.returned_date IS NULL
ORDER BY aa.assigned_date;
*/
