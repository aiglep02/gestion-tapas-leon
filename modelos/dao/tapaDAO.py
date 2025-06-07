from modelos.vo.tapaVO import TapaVO
from modelos.ConexionMYSQL import conectar 

class TapaDAO:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def obtener_todas_las_tapas(self):
        try:
            self.cursor.execute("SELECT id, nombre, precio FROM Tapa WHERE stock > 0")
            return self.cursor.fetchall()
        except Exception as e:
            print("Error al obtener tapas:", e)
            return []

    def insertar_tapa(self, tapaVO):
        try:
            self.cursor.execute(
                "INSERT INTO Tapa (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
                (tapaVO.nombre, tapaVO.descripcion, tapaVO.precio, tapaVO.stock)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print("Error al insertar tapa:", e)
            return False


