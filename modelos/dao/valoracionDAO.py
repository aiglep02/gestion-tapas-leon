from modelos.ConexionMYSQL import conectar
from modelos.vo.valoracionVO import ValoracionVO

class ValoracionDAO:
    def __init__(self):
        self.conn = conectar()
        self.cursor = self.conn.cursor()

    def insertar_valoracion(self, valoracionVO):
        try:
            self.cursor.execute("""
                INSERT INTO valoracion (id_usuario, id_tapa, puntuacion, comentario)
                VALUES (%s, %s, %s, %s)
            """, (
                valoracionVO.id_usuario,
                valoracionVO.id_tapa,
                valoracionVO.puntuacion,
                valoracionVO.comentario
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error al insertar valoración:", e)
            return False
