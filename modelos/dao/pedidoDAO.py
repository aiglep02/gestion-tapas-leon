from modelos.ConexionMYSQL import conectar 
from modelos.vo.pedidoVO import PedidoVO

class PedidoDAO:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def insertar_pedido(self, pedidoVO):
        try:
            self.cursor.execute(
                "INSERT INTO pedido (usuario_id, id_tapa, cantidad, estado) VALUES (%s, %s, %s, %s)",
                (pedidoVO.id_usuario, pedidoVO.id_tapa, pedidoVO.cantidad, pedidoVO.estado)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print("Error al insertar pedido:", e)
            return False

    def obtener_pedidos_por_usuario(self, usuario_id):
        try:
            self.cursor.execute("""
                SELECT p.id, t.nombre, p.cantidad, p.estado, p.fecha
                FROM pedido p
                JOIN tapa t ON p.id_tapa = t.id
                WHERE p.usuario_id = %s
                ORDER BY p.fecha DESC
            """, (usuario_id,))
            resultados = self.cursor.fetchall()
            print(f"Pedidos del usuario {usuario_id}:", resultados)
            return resultados
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
        
    def actualizar_estado_pedido(self, id_pedido, nuevo_estado):
        try:
            self.cursor.execute(
                "UPDATE pedido SET estado = %s WHERE id = %s",
                (nuevo_estado, id_pedido)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print("Error al actualizar estado del pedido:", e)
            return False










