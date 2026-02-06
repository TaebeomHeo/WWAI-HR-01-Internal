import mysql.connector

DB_CONFIG = {
    'host': '61.37.80.105',
    'port': 3306,
    'database': 'dbwisewiresdb',
    'user': 'wisewires',
    'password': 'wiseadmin140!'
}

def final_check():
    query = """
    SELECT DISTINCT
        name,
        project_name,
        assignment_date,
        end_date
    FROM hrtransferhistory2
    WHERE
        LOWER(project_name) LIKE '%hm%'
        AND (
            (assignment_date <= '2025-12-31') AND
            (end_date >= '2025-01-01' OR end_date IS NULL OR end_date = '')
        )
    ORDER BY project_name, name;
    """
    
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if not rows:
                print("No projects found matching 'hm' (case-insensitive) in 2025.")
            else:
                print(f"{'Name':<15} | {'Project Name':<40} | {'Start Date':<12} | {'End Date':<12}")
                print("-" * 85)
                for row in rows:
                    name, project, start, end = row
                    start_str = str(start) if start else ""
                    end_str = str(end) if end else "Present"
                    if not end: end_str = "Present"
                    print(f"{name:<15} | {project:<40} | {start_str:<12} | {end_str:<12}")
            cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    final_check()
