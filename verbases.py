import mysql.connector

conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='bdpass'
)
cursor = conexion.cursor()
cursor.execute("SHOW DATABASES")
for base in cursor:
    print(base)
conexion.close()
