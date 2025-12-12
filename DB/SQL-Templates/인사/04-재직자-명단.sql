-- ============================================
-- 재직자 명단 조회
-- ============================================
-- 목적: 현재 재직 중인 전체 직원 명단 추출
-- 테이블: basicinfoview
-- ============================================

-- ▼▼▼ 조회 조건 설정 (여기만 수정하세요) ▼▼▼
SET @팀코드 = '';           -- 특정 팀만 조회시 팀코드 입력 (전체는 빈값)
SET @종료월 = '2025-11';    -- 프로젝트 종료 예정 월 (YYYY-MM)
-- ▲▲▲ 조회 조건 설정 ▲▲▲

-- 전체 재직자 명단
SELECT
    member_id AS 사번,
    name_kor AS 이름,
    team_code AS 팀코드,
    position_code AS 직급,
    join_date AS 입사일,
    email_address AS 이메일,
    mobile_number AS 연락처,
    current_project_name AS 현재프로젝트
FROM basicinfoview
ORDER BY team_code, name_kor;


-- 특정 팀의 재직자 명단
/*
SELECT
    member_id AS 사번,
    name_kor AS 이름,
    position_code AS 직급,
    join_date AS 입사일,
    email_address AS 이메일,
    mobile_number AS 연락처,
    current_project_name AS 현재프로젝트
FROM basicinfoview
WHERE team_code = @팀코드
ORDER BY name_kor;
*/


-- 프로젝트 종료 임박 직원 (특정 월)
/*
SELECT
    member_id AS 사번,
    name_kor AS 이름,
    team_code AS 팀코드,
    current_project_name AS 프로젝트명,
    current_project_end_date AS 종료예정일
FROM basicinfoview
WHERE current_project_end_date LIKE CONCAT(@종료월, '%')
ORDER BY current_project_end_date;
*/
