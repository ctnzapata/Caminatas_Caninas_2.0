
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS caminatas_comunitarias;
USE caminatas_comunitarias;

-- 1. Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    contrasenia VARCHAR(255),
    rol ENUM('voluntario', 'admin') DEFAULT 'voluntario',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de perfiles de voluntarios
CREATE TABLE perfiles_voluntarios (
    id INT PRIMARY KEY,
    telefono VARCHAR(20),
    direccion TEXT,
    experiencia TEXT,
    FOREIGN KEY (id) REFERENCES usuarios(id)
);

-- 3. Tabla de refugios
CREATE TABLE refugios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    direccion TEXT,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- 4. Tabla de perros
CREATE TABLE perros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    edad INT,
    raza VARCHAR(100),
    tamanio ENUM('pequeño', 'mediano', 'grande'),
    energia ENUM('baja', 'media', 'alta'),
    descripcion TEXT,
    estado ENUM('disponible', 'adoptado', 'en paseo') DEFAULT 'disponible',
    refugio_id INT,
    FOREIGN KEY (refugio_id) REFERENCES refugios(id)
);

-- 5. Tabla de rutas disponibles
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    distancia_km DECIMAL(5,2),
    dificultad ENUM('fácil', 'moderada', 'difícil'),
    descripcion TEXT,
    puntos_referencia TEXT,
    tiempo_estimado_min INT
);

-- 6. Tabla de horarios disponibles
CREATE TABLE horarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dia_semana ENUM('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'),
    hora_inicio TIME,
    hora_fin TIME,
    max_voluntarios INT
);

-- 7. Tabla de caminatas programadas
CREATE TABLE caminatas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    horario_id INT,
    ruta_id INT,
    estado ENUM('pendiente', 'en_progreso', 'completada', 'cancelada') DEFAULT 'pendiente',
    FOREIGN KEY (horario_id) REFERENCES horarios(id),
    FOREIGN KEY (ruta_id) REFERENCES rutas(id)
);

-- 8. Tabla de registro de caminatas (relación muchos a muchos entre usuarios y caminatas)
CREATE TABLE registro_caminatas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    caminata_id INT,
    perro_id INT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asistencia BOOLEAN DEFAULT FALSE,
    comentarios TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (caminata_id) REFERENCES caminatas(id),
    FOREIGN KEY (perro_id) REFERENCES perros(id)
);

-- 9. Tabla de preferencias de perros por usuario
CREATE TABLE preferencias_perros (
    usuario_id INT,
    perro_id INT,
    preferencia INT, -- 1 a 5, siendo 5 la mayor preferencia
    PRIMARY KEY (usuario_id, perro_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (perro_id) REFERENCES perros(id)
);

-- 10. Tabla de preferencias de rutas por usuario
CREATE TABLE preferencias_rutas (
    usuario_id INT,
    ruta_id INT,
    preferencia INT, -- 1 a 5, siendo 5 la mayor preferencia
    PRIMARY KEY (usuario_id, ruta_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (ruta_id) REFERENCES rutas(id)
);

-- 11. Tabla de historial de caminatas
CREATE TABLE historial_caminatas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_caminata_id INT,
    duracion_real_min INT,
    distancia_real_km DECIMAL(5,2),
    comportamiento_perro ENUM('excelente', 'bueno', 'regular', 'malo'),
    observaciones TEXT,
    FOREIGN KEY (registro_caminata_id) REFERENCES registro_caminatas(id)
);

-- 12. Tabla de requisitos para pasear perros
CREATE TABLE requisitos_perros (
    perro_id INT,
    requisito VARCHAR(255),
    PRIMARY KEY (perro_id, requisito),
    FOREIGN KEY (perro_id) REFERENCES perros(id)
);

-- 13. Tabla de equipamiento para caminatas
CREATE TABLE equipamiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    cantidad_disponible INT
);

-- 14. Tabla de préstamo de equipamiento
CREATE TABLE prestamo_equipamiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_caminata_id INT,
    equipamiento_id INT,
    cantidad INT,
    devuelto BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (registro_caminata_id) REFERENCES registro_caminatas(id),
    FOREIGN KEY (equipamiento_id) REFERENCES equipamiento(id)
);

--Poblar tablas con datos de prueba:
USE caminatas_comunitarias;

-- 1. Usuarios
INSERT INTO usuarios (nombre, correo, contrasenia, rol) VALUES
('Laura Gómez', 'laura@example.com', 'pass123', 'voluntario'),
('Carlos Pérez', 'carlos@example.com', 'pass456', 'voluntario'),
('Ana Torres', 'ana@example.com', 'pass789', 'voluntario'),
('Admin User', 'admin@example.com', 'adminpass', 'admin');

-- 2. Perfiles de Voluntarios
INSERT INTO perfiles_voluntarios (id, telefono, direccion, experiencia) VALUES
(1, '3001234567', 'Calle 123', 'Ama los animales'),
(2, '3009876543', 'Carrera 45', 'Ha paseado perros antes'),
(3, '3011122233', 'Diagonal 78', 'Tiene experiencia en adiestramiento');

-- 3. Refugios
INSERT INTO refugios (nombre, direccion, telefono, correo) VALUES
('Refugio Huellitas', 'Cra 10 #45-78', '3104567890', 'huellitas@refugio.com'),
('Amigos Peludos', 'Cl 67 #12-34', '3111234567', 'amigospeludos@refugio.com');

-- 4. Perros
INSERT INTO perros (nombre, edad, raza, tamanio, energia, descripcion, estado, refugio_id) VALUES
('Max', 3, 'Labrador', 'grande', 'alta', 'Juguetón y amigable', 'disponible', 1),
('Luna', 2, 'Beagle', 'mediano', 'media', 'Cariñosa y activa', 'disponible', 1),
('Rocky', 5, 'Pastor Alemán', 'grande', 'alta', 'Leal y protector', 'disponible', 2),
('Mila', 1, 'Poodle', 'pequeño', 'baja', 'Tranquila y obediente', 'disponible', 2);

-- 5. Rutas
INSERT INTO rutas (nombre, distancia_km, dificultad, descripcion, puntos_referencia, tiempo_estimado_min) VALUES
('Ruta Parque Central', 2.5, 'fácil', 'Recorrido por el parque del barrio', 'Cancha, Lago, Zona infantil', 30),
('Sendero Montaña', 5.0, 'difícil', 'Subida por senderos naturales', 'Mirador, Cascada', 90),
('Paseo Urbano', 3.2, 'moderada', 'Calles y avenidas del centro', 'Iglesia, Plazoleta, Cafés', 45),
('Vuelta al lago', 4.1, 'moderada', 'Camino alrededor del lago municipal', 'Bosque, Mirador, Lago', 60);

-- 6. Horarios
INSERT INTO horarios (dia_semana, hora_inicio, hora_fin, max_voluntarios) VALUES
('Sábado', '09:00:00', '10:00:00', 5),
('Domingo', '08:30:00', '10:00:00', 4),
('Miércoles', '17:00:00', '18:00:00', 3),
('Viernes', '16:00:00', '17:30:00', 6);

-- 7. Caminatas
INSERT INTO caminatas (fecha, horario_id, ruta_id, estado) VALUES
('2025-04-21', 1, 1, 'pendiente'),
('2025-04-22', 2, 2, 'pendiente'),
('2025-04-23', 3, 3, 'pendiente'),
('2025-04-24', 4, 4, 'pendiente');

-- 8. Registro de Caminatas
INSERT INTO registro_caminatas (usuario_id, caminata_id, perro_id, asistencia, comentarios) VALUES
(1, 1, 1, TRUE, 'Todo bien'),
(2, 2, 2, TRUE, 'Muy animado el perro'),
(3, 3, 3, FALSE, 'No pudo asistir'),
(1, 4, 4, TRUE, 'Excelente experiencia');

-- 9. Preferencias de perros
INSERT INTO preferencias_perros (usuario_id, perro_id, preferencia) VALUES
(1, 1, 5),
(1, 2, 4),
(2, 3, 5),
(3, 4, 3);

-- 10. Preferencias de rutas
INSERT INTO preferencias_rutas (usuario_id, ruta_id, preferencia) VALUES
(1, 1, 4),
(2, 2, 5),
(3, 3, 3),
(1, 4, 2);

-- 11. Historial de caminatas
INSERT INTO historial_caminatas (registro_caminata_id, duracion_real_min, distancia_real_km, comportamiento_perro, observaciones) VALUES
(1, 35, 2.4, 'excelente', 'Muy tranquilo'),
(2, 90, 5.1, 'bueno', 'Se emocionó con otros perros'),
(4, 55, 4.0, 'excelente', 'Muy obediente'),
(3, 0, 0.0, 'regular', 'No asistió');

-- 12. Requisitos para pasear perros
INSERT INTO requisitos_perros (perro_id, requisito) VALUES
(1, 'Debe tener correa'),
(1, 'Debe ir con bozal'),
(2, 'Llevar agua'),
(3, 'Evitar ruidos fuertes');

-- 13. Equipamiento
INSERT INTO equipamiento (nombre, descripcion, cantidad_disponible) VALUES
('Correa', 'Correa estándar de nylon', 10),
('Bozal', 'Bozal talla grande', 5),
('Botella de agua', 'Botella plástica reutilizable', 15),
('Dispensador de bolsas', 'Para recoger excrementos', 12);

-- 14. Préstamo de equipamiento
INSERT INTO prestamo_equipamiento (registro_caminata_id, equipamiento_id, cantidad, devuelto) VALUES
(1, 1, 1, TRUE),
(2, 2, 1, FALSE),
(3, 3, 1, FALSE),
(4, 4, 1, TRUE);