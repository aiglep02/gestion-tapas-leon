# Gestión de Tapas León

## Descripción del Proyecto

Esta aplicación de escritorio, desarrollada en Python utilizando el framework PyQt5, tiene como objetivo principal la gestión de pedidos y valoraciones de tapas de un bar en la ciudad de León. Ofrece una interfaz intuitiva para usuarios con diferentes roles (cliente, empleado, administrador), permitiendo una interacción fluida con el sistema de tapas local.

## Características

* **Autenticación y Roles:** Sistema de login robusto con roles de usuario diferenciados (cliente, empleado, administrador).
* **Catálogo de Tapas:** Visualización y gestión del listado de tapas disponibles.
* **Gestión de Pedidos:** Funcionalidades para crear nuevos pedidos, hacer seguimiento de su estado y gestionarlos a lo largo de su ciclo de vida.
* **Valoración de Tapas:** Permite a los usuarios valorar las tapas, contribuyendo a un sistema de clasificación.
* **Estadísticas Avanzadas:** Proporciona a los administradores la capacidad de ver estadísticas, como las tapas mejor valoradas.
* **Interfaz de Usuario:** Interfaz de usuario atractiva y personalizable mediante hojas de estilo Qt (QSS).

## Requisitos

Para ejecutar esta aplicación, asegúrate de tener instalados los siguientes componentes en tu sistema:

* **Python 3.x**
* **MySQL Server** - Versión 8.0+ recomendada.
* **Pip** (el gestor de paquetes de Python)

## Instalación y Configuración

Sigue estos pasos para configurar y poner en marcha el proyecto en tu máquina local:

### 1. Clonar el Repositorio (o descargar el código)

Si el proyecto está en un repositorio Git:

```bash
git clone <URL_DEL_REPOSITORIO>
cd gestion-tapas-leon
```

### 2. Configuración del Entorno Python
Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto.

```bash
# Crear el entorno virtual (solo la primera vez)
python -m venv env

# Activar el entorno virtual
# En Windows:
.\env\Scripts\activate
# En macOS/Linux:
source env/bin/activate

# Instalar las dependencias del proyecto
pip install -r requirements.txt
```
### 3. Configuración de la Base de Datos MySQL
La aplicación se conecta a una base de datos MySQL llamada gestion_tapas.

* **Abrir tu Cliente MySQL:**
Abre tu cliente de MySQL (ej. MySQL Workbench, DBeaver, o la línea de comandos de MySQL).

* **Ejecutar el Script SQL Completo:**
Ejecuta el siguiente script SQL para crear la base de datos y todas las tablas con su estructura final, tal como las tienes ahora:

```bash
-- -----------------------------------------------------
-- Script SQL de Configuración de la Base de Datos 'gestion_tapas'
-- Generado automáticamente en base a tu esquema actual.
-- -----------------------------------------------------

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS gestion_tapas;
USE gestion_tapas;

-- -----------------------------------------------------
-- Tabla `usuario`
-- -----------------------------------------------------
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('cliente','empleado','administrador','admin') NOT NULL DEFAULT 'cliente',
  `preferencias` text,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Tabla `tapas`
-- -----------------------------------------------------
CREATE TABLE `tapas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `activa` tinyint(1) DEFAULT '1',
  `premium` tinyint(1) DEFAULT '0',
  `categoria` varchar(50) DEFAULT NULL,
  `popularidad` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_tapas_categoria` (`categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Tabla `pedido`
-- NOTA SOBRE EL DISEÑO:
-- Esta tabla incluye `id_tapa` y `cantidad`, lo que implica que
-- este registro de `pedido` está diseñado para una ÚNICA tapa.
-- Si un pedido debe contener múltiples tapas (variedad),
-- la tabla `pedido_tapas` gestionaría esos detalles.
-- -----------------------------------------------------
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `id_tapa` int NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('creado','confirmado','preparando','listo','entregado','cancelado','en preparación') DEFAULT 'creado',
  `total` decimal(10,2) DEFAULT NULL,
  `direccion_entrega` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`usuario_id`),
  KEY `idx_pedidos_estado` (`estado`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE
  -- Nota: No se añadió FK para id_tapa aquí en tu esquema actual, aunque la lógica del Python lo usa.
  -- Si es un FK, puedes añadir: CONSTRAINT `fk_pedido_tapa_simple` FOREIGN KEY (`id_tapa`) REFERENCES `tapas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Tabla `pedido_tapas`
-- Esta tabla maneja los detalles de las tapas dentro de un pedido
-- para el caso de que un pedido tenga múltiples ítems.
-- -----------------------------------------------------
CREATE TABLE `pedido_tapas` (
  `id_pedido` int NOT NULL,
  `id_tapa` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `precio_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_pedido`,`id_tapa`),
  KEY `id_tapa` (`id_tapa`),
  CONSTRAINT `pedido_tapas_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedido_tapas_ibfk_2` FOREIGN KEY (`id_tapa`) REFERENCES `tapas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedido_tapas_chk_1` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Tabla `valoracion`
-- -----------------------------------------------------
CREATE TABLE `valoracion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_tapa` int NOT NULL,
  `usuario_id` int NOT NULL,
  `puntuacion` int NOT NULL,
  `comentario` text,
  `fecha_valoracion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_valoracion_tapa` (`id_tapa`),
  KEY `fk_valoracion_usuario` (`usuario_id`),
  CONSTRAINT `fk_valoracion_tapa` FOREIGN KEY (`id_tapa`) REFERENCES `tapas` (`id`),
  CONSTRAINT `fk_valoracion_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `valoracion_chk_1` CHECK (((`puntuacion` >= 1) and (`puntuacion` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Inserción de Datos de Ejemplo (Opcional)
-- -----------------------------------------------------
-- Puedes añadir aquí sentencias INSERT INTO para poblar tu base de datos con datos iniciales
-- de usuarios, tapas, etc., para pruebas.
/*
-- Ejemplo de usuario administrador:
-- ¡IMPORTANTE! Asegúrate de hashear la contraseña si tu aplicación lo requiere.
INSERT INTO usuario (nombre, email, contraseña, rol) VALUES ('admin_test', 'admin@example.com', 'mi_pass_segura', 'admin');
INSERT INTO usuario (nombre, email, contraseña, rol) VALUES ('cliente_ejemplo', 'cliente@example.com', 'pass_cliente', 'cliente');

-- Ejemplo de tapas:
INSERT INTO tapas (nombre, descripcion, activa, premium, categoria, popularidad) VALUES ('Croqueta de Jamón', 'Clásica croqueta de jamón ibérico', 1, 0, 'Clásica', 150);
INSERT INTO tapas (nombre, descripcion, activa, premium, categoria, popularidad) VALUES ('Mini Hamburguesa', 'Pequeña hamburguesa con queso y bacon', 1, 0, 'Moderna', 200);
INSERT INTO tapas (nombre, descripcion, activa, premium, categoria, popularidad) VALUES ('Ensaladilla Rusa', 'Porción de ensaladilla casera', 1, 0, 'Vegetariana', 100);
*/
```


### 4. Configurar la Conexión en Python:
Abre el archivo modelos/ConexionMYSQL.py y asegúrate de que los detalles de conexión (host, user, password, database) coincidan con tu configuración de MySQL.

```bash
# modelos/ConexionMYSQL.py
import mysql.connector

class ConexionMYSQL:
    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super(ConexionMYSQL, cls).__new__(cls)
            cls._instancia._conectar()
        return cls._instancia

    def _conectar(self):
        self._conexion = mysql.connector.connect(
            host='localhost', # O la IP de tu servidor MySQL si no es local
            user='root',      # O tu usuario de MySQL
            password='bdpass',# O tu contraseña de MySQL
            database='gestion_tapas'
        )

    def obtener_conexion(self):
        try:
            self._conexion.ping(reconnect=True, attempts=3, delay=2)
        except mysql.connector.errors.OperationalError:
            print("[INFO] Reconectando a la base de datos...")
            self._conectar()
        return self._conexion

def conectar():
    return ConexionMYSQL().obtener_conexion()
```

## Uso de la aplicación
Para ejecutar la aplicación, asegúrate de estar en el entorno virtual activado y en la raíz del proyecto (gestion-tapas-leon), luego ejecuta:

```bash
python main.py
```

## Estructura del proyecto

```bash
.
├── controladores/       # Contiene la lógica de negocio y controladores de la aplicación.
├── modelos/             # Define los modelos de datos y las clases de acceso a datos (DAO/VO).
│   ├── dao/             # Data Access Objects (lógica de interacción con la BD).
│   └── vo/              # Value Objects (estructuras de datos para los modelos).
├── vistas/              # Archivos de interfaz de usuario, ventanas y elementos visuales.
├── estrategias/         # Implementación de patrones de diseño como el patrón Estrategia.
├── estilos/             # Hojas de estilo Qt (QSS) para la personalización visual de la UI.
│   └── estilo.qss
├── main.py              # Punto de entrada principal de la aplicación.
├── README.md            # Este archivo de documentación.
├── login.ui             # Archivo de diseño de la ventana de login (creado con Qt Designer).
├── requirements.txt     # Lista de dependencias de Python del proyecto.
└── ...                  # Otros archivos y directorios del proyecto.
```


