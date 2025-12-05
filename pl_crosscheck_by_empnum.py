import pymysql
import pandas as pd

# DB 접속
conn = pymysql.connect(
    host='61.37.80.105',
    port=3306,
    user='wisewires',
    password='wiseadmin140!',
    database='dbwisewiresdb',
    charset='utf8mb4'
)

print("=" * 70)
print("1. hrtransferhistory2에서 2025년 10월 PL 조회 (사번 + 이름)")
print("=" * 70)

# Query 1: hrtransferhistory2에서 PL 조회 - 사번과 이름 모두
query1 = """
SELECT DISTINCT
    employee_number AS 사번,
    name AS 이름,
    role,
    assignment_date AS 시작일,
    end_date AS 종료일,
    project_name AS 프로젝트명
FROM hrtransferhistory2
WHERE role = 'PL'
  AND assignment_date <= '2025-10-31'
  AND (end_date IS NULL OR end_date = '' OR end_date >= '2025-10-01')
ORDER BY employee_number
"""

df_transfer = pd.read_sql(query1, conn)
print(f"\n총 {len(df_transfer)}건의 PL 발령 이력이 있습니다.")

# 사번과 이름 매핑 딕셔너리
transfer_pl_dict = dict(zip(df_transfer['사번'], df_transfer['이름']))
transfer_pl_set = set(df_transfer['사번'].tolist())
print(f"고유 사번 수: {len(transfer_pl_set)}명")
print(f"\n사번 목록: {sorted(transfer_pl_set)}")

print("\n")
print("=" * 70)
print("2. projectinfoview에서 2025년 10월 활성 프로젝트 PL 조회 (사번 + 이름)")
print("=" * 70)

# Query 2: projectinfoview에서 PL 조회 - 사번과 이름 모두
query2 = """
SELECT DISTINCT
    project_leader AS 사번,
    project_leader_name AS 이름,
    project_name AS 프로젝트명,
    start_date AS 시작일,
    end_date AS 종료일
FROM projectinfoview
WHERE start_date <= '2025-10-31'
  AND (end_date IS NULL OR end_date = '' OR end_date >= '2025-10-01')
  AND project_leader IS NOT NULL
  AND project_leader != ''
ORDER BY project_leader
"""

df_project = pd.read_sql(query2, conn)
print(f"\n총 {len(df_project)}개 프로젝트가 있습니다.")

# 사번과 이름 매핑 딕셔너리
project_pl_dict = dict(zip(df_project['사번'], df_project['이름']))
project_pl_set = set(df_project['사번'].tolist())
print(f"고유 PL 사번 수: {len(project_pl_set)}명")
print(f"\n사번 목록: {sorted(project_pl_set)}")

print("\n")
print("=" * 70)
print("3. 사번 기준 Cross-Check 결과")
print("=" * 70)

# Cross-check
both = transfer_pl_set & project_pl_set
only_transfer = transfer_pl_set - project_pl_set
only_project = project_pl_set - transfer_pl_set

print(f"\n[양쪽 모두에 있는 PL] - {len(both)}명")
print("-" * 50)
if both:
    for emp_num in sorted(both):
        name = transfer_pl_dict.get(emp_num, project_pl_dict.get(emp_num, 'N/A'))
        print(f"  사번: {emp_num}, 이름: {name}")
else:
    print("  없음")

print(f"\n[발령이력에만 있는 PL (프로젝트 미배정)] - {len(only_transfer)}명")
print("-" * 50)
if only_transfer:
    for emp_num in sorted(only_transfer):
        name = transfer_pl_dict.get(emp_num, 'N/A')
        print(f"  사번: {emp_num}, 이름: {name}")
        # 해당 발령 정보도 출력
        projects = df_transfer[df_transfer['사번'] == emp_num]['프로젝트명'].tolist()
        for proj in projects:
            print(f"    - 발령 프로젝트: {proj}")
else:
    print("  없음")

print(f"\n[프로젝트에만 있는 PL (발령이력 없음)] - {len(only_project)}명")
print("-" * 50)
if only_project:
    for emp_num in sorted(only_project):
        name = project_pl_dict.get(emp_num, 'N/A')
        print(f"  사번: {emp_num}, 이름: {name}")
        # 해당 프로젝트 정보도 출력
        projects = df_project[df_project['사번'] == emp_num]['프로젝트명'].tolist()
        for proj in projects:
            print(f"    - 프로젝트: {proj}")
else:
    print("  없음")

print("\n")
print("=" * 70)
print("4. 요약")
print("=" * 70)
print(f"\n발령이력(hrtransferhistory2) PL 수: {len(transfer_pl_set)}명")
print(f"프로젝트(projectinfoview) PL 수: {len(project_pl_set)}명")
print(f"양쪽 일치: {len(both)}명")
print(f"발령이력에만 존재: {len(only_transfer)}명")
print(f"프로젝트에만 존재: {len(only_project)}명")

conn.close()
print("\n완료!")
