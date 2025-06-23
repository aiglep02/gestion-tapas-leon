class PedidoVO:
    def __init__(self, id_usuario, id_tapa=None, cantidad=None, id=None, estado="En preparación"):
        self.id = id
        self.id_usuario = id_usuario
        self.id_tapa = id_tapa
        self.cantidad = cantidad
        self.estado = estado

    def __repr__(self):
        return (
            f"<PedidoVO id={self.id}, id_usuario={self.id_usuario}, id_tapa={self.id_tapa}, "
            f"cantidad={self.cantidad}, estado='{self.estado}'>"
        )

    def __eq__(self, other):
        if not isinstance(other, PedidoVO):
            return False
        return (
            self.id == other.id and
            self.id_usuario == other.id_usuario and
            self.id_tapa == other.id_tapa and
            self.cantidad == other.cantidad and
            self.estado == other.estado
        )
