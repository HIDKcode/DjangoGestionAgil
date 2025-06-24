
DROP DATABASE inventario;
CREATE DATABASE inventario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE inventario;
DROP TABLE IF EXISTS errores;
DROP TABLE IF EXISTS ordenes;
DROP TABLE IF EXISTS kits_piezas;
DROP TABLE IF EXISTS kits;
DROP TABLE IF EXISTS precios_anteriores;
DROP TABLE IF EXISTS piezas;
DROP TABLE IF EXISTS proveedores;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    rut VARCHAR(12) PRIMARY KEY,
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
    fecha_actualizacion DATE,
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
    fecha_creacion DATE,
    estado VARCHAR(50) DEFAULT 'pendiente',
    aprobado_por VARCHAR(12),
    FOREIGN KEY (pieza_id) REFERENCES piezas(id),
    FOREIGN KEY (aprobado_por) REFERENCES usuarios(rut)
);

CREATE TABLE errores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_rut VARCHAR(12),
    mensaje TEXT,
    origen_html TEXT,
    FOREIGN KEY (usuario_rut) REFERENCES usuarios(rut)
);

CREATE TABLE movimiento_inventario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    pieza_id INT NOT NULL,
    accion VARCHAR(10) NOT NULL,
    cantidad INT,
    usuario_rut VARCHAR(12),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    observacion TEXT,
    FOREIGN KEY (pieza_id) REFERENCES piezas(id),
    FOREIGN KEY (usuario_rut) REFERENCES usuarios(rut)
);

-- Insert para tabla usuarios

INSERT INTO usuarios (rut, password, rol, intentos_fallidos, bloqueado, is_active, is_staff, is_superuser) VALUES
('11111111-1', 'admin', 'admin', 0, 0, 1, 0, 1),
('22222222-2', 'inventario', 'inventario', 0, 0, 1, 0, 0),
('33333333-3', 'comprador', 'comprador', 0, 0, 1, 0, 0),
('44444444-4', 'logistica', 'logistica', 0, 0, 1, 0, 0),
('55555555-5', 'produccion', 'produccion', 0, 0, 1, 0, 0),
('66666666-6', 'auditor', 'auditor', 0, 0, 1, 0, 0),
('77777777-7', 'gerente', 'gerente', 0, 0, 1, 0, 0),
('88888888-8', 'planta', 'planta', 0, 0, 1, 0, 0);

INSERT INTO usuarios (rut, password, rol, intentos_fallidos, bloqueado, is_active, is_staff, is_superuser) VALUES
('admin2', 'admin2', 'admin', 0, 0, 1, 0, 1);

-- Insert para tabla proveedores
INSERT INTO proveedores (id, nombre, contacto, condiciones_pago) VALUES
(1, 'Proveedor X', 'contacto@proveedorx.com', 'Pago a 30 días'),
(2, 'Proveedor Y', 'contacto@proveedory.com', 'Pago a 15 días');

-- Insert para tabla piezas (25 piezas variadas)
INSERT INTO piezas (id, nombre, categoria, stock, umbral_minimo, fecha_vencimiento, proveedor_id) VALUES
(1, 'Filtro hidráulico', 'Componente hidráulico', 100, 20, NULL, 1),
(2, 'Motor eléctrico 220V', 'Motor', 15, 3, NULL, 2),
(3, 'Bomba de agua', 'Bomba', 25, 5, NULL, 1),
(4, 'Engranaje metálico', 'Mecánico', 50, 10, NULL, 1),
(5, 'Correa de transmisión', 'Mecánico', 40, 10, NULL, 2),
(6, 'Rodamiento de bola', 'Mecánico', 80, 15, NULL, 1),
(7, 'Válvula neumática', 'Neumático', 30, 5, NULL, 2),
(8, 'Tubo flexible hidráulico', 'Hidráulico', 60, 10, NULL, 1),
(9, 'Sensor de temperatura', 'Electrónico', 20, 4, NULL, 2),
(10, 'Panel de control', 'Electrónico', 10, 2, NULL, 1),
(11, 'Bujía industrial', 'Electrónico', 70, 10, NULL, 2),
(12, 'Cable eléctrico 10mm', 'Eléctrico', 100, 20, NULL, 1),
(13, 'Interruptor térmico', 'Eléctrico', 35, 5, NULL, 2),
(14, 'Disco de freno', 'Mecánico', 60, 15, NULL, 1),
(15, 'Eje de transmisión', 'Mecánico', 12, 3, NULL, 2),
(16, 'Lubricante industrial', 'Químico', 90, 20, NULL, 1),
(17, 'Manómetro de presión', 'Instrumental', 22, 5, NULL, 2),
(18, 'Filtro de aire', 'Componente hidráulico', 45, 10, NULL, 1),
(19, 'Termostato', 'Electrónico', 30, 8, NULL, 2),
(20, 'Bomba de vacío', 'Bomba', 8, 2, NULL, 1),
(21, 'Correa dentada', 'Mecánico', 40, 10, NULL, 2),
(22, 'Tornillo hexagonal M10', 'Mecánico', 500, 100, NULL, 1),
(23, 'Llave inglesa', 'Herramienta', 25, 5, NULL, 2),
(24, 'Martillo de mano', 'Herramienta', 30, 5, NULL, 1),
(25, 'Taladro eléctrico', 'Herramienta', 15, 3, NULL, 2);

-- Insert para tabla kits
INSERT INTO kits (id, nombre, descripcion) VALUES
(1, 'Kit de mantenimiento hidráulico', 'Contiene piezas esenciales para mantenimiento hidráulico'),
(2, 'Kit eléctrico básico', 'Componentes eléctricos comunes para reparación'),
(3, 'Kit mecánico estándar', 'Piezas mecánicas comunes para mantenimiento');

-- Insert para tabla kits_piezas (relación kits - piezas)
INSERT INTO kits_piezas (id, kit, pieza, cantidad) VALUES
(1, 1, 1, 2),   -- Filtro hidráulico x2
(2, 1, 8, 3),   -- Tubo flexible hidráulico x3
(3, 2, 2, 1),  
(4, 2, 12, 5);  

-- Insert para tabla ordenes
INSERT INTO ordenes (id, pieza, cantidad, fecha_creacion, estado, aprobado_por) VALUES
(1, 1, 50, '2025-06-01', 'Pendiente', 33333333-3), 
(2, 3, 30, '2025-06-03', 'Aprobado', 11111111-1), 
(3, 10, 5, '2025-06-05', 'Rechazado', 44444444-4);


-- Insert para tabla precios_anteriores
INSERT INTO precios_anteriores (id, pieza, precio, fecha_actualizacion) VALUES
(1, 1, 15000.00, '2025-01-01'),
(2, 2, 35000.00, '2025-02-01'),
(3, 3, 27000.00, '2025-03-01'),
(4, 4, 12000.00, '2025-04-01'),
(5, 5, 8000.00, '2025-05-01');
