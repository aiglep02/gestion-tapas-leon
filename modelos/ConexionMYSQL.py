# modelos/ConexionMYSQL.py

import mysql.connector

class ConexionMYSQL:
    _instancia = None  # ← Singleton: única instancia

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super(ConexionMYSQL, cls).__new__(cls)
            cls._instancia._conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='bdpass',
                database='gestion_tapas'
            )
        return cls._instancia

    def obtener_conexion(self):
        return self._conexion

# ⚠️ Esta es la función que usarás en todos los archivos
def conectar():
    return ConexionMYSQL().obtener_conexion()
