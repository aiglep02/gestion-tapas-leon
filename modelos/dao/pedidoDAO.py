from modelos.vo.pedidoVO import PedidoVO

class PedidoDAO:
    def __init__(self, conexion):
        self.conn = conexion  

    def insertar_pedido(self, pedidoVO):
        try:
            if pedidoVO.id_tapa is None or pedidoVO.cantidad is None or pedidoVO.estado is None:
                raise ValueError("Datos incompletos para insertar el pedido.")
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO pedido (usuario_id, id_tapa, cantidad, estado)
                VALUES (?, ?, ?, ?)
            """, (
                pedidoVO.id_usuario,
                pedidoVO.id_tapa,
                pedidoVO.cantidad,
                pedidoVO.estado
            ))
            pedidoVO.id = cursor.lastrowid
            self.conn.commit()
            cursor.close()
            print(f"Pedido insertado con ID: {pedidoVO.id}")
            return pedidoVO.id

        except Exception as e:
            print("Error al insertar pedido:", e)
            return None

    def obtener_pedidos_por_usuario(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, id_tapa, cantidad, estado
                FROM pedido
                WHERE usuario_id = ?
                ORDER BY fecha DESC
            """, (usuario_id,))
            filas = cursor.fetchall()
            cursor.close()

            return [
                PedidoVO(
                    id_usuario=usuario_id,
                    id_tapa=f[1],
                    cantidad=f[2],
                    id=f[0],
                    estado=f[3]
                ) for f in filas
            ]
        except Exception as e:
            print("Error al obtener pedidos:", e)
            return []

    def obtener_pedidos_pendientes(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, usuario_id, id_tapa, cantidad, estado
                FROM pedido
                WHERE estado != 'entregado'
                ORDER BY fecha ASC
            """)
            filas = cursor.fetchall()
            cursor.close()

            return [
                PedidoVO(
                    id=f[0],
                    id_usuario=f[1],
                    id_tapa=f[2],
                    cantidad=f[3],
                    estado=f[4]
                ) for f in filas
            ]
        except Exception as e:
            print("Error al obtener pedidos pendientes:", e)
            return []

    def actualizar_estado_pedido(self, pedido_id, estado):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE pedido
                SET estado = ?
                WHERE id = ?
            """, (estado, pedido_id))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Error al actualizar estado del pedido:", e)
            return False

    def entregar_pedido(self, pedido_id, nombre_tapa, cantidad):
        try:
            exito = self.actualizar_estado_pedido(pedido_id, "entregado")
            if exito:
                cursor = self.conn.cursor()
                cursor.execute("""
                    UPDATE tapa
                    SET stock = stock - ?
                    WHERE nombre = ?
                """, (cantidad, nombre_tapa))
                self.conn.commit()
                cursor.close()
                return True
            return False
        except Exception as e:
            print("Error al entregar pedido y reducir stock:", e)
            return False

    def obtener_pedidos_entregados_por_usuario(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT DISTINCT t.id, t.nombre
                FROM pedido p
                JOIN tapa t ON p.id_tapa = t.id
                WHERE p.usuario_id = ? AND p.estado = 'entregado'
            """, (usuario_id,))
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Exception as e:
            print("Error al obtener tapas entregadas:", e)
            return []

    def actualizar_tapa_pedido(self, pedido_id, nueva_tapa_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE pedido
                SET id_tapa = ?
                WHERE id = ? AND estado = 'en preparación'
            """, (nueva_tapa_id, pedido_id))
            self.conn.commit()
            cursor.close()
            return cursor.rowcount
        except Exception as e:
            print("Error al cambiar tapa:", e)
            return 0

    def eliminar_pedido(self, pedido_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM pedido WHERE id = ? AND estado = 'en preparación'", (pedido_id,))
            self.conn.commit()
            cursor.close()
            return cursor.rowcount
        except Exception as e:
            print("Error al eliminar pedido:", e)
            return 0

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
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Exception as e:
            print("Error al obtener datos para estadísticas:", e)
            return []
