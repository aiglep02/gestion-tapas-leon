from estrategias.IEstrategiaEstadistica import IEstrategiaEstadistica

class EstadisticaTopValoradas(IEstrategiaEstadistica):
    def calcular(self, conexion):
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.nombre, AVG(v.puntuacion) AS puntuacion_media
            FROM valoracion v
            JOIN tapa t ON v.id_tapa = t.id
            GROUP BY t.id
            ORDER BY puntuacion_media DESC
            LIMIT 5
        """)
        return cursor.fetchall()
