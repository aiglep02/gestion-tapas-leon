# modelo/vo/UsuarioVO.py

class UsuarioVO:
    def __init__(self, id_usuario, nombre, email, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.rol = rol

    def __str__(self):
        return f"UsuarioVO(id={self.id_usuario}, nombre={self.nombre}, rol={self.rol})"
