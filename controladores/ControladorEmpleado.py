class ControladorEmpleado:
    def __init__(self, conexion):
        self.db = conexion

    def obtener_pedidos_pendientes(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
            SELECT p.id, p.fecha, p.estado, u.nombre AS cliente
            FROM pedido p
            JOIN usuario u ON p.usuario_id = u.id
            WHERE p.estado IN ('pendiente', 'en preparación')
            ORDER BY p.fecha ASC
        """
        cursor.execute(sql)
        return cursor.fetchall()

    def obtener_lineas_pedido(self, pedido_id):
        cursor = self.db.cursor(dictionary=True)
        sql = """
            SELECT lp.id, t.nombre, lp.cantidad
            FROM lineapedido lp
            JOIN tapa t ON lp.tapa_id = t.id
            WHERE lp.pedido_id = %s
        """
        cursor.execute(sql, (pedido_id,))
        return cursor.fetchall()

    def actualizar_estado_pedido(self, pedido_id, nuevo_estado):
        cursor = self.db.cursor()
        sql = "UPDATE pedido SET estado = %s WHERE id = %s"
        cursor.execute(sql, (nuevo_estado, pedido_id))
        self.db.commit()
        return cursor.rowcount  # 1 si se actualizó, 0 si no
