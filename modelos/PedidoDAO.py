from modelos.ConexionMYSQL import ConexionMYSQL
"""
class PedidoDAO:
    def __init__(self):
        self.db = ConexionMYSQL().conexion

    def insertarPedido(self, pedidoVO):
        cursor = self.db.cursor()
        sql = "INSERT INTO pedido (usuario_id) VALUES (%s)"
        cursor.execute(sql, (pedidoVO.id_usuario,))
        self.db.commit()
        return cursor.lastrowid  # ID del pedido recién creado
""" 

class PedidoDAO:
    def __init__(self, conexion):
        self.db = conexion

    def insertarPedido(self, pedidoVO):
        cursor = self.db.cursor()
        sql = "INSERT INTO pedido (usuario_id) VALUES (%s)"
        cursor.execute(sql, (pedidoVO.id_usuario,))
        return cursor.lastrowid




