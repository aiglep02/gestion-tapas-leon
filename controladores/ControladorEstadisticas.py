class ControladorEstadisticas:
    def __init__(self, conexion):
        self.db = conexion

    def tapas_mas_pedidas(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
            SELECT t.nombre, SUM(lp.cantidad) AS total_pedida
            FROM lineapedido lp
            JOIN tapa t ON lp.tapa_id = t.id
            GROUP BY t.id
            ORDER BY total_pedida DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()

    def pedidos_por_estado(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
            SELECT estado, COUNT(*) AS cantidad
            FROM pedido
            GROUP BY estado
        """
        cursor.execute(sql)
        return cursor.fetchall()
