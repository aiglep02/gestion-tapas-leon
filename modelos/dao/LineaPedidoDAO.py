from modelos.ConexionMYSQL import ConexionMYSQL
"""
class LineaPedidoDAO:
    def __init__(self):
        self.db = ConexionMYSQL().conexion

    def insertarLineaPedido(self, lineaVO):
        cursor = self.db.cursor()
        sql = "INSERT INTO lineapedido (pedido_id, tapa_id, cantidad) VALUES (%s, %s, %s)"
        cursor.execute(sql, (lineaVO.id_pedido, lineaVO.id_tapa, lineaVO.cantidad))
        self.db.commit()
"""
class LineaPedidoDAO:
    def __init__(self, conexion):
        self.db = conexion

    def insertarLineaPedido(self, lineaVO):
        cursor = self.db.cursor()
        sql = "INSERT INTO lineapedido (pedido_id, tapa_id, cantidad) VALUES (%s, %s, %s)"
        cursor.execute(sql, (lineaVO.id_pedido, lineaVO.id_tapa, lineaVO.cantidad))
