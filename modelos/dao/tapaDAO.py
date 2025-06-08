from modelos.vo.tapaVO import TapaVO
from modelos.ConexionMYSQL import conectar 

class TapaDAO:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def obtener_todas_las_tapas(self):
        try:
            self.cursor.execute("SELECT id, nombre, stock FROM Tapa")
            return self.cursor.fetchall()
        except Exception as e:
            print("Error al obtener tapas:", e)
            return []

    def insertar_tapa(self, tapaVO):
        try:
            self.cursor.execute(
                "INSERT INTO Tapa (nombre, descripcion, stock) VALUES (%s, %s, %s)",
                (tapaVO.nombre, tapaVO.descripcion, tapaVO.stock)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print("Error al insertar tapa:", e)
            return False

    def reducir_stock_por_nombre(self, nombre_tapa, cantidad):
        try:
            self.cursor.execute(
                "UPDATE Tapa SET stock = stock - %s WHERE nombre = %s AND stock >= %s",
                (cantidad, nombre_tapa, cantidad)
            )
            self.conn.commit()
        except Exception as e:
            print(f"[ERROR] No se pudo reducir stock: {e}")
