from modelos.dao.tapaDAO import TapaDAO

class ControladorTapa:
    def __init__(self):
        self.tapa_dao = TapaDAO()

    def obtener_tapas(self):
        return self.tapa_dao.obtener_todas_las_tapas()

    def reducir_stock(self, nombre_tapa, cantidad):
        self.tapa_dao.reducir_stock_por_nombre(nombre_tapa, cantidad)
