from modelos.ConexionJDBC import conectar
import hashlib
from modelos.vo.usuarioVO import UsuarioVO

class UsuarioDAO:
    def __init__(self):
        self.db = conectar()

    def verificar_credenciales(self, email, contrasena):
        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        sql = "SELECT id, nombre, email, rol FROM usuario WHERE email = ? AND contraseña = ?"
        cursor = self.db.cursor()
        cursor.execute(sql, (email, contrasena_hash))
        fila = cursor.fetchone()
        cursor.close()

        if fila:
            return UsuarioVO(
                id_usuario=fila[0],
                nombre=fila[1],
                email=fila[2],
                rol=fila[3]
            )
        return None

    def email_existente(self, email):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0] > 0 if resultado else False

    def nombre_existente(self, nombre):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0] > 0 if resultado else False

    def insertar_usuario(self, usuario_vo, contrasena_hash):
        sql = """
            INSERT INTO usuario (nombre, email, contraseña, rol)
            VALUES (?, ?, ?, ?)
        """
        valores = (usuario_vo.nombre, usuario_vo.email, contrasena_hash, usuario_vo.rol)
        cursor = self.db.cursor()
        cursor.execute(sql, valores)
        self.db.commit()
        cursor.close()

    def insertar_usuario_manual(self, nombre, email, contrasena_hash, rol):
        cursor = self.db.cursor()
        sql = """
            INSERT INTO usuario (nombre, email, contraseña, rol)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (nombre, email, contrasena_hash, rol))
        self.db.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]

        cursor.close()
        return last_id

    def obtener_todos(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, nombre, email, rol FROM usuario")
        resultados = cursor.fetchall()
        cursor.close()
        return [
            UsuarioVO(
                id_usuario=row[0],
                nombre=row[1],
                email=row[2],
                rol=row[3]
            ) for row in resultados
        ]

    def eliminar_por_id(self, id_usuario):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = ?", (id_usuario,))
        self.db.commit()
        cursor.close()

    def actualizar_rol(self, id_usuario, nuevo_rol):
        cursor = self.db.cursor()
        cursor.execute("UPDATE usuario SET rol = ? WHERE id = ?", (nuevo_rol, id_usuario))
        self.db.commit()
        cursor.close()

    def obtener_pedidos_por_usuario(self, id_usuario):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT id FROM pedido WHERE usuario_id = ?", (id_usuario,))
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Exception as e:
            print("Error al comprobar pedidos del usuario:", e)
            return []
