import mysql.connector
import os

DB_CONFIG = {
    'host': '61.37.80.105',
    'port': 3306,
    'database': 'dbwisewiresdb',
    'user': 'wisewires',
    'password': 'wiseadmin140!'
}

def get_schema_markdown():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if not conn.is_connected():
            return "Failed to connect to the database."

        cursor = conn.cursor()

        # Get list of tables
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
        tables = cursor.fetchall()
        
        # Get list of views
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()

        markdown_content = "# 데이터베이스 스키마 문서\n\n"
        
        # Document Tables
        markdown_content += "## Tables\n\n"
        if tables:
            for (table_name, _) in tables:
                markdown_content += f"### {table_name}\n\n"
                cursor.execute(f"DESCRIBE `{table_name}`")
                schema = cursor.fetchall()
                
                markdown_content += "| Column Name | Type | Null | Key | Default | Extra |\n"
                markdown_content += "|-------------|------|------|-----|---------|-------|\n"
                for col in schema:
                    markdown_content += f"| {' | '.join(map(str, col))} |\n"
                markdown_content += "\n"
        else:
            markdown_content += "No tables found.\n\n"

        # Document Views
        markdown_content += "## Views\n\n"
        if views:
            for (view_name, _) in views:
                markdown_content += f"### {view_name}\n\n"
                cursor.execute(f"DESCRIBE `{view_name}`")
                schema = cursor.fetchall()
                
                markdown_content += "| Column Name | Type | Null | Key | Default | Extra |\n"
                markdown_content += "|-------------|------|------|-----|---------|-------|\n"
                for col in schema:
                    # Replace None with empty string for cleaner markdown
                    cleaned_col = ["" if v is None else v for v in col]
                    markdown_content += f"| {' | '.join(map(str, cleaned_col))} |\n"
                markdown_content += "\n"
        else:
            markdown_content += "No views found.\n\n"

        cursor.close()
        return markdown_content

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if conn and conn.is_connected():
            conn.close()

def main():
    output_filename = "database_schema_documentation.md"
    markdown_data = get_schema_markdown()

    if "Error" in markdown_data or "Failed" in markdown_data:
        print(f"An error occurred:\n{markdown_data}")
        return

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(markdown_data)
    
    print(f"데이터베이스 스키마 문서가 '{output_filename}' 파일로 저장되었습니다.")
    print("파일의 처음 20줄을 출력합니다:\n")
    with open(output_filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 20:
                break
            print(line, end="")


if __name__ == "__main__":
    main()
