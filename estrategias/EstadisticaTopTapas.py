from estrategias.IEstrategiaEstadistica import IEstrategiaEstadistica

class EstadisticaTopTapas(IEstrategiaEstadistica):
    def calcular(self, conexion):
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.nombre, SUM(p.cantidad) AS total_pedida
            FROM pedido p
            JOIN tapa t ON p.id_tapa = t.id
            GROUP BY t.id
            ORDER BY total_pedida DESC
        """)
        return cursor.fetchall()