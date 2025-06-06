class ControladorLogin:
    def __init__(self, conexion):
        self.db = conexion

    def verificar_credenciales(self, email, contraseña):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT id, nombre, rol FROM usuario WHERE email = %s AND contraseña = %s"
        cursor.execute(sql, (email, contraseña))
        resultado = cursor.fetchone()
        return resultado

