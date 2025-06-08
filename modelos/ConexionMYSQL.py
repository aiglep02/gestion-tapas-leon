"""
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
"""
import mysql.connector
from mysql.connector.errors import OperationalError

class ConexionMYSQL:
    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super(ConexionMYSQL, cls).__new__(cls)
            cls._instancia._conectar()
        return cls._instancia

    def _conectar(self):
        self._conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='bdpass',
            database='gestion_tapas'
        )

    def obtener_conexion(self):
        try:
            self._conexion.ping(reconnect=True, attempts=3, delay=2)
        except OperationalError:
            print("[INFO] Reconectando a la base de datos...")
            self._conectar()
        return self._conexion

def conectar():
    return ConexionMYSQL().obtener_conexion()
