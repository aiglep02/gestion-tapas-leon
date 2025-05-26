import mysql.connector

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='bdpass',
        database='gestion_tapas'
    )
