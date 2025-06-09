from modelos.ConexionMYSQL import conectar 
from modelos.vo.pedidoVO import PedidoVO

class PedidoDAO:
    def __init__(self):
        self.conn = conectar()

    def insertar_pedido(self, pedidoVO):
        try:
            if pedidoVO.id_tapa is None or pedidoVO.cantidad is None or pedidoVO.estado is None:
                raise ValueError("Datos incompletos para insertar el pedido.")
            
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pedido (usuario_id, id_tapa, cantidad, estado)
                    VALUES (%s, %s, %s, %s)
                """, (
                    pedidoVO.id_usuario,
                    pedidoVO.id_tapa,
                    pedidoVO.cantidad,
                    pedidoVO.estado
                ))
                pedidoVO.id = cursor.lastrowid
                self.conn.commit()
                print(f"Pedido insertado con ID: {pedidoVO.id}")
                return pedidoVO.id

        except Exception as e:
            print("Error al insertar pedido:", e)
            return None

    def obtener_pedidos_por_usuario(self, usuario_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, id_tapa, cantidad, estado
                    FROM pedido
                    WHERE usuario_id = %s
                    ORDER BY fecha DESC
                """, (usuario_id,))
                filas = cursor.fetchall()

            pedidos = []
            for fila in filas:
                pedidos.append(PedidoVO(
                    id_usuario=usuario_id,
                    id_tapa=fila[1],
                    cantidad=fila[2],
                    id=fila[0],
                    estado=fila[3]
                ))
            return pedidos

        except Exception as e:
            print("Error al obtener pedidos:", e)
            return []

    def obtener_pedidos_pendientes(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, usuario_id, id_tapa, cantidad, estado
                    FROM pedido
                    WHERE estado != 'entregado'
                    ORDER BY fecha ASC
                """)
                filas = cursor.fetchall()

            pedidos = []
            for fila in filas:
                pedidos.append(PedidoVO(
                    id=fila[0],
                    id_usuario=fila[1],
                    id_tapa=fila[2],
                    cantidad=fila[3],
                    estado=fila[4]
                ))
            return pedidos

        except Exception as e:
            print("Error al obtener pedidos pendientes:", e)
            return []

    def actualizar_estado_pedido(self, pedido_id, estado):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE pedido
                    SET estado = %s
                    WHERE id = %s
                """, (estado, pedido_id))
                self.conn.commit()
            return True
        except Exception as e:
            print("Error al actualizar estado del pedido:", e)
            return False

    def entregar_pedido(self, pedido_id, nombre_tapa, cantidad):
        try:
            exito = self.actualizar_estado_pedido(pedido_id, "entregado")
            if exito:
                with self.conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE tapa
                        SET stock = stock - %s
                        WHERE nombre = %s
                    """, (cantidad, nombre_tapa))
                    self.conn.commit()
                return True
            return False
        except Exception as e:
            print("Error al entregar pedido y reducir stock:", e)
            return False

    def obtener_pedidos_entregados_por_usuario(self, usuario_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT DISTINCT t.id, t.nombre
                    FROM pedido p
                    JOIN tapa t ON p.id_tapa = t.id
                    WHERE p.usuario_id = %s AND p.estado = 'entregado'
                """, (usuario_id,))
                return cursor.fetchall()
        except Exception as e:
            print("Error al obtener tapas entregadas:", e)
            return []

    def actualizar_tapa_pedido(self, pedido_id, nueva_tapa_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE pedido
                    SET id_tapa = %s
                    WHERE id = %s AND estado = 'en preparación'
                """, (nueva_tapa_id, pedido_id))
                self.conn.commit()
                return cursor.rowcount
        except Exception as e:
            print("Error al cambiar tapa:", e)
            return 0

    def eliminar_pedido(self, pedido_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM pedido WHERE id = %s AND estado = 'en preparación'", (pedido_id,))
                self.conn.commit()
                return cursor.rowcount
        except Exception as e:
            print("Error al eliminar pedido:", e)
            return 0

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
                resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print("Error al obtener datos para estadísticas:", e)
            return []
