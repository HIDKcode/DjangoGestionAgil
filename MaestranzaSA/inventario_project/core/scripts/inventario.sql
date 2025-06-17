DROP TABLE IF EXISTS errores;
DROP TABLE IF EXISTS ordenes;
DROP TABLE IF EXISTS kits_piezas;
DROP TABLE IF EXISTS kits;
DROP TABLE IF EXISTS precios_anteriores;
DROP TABLE IF EXISTS piezas;
DROP TABLE IF EXISTS proveedores;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rut VARCHAR(12) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    rol ENUM('admin', 'inventario', 'comprador', 'logistica', 'produccion', 'auditor', 'gerente', 'planta') NOT NULL DEFAULT 'planta',
    intentos_fallidos INT DEFAULT 0,
    bloqueado TINYINT(1) DEFAULT 0,
    is_staff TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1
);

CREATE TABLE proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto TEXT,
    condiciones_pago TEXT
);

CREATE TABLE piezas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(100),
    stock INT DEFAULT 0,
    umbral_minimo INT DEFAULT 0,
    fecha_vencimiento DATE,
    proveedor_id INT,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

CREATE TABLE precios_anteriores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pieza_id INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    fecha_actualizacion DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (pieza_id) REFERENCES piezas(id)
);

CREATE TABLE kits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE kits_piezas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kit_id INT NOT NULL,
    pieza_id INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (kit_id) REFERENCES kits(id),
    FOREIGN KEY (pieza_id) REFERENCES piezas(id)
);

CREATE TABLE ordenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pieza_id INT NOT NULL,
    cantidad INT NOT NULL,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(50) DEFAULT 'pendiente',
    aprobado_por INT,
    FOREIGN KEY (pieza_id) REFERENCES piezas(id),
    FOREIGN KEY (aprobado_por) REFERENCES usuarios(id)
);

CREATE TABLE errores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    mensaje TEXT,
    origen_html TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
