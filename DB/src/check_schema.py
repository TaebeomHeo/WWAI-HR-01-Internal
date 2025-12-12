import pymysql

# DB 접속
conn = pymysql.connect(
    host='61.37.80.105',
    port=3306,
    user='wisewires',
    password='wiseadmin140!',
    database='dbwisewiresdb',
    charset='utf8mb4'
)

cursor = conn.cursor()

print("=" * 70)
print("hrtransferhistory2 테이블 구조")
print("=" * 70)
cursor.execute("DESCRIBE hrtransferhistory2")
for row in cursor.fetchall():
    print(row)

print("\n")
print("=" * 70)
print("projectinfoview 테이블 구조")
print("=" * 70)
cursor.execute("DESCRIBE projectinfoview")
for row in cursor.fetchall():
    print(row)

conn.close()
