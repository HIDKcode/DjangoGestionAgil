USE inventario;
-- Insert para tabla usuarios
INSERT INTO usuarios (rut, password, rol, intentos_fallidos, bloqueado, is_active, is_staff, is_superuser) VALUES
('11111111-1', 'admin', 'admin', 0, 0, 1, 0, 1),
('22222222-2', 'inventario', 'inventario', 0, 0, 1, 0, 0),
('33333333-3', 'comprador', 'comprador', 0, 0, 1, 0, 0),
('44444444-4', 'logistica', 'logistica', 0, 0, 1, 0, 0),
('55555555-5', 'produccion', 'produccion', 0, 0, 1, 0, 0),
('66666666-6', 'auditor', 'auditor', 0, 0, 1, 1, 0), --  cuenta bloqueda para prboar
('77777777-7', 'gerente', 'gerente', 0, 0, 1, 0, 0),
('88888888-8', 'planta', 'planta', 0, 0, 1, 0, 0);

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
