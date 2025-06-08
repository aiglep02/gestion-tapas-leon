from estrategias.IEstrategiaEstadistica import IEstrategiaEstadistica

class EstadisticaTopTapas(IEstrategiaEstadistica):
    def calcular(self, conexion):
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.nombre, SUM(lp.cantidad) AS total_pedida
            FROM lineapedido lp
            JOIN tapa t ON lp.tapa_id = t.id
            GROUP BY t.id
            ORDER BY total_pedida DESC
        """)
        return cursor.fetchall()

