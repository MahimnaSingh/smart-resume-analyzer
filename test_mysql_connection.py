import pymysql

connection = None  # So we can safely close it later

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='943519',
        unix_socket='/tmp/mysql.sock',
        database='cv'  # <- changed from 'project' to 'cv'
    )
    print("Connection successful!")

    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        print("Connected to database:", result)

except pymysql.MySQLError as e:
    print(f"Error: {e}")

finally:
    if connection:
        connection.close()


