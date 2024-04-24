DROP DATABASE IF EXISTS General;

CREATE DATABASE IF NOT EXISTS General;

USE General;

CREATE TABLE IF NOT EXISTS Modulos (
    idmodulo INT AUTO_INCREMENT PRIMARY KEY,
    nommodulo VARCHAR(100),
    nomprofesor VARCHAR(50),
    curso INT,
    creditos INT
);

INSERT INTO Modulos (nommodulo, nomprofesor, curso, creditos) VALUES
('Sistemas informáticos', 'Elena M.', 1, 10),
('Bases de datos', 'Carlos R.', 1, 10);

('Entornos de desarrollo', 'Laura G.', 1, 10),
('Lenguaje de marcas y sistemas de gestión de información', 'Roberto M.', 1, 10),
('Programación', 'Ana S.', 1, 10),
('Formación y orientación laboral', 'David P.', 1, 10);