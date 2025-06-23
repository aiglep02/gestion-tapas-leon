from modelos.dao.tapaDAO import TapaDAO
from modelos.ConexionJDBC import conectar

class TapaService:
    def __init__(self, conexion=None):
        # Permite inyectar conexión desde fuera, útil para testing o controladores
        self.dao = TapaDAO(conexion if conexion else conectar())

    def obtener_todas_las_tapas(self):
        return self.dao.obtener_todas_las_tapas()

    def insertar_tapa(self, tapa_vo):
        return self.dao.insertar_tapa(tapa_vo)

    def actualizar_tapa(self, tapa_id, nombre=None, descripcion=None, precio=None, stock=None):
        return self.dao.actualizar_tapa(tapa_id, nombre, descripcion, precio, stock)

    def eliminar_tapa(self, tapa_id):
        return self.dao.eliminar_tapa(tapa_id)

    def reducir_stock_por_id(self, id_tapa, cantidad):
        return self.dao.reducir_stock_por_id(id_tapa, cantidad)

    def reducir_stock_por_nombre(self, nombre_tapa, cantidad):
        return self.dao.reducir_stock_por_nombre(nombre_tapa, cantidad)

    def obtener_nombre_por_id(self, id_tapa):
        return self.dao.obtener_nombre_por_id(id_tapa)

    def obtener_datos_para_estadisticas(self):
        return self.dao.obtener_datos_para_estadisticas()
