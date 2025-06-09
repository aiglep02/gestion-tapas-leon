from modelos.vo.tapaVO import TapaVO
from modelos.vo.EstadisticaVO import EstadisticaVO
from modelos.ConexionMYSQL import conectar 

class TapaDAO:
    def __init__(self):
        self.conn = conectar()

    def obtener_todas_las_tapas(self):
        try:
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre, descripcion, stock FROM tapa")
                filas = cursor.fetchall()

            tapas = [
                TapaVO(
                    id_tapa=fila['id'],
                    nombre=fila['nombre'],
                    descripcion=fila.get('descripcion'),
                    stock=fila['stock']
                ) for fila in filas
            ]
            return tapas
        except Exception as e:
            print("Error al obtener tapas:", e)
            return []

    def obtener_datos_para_estadisticas(self):
        try:
            with self.conn.cursor(dictionary=True) as cursor:
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

            estadisticas = [
                EstadisticaVO(
                    nombre=fila['nombre'],
                    total_pedida=fila['total_pedida'],
                    puntuacion_media=fila['puntuacion_media']
                ) for fila in filas
            ]
            return estadisticas

        except Exception as e:
            print("Error al obtener datos para estadísticas:", e)
            return []

    def insertar_tapa(self, tapaVO):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tapa (nombre, descripcion, stock) VALUES (%s, %s, %s)",
                    (tapaVO.nombre, tapaVO.descripcion, tapaVO.stock)
                )
                self.conn.commit()
                return True
        except Exception as e:
            print("Error al insertar tapa:", e)
            return False

    def reducir_stock_por_nombre(self, nombre_tapa, cantidad):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE tapa SET stock = stock - %s WHERE nombre = %s AND stock >= %s",
                    (cantidad, nombre_tapa, cantidad)
                )
                self.conn.commit()
        except Exception as e:
            print(f"[ERROR] No se pudo reducir stock: {e}")
