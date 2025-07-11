from controladores.ControladorLogin import ControladorLogin
from vistas.ventana_registro import VentanaRegistro
from vistas.ventana_admin import VentanaAdmin
from vistas.ventana_empleado import VentanaEmpleado
from vistas.ventana_cliente import VentanaClienteRegistrado
from vistas.ventana_invitado import VentanaInvitado

class Coordinador:
    def __init__(self):
        self.login_controller = ControladorLogin() 
        self.registro_ventana = VentanaRegistro(self)  
        self.intentos_fallidos = 0

    def login(self, email, contrasena, rol_ingresado, login_vista):
        resultado = self.login_controller.verificar_credenciales(email, contrasena, rol_ingresado)

        if resultado is None or resultado[0] is None:
            self.intentos_fallidos += 1
            login_vista.mostrar_error("Credenciales incorrectas.")
            if self.intentos_fallidos >= 3:
                print("[ERROR] Demasiados intentos fallidos. Cerrando aplicación.")
                exit(0)
            return

        usuario_vo, error = resultado

        if error:
            self.intentos_fallidos += 1
            login_vista.mostrar_error(error)
            if self.intentos_fallidos >= 3:
                print("[ERROR] Demasiados intentos fallidos. Cerrando aplicación.")
                exit(0)
            return

        self.intentos_fallidos = 0
        login_vista.close()
        print(f"[INFO] Login correcto: {usuario_vo.nombre} ({usuario_vo.rol})")

        rol = usuario_vo.rol.lower().strip()
        if rol == "admin":
            self.abrir_panel_admin(usuario_vo)
        elif rol == "empleado":
            self.abrir_panel_empleado(usuario_vo)
        else:
            self.abrir_panel_cliente(usuario_vo)

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
        self.invitado = VentanaInvitado(self)
        self.invitado.show()

    def mostrar_registro(self):
        self.registro_ventana.show()
