-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'trabajador') NOT NULL,
    intentos_fallidos INT DEFAULT 0,
    bloqueado TINYINT(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla de proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contacto VARCHAR(255),
    condiciones_pago TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla de piezas
CREATE TABLE IF NOT EXISTS piezas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(255),
    stock INT DEFAULT 0,
    umbral_minimo INT DEFAULT 0,
    fecha_vencimiento DATE,
    proveedor_id INT,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla de historial de precios
CREATE TABLE IF NOT EXISTS precios_anteriores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pieza_id INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    fecha_actualizacion DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (pieza_id) REFERENCES piezas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla de kits
CREATE TABLE IF NOT EXISTS kits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla de relación entre kits y piezas
CREATE TABLE IF NOT EXISTS kits_piezas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kit_id INT NOT NULL,
    pieza_id INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (kit_id) REFERENCES kits(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (pieza_id) REFERENCES piezas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla de órdenes de compra
CREATE TABLE IF NOT EXISTS ordenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pieza_id INT NOT NULL,
    cantidad INT NOT NULL,
    fecha_creacion DATE DEFAULT (CURRENT_DATE),
    estado VARCHAR(50) DEFAULT 'pendiente',
    aprobado_por INT,
    FOREIGN KEY (pieza_id) REFERENCES piezas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (aprobado_por) REFERENCES usuarios(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla de errores o auditoría
CREATE TABLE IF NOT EXISTS errores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    mensaje TEXT,
    origen_html TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
