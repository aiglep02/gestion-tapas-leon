from modelos.ConexionJDBC import conectar

class LineaPedidoDAO:
    def __init__(self):
        self.db = conectar()  

    def insertarLineaPedido(self, lineaVO):
        cursor = self.db.cursor()
        sql = "INSERT INTO lineapedido (pedido_id, tapa_id, cantidad) VALUES (%s, %s, %s)"
        cursor.execute(sql, (lineaVO.id_pedido, lineaVO.id_tapa, lineaVO.cantidad))
        self.db.commit()
