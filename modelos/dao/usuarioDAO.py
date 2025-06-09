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
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        sql = """
        SELECT id, nombre, email, rol 
        FROM usuario 
        WHERE email = %s AND contraseña = %s
        """
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (email, contrasena_hash))
            fila = cursor.fetchone()
            # 🔒 Consumimos todos los resultados para evitar el error
            while cursor.nextset():
                pass

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
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE email = %s", (email,))
            resultado = cursor.fetchone()
        return resultado[0] > 0 if resultado else False

    def nombre_existente(self, nombre):
        """
        Comprueba si ya existe un usuario con ese nombre.
        """
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE nombre = %s", (nombre,))
            resultado = cursor.fetchone()
        return resultado[0] > 0 if resultado else False

    def insertar_usuario(self, usuario_vo, contrasena_hash):
        """
        Inserta un nuevo usuario con el hash de contraseña.
        """
        sql = """
            INSERT INTO usuario (nombre, email, contraseña, rol)
            VALUES (%s, %s, %s, %s)
        """
        valores = (usuario_vo.nombre, usuario_vo.email, contrasena_hash, usuario_vo.rol)
        with self.db.cursor() as cursor:
            cursor.execute(sql, valores)
        self.db.commit()

    def obtener_todos(self):
        """
        Devuelve todos los usuarios como una lista de UsuarioVO.
        """
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id, nombre, email, rol FROM usuario")
            resultados = cursor.fetchall()
        return [
            UsuarioVO(
                id_usuario=row["id"],
                nombre=row["nombre"],
                email=row["email"],
                rol=row["rol"]
            ) for row in resultados
        ]

    def eliminar_por_id(self, id_usuario):
        """
        Elimina un usuario dado su ID.
        """
        with self.db.cursor() as cursor:
            cursor.execute("DELETE FROM usuario WHERE id = %s", (id_usuario,))
        self.db.commit()

    def actualizar_rol(self, id_usuario, nuevo_rol):
        """
        Actualiza el rol de un usuario por su ID.
        """
        with self.db.cursor() as cursor:
            cursor.execute("UPDATE usuario SET rol = %s WHERE id = %s", (nuevo_rol, id_usuario))
        self.db.commit()
