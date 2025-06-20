import jaydebeapi
import os

class ConexionJDBC:
    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super(ConexionJDBC, cls).__new__(cls)
            cls._instancia._conectar()
        return cls._instancia

    def _conectar(self):
        try:
            # Ruta al conector JDBC .jar (debes poner aquí la ruta real)
            ruta_jar = os.path.abspath("lib/mysql-connector-j-9.3.0.jar")
            driver = "com.mysql.cj.jdbc.Driver"
            url = "jdbc:mysql://localhost:3306/gestion_tapas"
            usuario = "root"
            contrasena = "bdpass"

            self._conexion = jaydebeapi.connect(driver, url, [usuario, contrasena], ruta_jar)
            print("[INFO] Conexión JDBC establecida.")
        except Exception as e:
            print("[ERROR] Fallo al conectar vía JDBC:", e)
            self._conexion = None

    def obtener_conexion(self):
        return self._conexion

def conectar():
    return ConexionJDBC().obtener_conexion()
