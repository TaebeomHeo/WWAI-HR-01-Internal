import mysql.connector

DB_CONFIG = {
    'host': '61.37.80.105',
    'port': 3306,
    'database': 'dbwisewiresdb',
    'user': 'wisewires',
    'password': 'wiseadmin140!'
}

def execute_query(query):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Fetch column names
            columns = [col[0] for col in cursor.description]
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            cursor.close()
            return columns, rows
        else:
            print("Failed to connect to the database.")
            return None, None
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        return None, None
    finally:
        if conn and conn.is_connected():
            conn.close()

def natural_language_to_sql(nl_query):
    # This is a placeholder for a more sophisticated NL to SQL engine.
    # For now, we'll map a few example natural language queries to predefined SQL.
    if "모든 직원 목록" in nl_query:
        return """
        SELECT
            member_id AS 사번,
            name_kor AS 이름,
            team_code AS 팀코드,
            position_code AS 직급,
            join_date AS 입사일,
            current_project_name AS 현재프로젝트
        FROM basicinfoview
        ORDER BY join_date;
        """
    elif "최근 발령 내역" in nl_query:
        return """
        SELECT
            employee_number AS 사번,
            name AS 직원명,
            assignment_date AS 발령일,
            assignment_type AS 발령유형,
            division AS 본부,
            team_name AS 팀명,
            project_name AS 프로젝트명,
            role AS 역할
        FROM hrtransferhistory2
        WHERE assignment_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        ORDER BY assignment_date DESC;
        """
    elif "본부별 프로젝트 인원 현황" in nl_query or "이번주 프로젝트별 인원 현황" in nl_query:
        return """
        SELECT
            division AS 본부,
            COUNT(DISTINCT employee_number) AS 인원수
        FROM hrtransferhistory2
        WHERE end_date IS NULL OR end_date = ''
        GROUP BY division
        ORDER BY 인원수 DESC;
        """
    else:
        return None

def main():
    print("HR 데이터베이스 쿼리 도구")
    print("-------------------------")
    print("현재 다음과 같은 질문을 이해하고 처리할 수 있습니다:")
    print("- '모든 직원 목록': 현재 재직 중인 모든 직원의 기본 정보를 조회합니다.")
    print("- '최근 발령 내역': 지난 7일간의 발령 내역을 조회합니다.")
    print("- '본부별 프로젝트 인원 현황': 각 본부별 현재 프로젝트에 참여 중인 인원 현황을 조회합니다.")
    print("-------------------------")

    while True:
        nl_query = input("무엇을 알고 싶으세요? (종료하려면 'exit' 입력): ")
        if nl_query.lower() == 'exit':
            break
        
        sql_query = natural_language_to_sql(nl_query)
        
        if sql_query:
            print(f"\n실행할 SQL 쿼리:\n{sql_query}")
            columns, rows = execute_query(sql_query)
            
            if columns and rows:
                # Print header
                print("-" * 100)
                print(" | ".join(columns))
                print("-" * 100)
                # Print rows
                for row in rows:
                    print(" | ".join(map(str, row)))
                print("-" * 100)
            elif columns is not None: # Means query executed but returned no rows
                 print("No results found for your query.")
        else:
            print("죄송합니다. 해당 질문에 대한 SQL 쿼리를 생성할 수 없습니다. 다른 질문을 시도해 보세요.")

if __name__ == "__main__":
    main()
