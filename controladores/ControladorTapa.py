from modelos.logica.TapaService import TapaService

class ControladorTapa:
    def __init__(self):
        self.service = TapaService()  

    def obtener_tapas(self):
        return self.service.obtener_todas_las_tapas()

    def reducir_stock(self, id_tapa, cantidad):
        return self.service.reducir_stock_por_id(id_tapa, cantidad)

    def reducir_stock_por_nombre(self, nombre_tapa, cantidad):
        return self.service.reducir_stock_por_nombre(nombre_tapa, cantidad)
