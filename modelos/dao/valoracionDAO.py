
from modelos.ConexionJDBC import conectar
from modelos.vo.valoracionVO import ValoracionVO

class ValoracionDAO:
    def __init__(self):
        self.conn = conectar()

    def insertar_valoracion(self, valoracionVO):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO valoracion (id_usuario, id_tapa, puntuacion, comentario)
                    VALUES (?, ?, ?, ?)
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
