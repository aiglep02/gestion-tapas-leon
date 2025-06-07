from controladores.ControladorLogin import ControladorLogin
from modelos.ConexionMYSQL import ConexionMYSQL

conexion = ConexionMYSQL().conexion

try:
    email = 'real@correo.com'
    contraseña = '1234'

    login = ControladorLogin(conexion)
    usuario = login.verificar_credenciales(email, contraseña)

    if usuario:
        print(f"Login correcto. Bienvenido {usuario['nombre']} (rol: {usuario['rol']})")
    else:
        print("Credenciales incorrectas")

except Exception as e:
    print("Error:", e)

finally:
    conexion.close()
