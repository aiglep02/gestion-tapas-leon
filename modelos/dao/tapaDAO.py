from modelos.vo.tapaVO import TapaVO
from modelos.vo.EstadisticaVO import EstadisticaVO

class TapaDAO:
    def __init__(self, conexion):
        self.conn = conexion

    def obtener_todas_las_tapas(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, precio, stock FROM tapa")
            filas = cursor.fetchall()

            tapas = [
                TapaVO(
                    id_tapa=fila[0],
                    nombre=fila[1],
                    descripcion=fila[2],
                    precio=fila[3],
                    stock=fila[4]
                ) for fila in filas
            ]
            cursor.close()
            return tapas
        except Exception as e:
            print("Error al obtener tapas:", e)
            return []

    def insertar_tapa(self, tapaVO):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO tapa (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)",
                (tapaVO.nombre, tapaVO.descripcion, tapaVO.precio, tapaVO.stock)
            )
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Error al insertar tapa:", e)
            return False

    def actualizar_tapa(self, tapa_id, nombre=None, descripcion=None, precio=None, stock=None):
        try:
            campos = []
            valores = []

            if nombre:
                campos.append("nombre = ?")
                valores.append(nombre)
            if descripcion:
                campos.append("descripcion = ?")
                valores.append(descripcion)
            if precio is not None:
                campos.append("precio = ?")
                valores.append(precio)
            if stock is not None:
                campos.append("stock = ?")
                valores.append(stock)

            if not campos:
                return 0  # No hay nada que actualizar

            sql = f"UPDATE tapa SET {', '.join(campos)} WHERE id = ?"
            valores.append(tapa_id)

            cursor = self.conn.cursor()
            cursor.execute(sql, valores)
            self.conn.commit()
            cursor.close()
            return cursor.rowcount
        except Exception as e:
            print("Error al actualizar tapa:", e)
            return 0

    def eliminar_tapa(self, tapa_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM tapa WHERE id = ?", (tapa_id,))
            self.conn.commit()
            cursor.close()
            return cursor.rowcount
        except Exception as e:
            print("Error al eliminar tapa:", e)
            return 0

    def reducir_stock_por_id(self, id_tapa, cantidad):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE tapa SET stock = stock - ? WHERE id = ?", (cantidad, id_tapa))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Error al reducir stock:", e)
            return False

    def obtener_nombre_por_id(self, id_tapa):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT nombre FROM tapa WHERE id = ?", (id_tapa,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado[0] if resultado else None
        except Exception as e:
            print("Error al obtener nombre de tapa:", e)
            return None

    def obtener_datos_para_estadisticas(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    t.nombre, 
                    IFNULL(SUM(p.cantidad), 0) AS total_pedida,
                    IFNULL(AVG(v.puntuacion), 0) AS puntuacion_media
                FROM tapa t
                LEFT JOIN pedido p ON t.id = p.id_tapa
                LEFT JOIN valoracion v ON t.id = v.id_tapa
                GROUP BY t.id
            """)
            filas = cursor.fetchall()
            cursor.close()

            # Convertimos a objetos VO si vas a usarlos como tal en las estrategias
            estadisticas = [
                EstadisticaVO(
                    nombre=fila[0],
                    total_pedida=fila[1],
                    puntuacion_media=fila[2]
                ) for fila in filas
            ]
            return estadisticas
        except Exception as e:
            print("Error al obtener estadísticas:", e)
            return []
        
    def reducir_stock_por_nombre(self, nombre_tapa, cantidad):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE tapa SET stock = stock - ? WHERE nombre = ?", (cantidad, nombre_tapa))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Error al reducir stock por nombre:", e)
            return False
