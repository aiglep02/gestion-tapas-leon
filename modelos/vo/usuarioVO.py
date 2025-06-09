# modelos/vo/UsuarioVO.py

class UsuarioVO:
    def __init__(self, id_usuario, nombre, email, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.rol = rol

    def __str__(self):
        return f"UsuarioVO(id={self.id_usuario}, nombre={self.nombre}, rol={self.rol})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, UsuarioVO):
            return False
        return (self.id_usuario == other.id_usuario and
                self.nombre == other.nombre and
                self.email == other.email and
                self.rol == other.rol)
