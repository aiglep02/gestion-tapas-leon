import hashlib
from modelos.vo.usuarioVO import UsuarioVO

class UsuarioDAO:
    def __init__(self, conexion):
        self.db = conexion

    def verificar_credenciales(self, email, contrasena):
        """
        Verifica si un usuario con el email y contraseña hash existe.
        Devuelve un UsuarioVO si existe, o None si no.
        """
        cursor = self.db.cursor(dictionary=True)
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

        sql = """
        SELECT id, nombre, email, rol 
        FROM usuario 
        WHERE email = %s AND contraseña = %s
        """
        cursor.execute(sql, (email, contrasena_hash))
        fila = cursor.fetchone()

        if fila:
            return UsuarioVO(
                id_usuario=fila["id"],
                nombre=fila["nombre"],
                email=fila["email"],
                rol=fila["rol"]
            )
        return None

    def email_existente(self, email):
        """
        Comprueba si ya existe un usuario con ese email.
        """
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        return resultado[0] > 0 if resultado else False

    def nombre_existente(self, nombre):
        """
        Comprueba si ya existe un usuario con ese nombre.
        """
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        return resultado[0] > 0 if resultado else False
