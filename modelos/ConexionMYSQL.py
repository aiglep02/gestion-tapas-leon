"""
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='bdpass',
        database='gestion_tapas'
    )
"""
import mysql.connector

class ConexionMYSQL:
    def __init__(self, database='gestion_tapas'):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='bdpass',
            database=database
        )

def conectar():
    return ConexionMYSQL().conexion
