import hashlib
from modelos.vo.usuarioVO import UsuarioVO

class UsuarioDAO:
    def __init__(self, conexion):
        self.db = conexion

    def verificar_credenciales(self, email, contrasena):
        cursor = self.db.cursor(dictionary=True)

        # 🔐 Convertir a hash antes de comparar
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

        sql = "SELECT id, nombre, email, rol FROM usuario WHERE email = %s AND contraseña = %s"
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
