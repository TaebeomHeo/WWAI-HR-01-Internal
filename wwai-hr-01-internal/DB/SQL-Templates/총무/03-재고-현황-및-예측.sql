-- ============================================
-- 재고 현황 및 예측 조회
-- ============================================
-- 목적: 자산 재고 현황 파악 및 구매 필요성 예측
-- 테이블: assets, asset_assignments
-- ============================================
-- NOTE: 현재 자산 관련 테이블이 없습니다.
-- 아래는 자산 테이블이 생성된 후 사용할 템플릿입니다.
-- ============================================

-- 자산 유형별 재고 현황
/*
SELECT
    a.asset_type AS 자산유형,
    COUNT(*) AS 전체수량,
    SUM(CASE WHEN a.status = '재고' THEN 1 ELSE 0 END) AS 재고수량,
    SUM(CASE WHEN a.status = '사용중' THEN 1 ELSE 0 END) AS 사용중,
    SUM(CASE WHEN a.status = '수리중' THEN 1 ELSE 0 END) AS 수리중,
    ROUND(SUM(CASE WHEN a.status = '재고' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS 재고비율
FROM assets a
WHERE a.status != '폐기'
GROUP BY a.asset_type
ORDER BY 재고비율;
*/


-- 보증 만료 임박 자산 (3개월 이내)
/*
SELECT
    a.asset_type AS 자산유형,
    a.asset_name AS 자산명,
    a.serial_number AS 시리얼번호,
    a.warranty_end_date AS 보증만료일,
    DATEDIFF(a.warranty_end_date, CURDATE()) AS 남은일수
FROM assets a
WHERE a.warranty_end_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 3 MONTH)
  AND a.status != '폐기'
ORDER BY a.warranty_end_date;
*/


-- 구매 필요성 예측
-- (재고 < 월평균 사용량인 경우 구매 필요)
/*
WITH monthly_usage AS (
    SELECT
        a.asset_type,
        COUNT(*) / 3.0 AS avg_monthly_usage
    FROM asset_movements am
    INNER JOIN assets a ON am.asset_id = a.asset_id
    WHERE am.movement_type = '반출'
      AND am.movement_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
    GROUP BY a.asset_type
),
current_stock AS (
    SELECT
        asset_type,
        COUNT(*) AS stock_count
    FROM assets
    WHERE status = '재고'
    GROUP BY asset_type
)
SELECT
    cs.asset_type AS 자산유형,
    cs.stock_count AS 현재재고,
    ROUND(mu.avg_monthly_usage, 1) AS 월평균사용,
    CASE
        WHEN cs.stock_count < mu.avg_monthly_usage THEN '구매필요'
        WHEN cs.stock_count < mu.avg_monthly_usage * 2 THEN '구매검토'
        ELSE '충분'
    END AS 구매필요성
FROM current_stock cs
LEFT JOIN monthly_usage mu ON cs.asset_type = mu.asset_type
ORDER BY
    CASE
        WHEN cs.stock_count < IFNULL(mu.avg_monthly_usage, 0) THEN 1
        WHEN cs.stock_count < IFNULL(mu.avg_monthly_usage, 0) * 2 THEN 2
        ELSE 3
    END;
*/


-- ▼▼▼ 조회 기간 설정 (여기만 수정하세요) ▼▼▼
SET @시작일 = '2025-11-01';  -- 조회 시작일
SET @종료일 = '2025-11-30';  -- 조회 종료일
-- ▲▲▲ 조회 기간 설정 ▲▲▲

-- 프로젝트 종료에 따른 자산 회수 예상 (간접 조회)
-- 자산 테이블이 없어도 프로젝트 종료 예정으로 자원 반납 예상 가능
SELECT
    project_name AS 프로젝트명,
    client_company AS 고객사,
    end_date AS 종료예정일,
    COUNT(DISTINCT employee_number) AS 투입인원
FROM hrtransferhistory2
WHERE end_date >= @시작일
  AND end_date <= @종료일
  AND end_date != ''
GROUP BY project_name, client_company, end_date
ORDER BY end_date;
