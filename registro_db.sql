CREATE DATABASE IF NOT EXISTS Registros_Peaje;

USE Registros_Peaje;

CREATE TABLE IF NOT EXISTS Registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_TAG VARCHAR(100),
    concesion INT,
    tipo_TAG INT,
    IUT VARCHAR(100),
    categoria INT,
    categoria_cobrada INT,
    categoria_detectada INT,
    status INT,
    hora_peaje TIME,
    fecha_peaje DATE,
    importe_peaje INT,
    numero_reenvio INT,
    entrada INT,
    salida INT,
    sentido INT
    );
    
