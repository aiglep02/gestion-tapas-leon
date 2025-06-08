from controladores.ControladorLogin import ControladorLogin
from controladores.controladorRegistro import VentanaRegistro
from vistas.ventana_admin import VentanaAdmin
from vistas.ventana_empleado import VentanaEmpleado
from vistas.ventana_cliente import VentanaClienteRegistrado
from vistas.ventana_invitado import VentanaInvitado

class Coordinador:
    def __init__(self, conexion):
        self.conexion = conexion
        self.login_controller = ControladorLogin(conexion)
        self.registro_ventana = VentanaRegistro()
        self.intentos_fallidos = 0

    def login(self, email, contrasena, rol_ingresado, login_vista):
        usuario_vo = self.login_controller.verificar_credenciales(email, contrasena)
        if usuario_vo:
            rol_real = usuario_vo.rol.lower().strip()
            rol_ingresado = rol_ingresado.lower().strip()

            print(f"[DEBUG] Comparando rol → BD: '{rol_real}' | Seleccionado: '{rol_ingresado}'")

            if rol_real != rol_ingresado:
                login_vista.mostrar_error(f"El usuario no es {rol_ingresado}.")
                return

            self.intentos_fallidos = 0
            login_vista.close()

            print(f"[INFO] Login correcto: {usuario_vo.nombre} ({usuario_vo.rol})")

            if rol_real == "admin":
                self.abrir_panel_admin(usuario_vo)
            elif rol_real == "empleado":
                self.abrir_panel_empleado(usuario_vo)
            else:
                self.abrir_panel_cliente(usuario_vo)
        else:
            self.intentos_fallidos += 1
            login_vista.mostrar_error("Credenciales incorrectas.")
            if self.intentos_fallidos >= 3:
                print("[ERROR] Demasiados intentos fallidos. Cerrando aplicación.")
                exit(0)

    def abrir_panel_admin(self, usuario_vo):
        self.admin = VentanaAdmin(usuario_vo.nombre, self)
        self.admin.setWindowTitle(f"Admin - {usuario_vo.nombre}")
        self.admin.show()

    def abrir_panel_empleado(self, usuario_vo):
        self.empleado = VentanaEmpleado(usuario_vo.nombre, self)
        self.empleado.setWindowTitle(f"Empleado - {usuario_vo.nombre}")
        self.empleado.show()

    def abrir_panel_cliente(self, usuario_vo):
        self.cliente = VentanaClienteRegistrado(usuario_vo.id_usuario, usuario_vo.nombre, self)
        self.cliente.setWindowTitle(f"Cliente - {usuario_vo.nombre}")
        self.cliente.show()


    def mostrar_vista_invitado(self):
        from vistas.ventana_invitado import VentanaInvitado
        self.invitado = VentanaInvitado(self)
        self.invitado.show()

    def mostrar_registro(self):
        self.registro_ventana.show()
