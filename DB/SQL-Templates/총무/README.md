# 총무 SQL 템플릿

## 현재 상태

총무 관련 요구사항(자산관리, 반출/반입, 재고 현황 등)을 처리하려면 **자산 관련 테이블**이 필요합니다.

현재 HR 데이터베이스에는 자산 관련 View가 확인되지 않았습니다.

## 필요한 테이블 구조

자산 관리를 위해 다음과 같은 테이블이 필요합니다:

### 1. 자산 마스터 (assets)
```sql
CREATE TABLE assets (
    asset_id INT PRIMARY KEY,
    asset_name VARCHAR(256),
    asset_type VARCHAR(50),      -- 노트북, 모니터 등
    serial_number VARCHAR(100),
    purchase_date DATE,
    price DECIMAL(12,2),
    warranty_end_date DATE,
    status VARCHAR(20)           -- 재고, 사용중, 수리중, 폐기
);
```

### 2. 자산 배정 현황 (asset_assignments)
```sql
CREATE TABLE asset_assignments (
    assignment_id INT PRIMARY KEY,
    asset_id INT,
    employee_number VARCHAR(10),
    assigned_date DATE,
    returned_date DATE,
    location VARCHAR(100)
);
```

### 3. 자산 이동 이력 (asset_movements)
```sql
CREATE TABLE asset_movements (
    movement_id INT PRIMARY KEY,
    asset_id INT,
    movement_type VARCHAR(20),   -- 반출, 반입
    movement_date DATE,
    from_location VARCHAR(100),
    to_location VARCHAR(100),
    notes TEXT
);
```

## 자산 테이블 확보 후

자산 관련 테이블이 확보되면 다음 SQL 템플릿을 사용할 수 있습니다:
- 01-자산-반출반입-현황.sql
- 02-부서별-팀별-자산현황.sql
- 03-재고-현황-및-예측.sql

## 현재 가능한 작업

프로젝트 정보를 활용하여 간접적으로 자원 현황을 파악할 수 있습니다:
- 프로젝트별 투입 인원 현황
- 프로젝트 종료 예정에 따른 자원 회수 계획
