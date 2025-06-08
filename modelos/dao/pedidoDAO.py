from modelos.ConexionMYSQL import conectar 
from modelos.vo.pedidoVO import PedidoVO

class PedidoDAO:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def insertar_pedido(self, pedidoVO):
        try:
            if not pedidoVO.id_usuario or not pedidoVO.id_tapa or not pedidoVO.cantidad or not pedidoVO.estado:
                raise ValueError("Datos incompletos para insertar el pedido.")
            
            self.cursor.execute("""
                INSERT INTO pedido (usuario_id, id_tapa, cantidad, estado)
                VALUES (%s, %s, %s, %s)
            """, (
                pedidoVO.id_usuario,
                pedidoVO.id_tapa,
                pedidoVO.cantidad,
                pedidoVO.estado
            ))

            print(f"Pedido insertado con ID: {self.cursor.lastrowid}")
            self.conn.commit()
            pedidoVO.id = self.cursor.lastrowid
            return pedidoVO.id

        except Exception as e:
            print("Error al insertar pedido:", e)
            return None

    def obtener_pedidos_por_usuario(self, usuario_id):
        try:
            self.cursor.execute("""
                SELECT p.id, t.nombre AS tapa, p.cantidad, p.estado
                FROM pedido p
                JOIN tapa t ON p.id_tapa = t.id
                WHERE p.usuario_id = %s
                ORDER BY p.fecha DESC
            """, (usuario_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print("Error al obtener pedidos:", e)
            return []
        
    def obtener_pedidos_pendientes(self):
        try:
            self.cursor.execute("""
                SELECT p.id, u.nombre AS cliente, t.nombre AS tapa, p.cantidad, p.estado, p.fecha
                FROM pedido p
                JOIN usuario u ON p.usuario_id = u.id
                JOIN tapa t ON p.id_tapa = t.id
                WHERE p.estado != 'entregado'
                ORDER BY p.fecha ASC
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print("Error al obtener pedidos:", e)
            return []
        
    def actualizar_estado_pedido(self, pedido_id, estado):
        try:
            self.cursor.execute("""
                UPDATE pedido
                SET estado = %s
                WHERE id = %s
            """, (estado, pedido_id))
            self.conn.commit()
            return True  # 
        except Exception as e:
            print("Error al actualizar estado del pedido:", e)
            return False

    def obtener_pedidos_entregados_por_usuario(self, usuario_id):
        try:
            self.cursor.execute("""
                SELECT DISTINCT t.id, t.nombre
                FROM pedido p
                JOIN tapa t ON p.id_tapa = t.id
                WHERE p.usuario_id = %s AND p.estado = 'entregado'
            """, (usuario_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print("Error al obtener tapas entregadas:", e)
            return []
        
    def actualizar_tapa_pedido(self, pedido_id, nueva_tapa_id):
        try:
            cursor = self.conn.cursor()
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
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM pedido WHERE id = %s AND estado = 'en preparación'", (pedido_id,))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            print("Error al eliminar pedido:", e)
            return 0