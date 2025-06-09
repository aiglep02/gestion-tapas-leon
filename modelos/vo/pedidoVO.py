class PedidoVO:
    def __init__(self, id_usuario, id_tapa=None, cantidad=None, id=None, estado="En preparación"):
        self.id = id
        self.id_usuario = id_usuario
        self.id_tapa = id_tapa
        self.cantidad = cantidad
        self.estado = estado

    def __repr__(self):
        return (f"<PedidoVO id={self.id}, usuario={self.id_usuario}, tapa={self.id_tapa}, "
                f"cantidad={self.cantidad}, estado={self.estado}>")
