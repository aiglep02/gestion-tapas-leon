from PyQt5.QtWidgets import QMessageBox
class ControladorUsuarios:
    def __init__(self, conexion):
        self.db = conexion

    def obtener_usuarios(self):
        cursor = self.db.cursor(dictionary=True)
        sql = "SELECT id, nombre, email, rol FROM usuario"
        cursor.execute(sql)
        return cursor.fetchall()

    def eliminar_usuario(self, usuario_id):
        cursor = self.db.cursor()
        # Eliminar primero valoraciones asociadas
        cursor.execute("DELETE FROM valoracion WHERE id_usuario = %s", (usuario_id,))
        # Eliminar lineas de pedido relacionadas con sus pedidos
        cursor.execute("DELETE FROM lineapedido WHERE pedido_id IN (SELECT id FROM pedido WHERE usuario_id = %s)", (usuario_id,))
        # Eliminar pedidos del usuario
        cursor.execute("DELETE FROM pedido WHERE usuario_id = %s", (usuario_id,))
        # Eliminar el propio usuario
        cursor.execute("DELETE FROM usuario WHERE id = %s", (usuario_id,))
        self.db.commit()
        return cursor.rowcount


    def actualizar_rol_usuario(self, usuario_id, nuevo_rol):
        cursor = self.db.cursor()
        cursor.execute("UPDATE usuario SET rol = %s WHERE id = %s", (nuevo_rol, usuario_id))
        self.db.commit()
        return cursor.rowcount
    
    def crear_usuario(self, nombre, email, contrasena_hash, rol):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)",
            (nombre, email, contrasena_hash, rol)
        )
        self.db.commit()
