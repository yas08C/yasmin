CREATE DATABASE casasmart;
USE casasmart;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

CREATE TABLE comodo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

CREATE TABLE sensor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    id_comodo INT NOT NULL,
    FOREIGN KEY (id_comodo) REFERENCES comodo(id)
);

CREATE TABLE atuador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    estado VARCHAR(10) NOT NULL,
    id_comodo INT NOT NULL,
    FOREIGN KEY (id_comodo) REFERENCES comodo(id)
);

CREATE TABLE leitura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(5,1) NOT NULL,
    data_hora DATETIME NOT NULL,
    id_sensor INT NOT NULL,
    FOREIGN KEY (id_sensor) REFERENCES sensor(id)
);


INSERT INTO usuario (nome, email, senha_hash)
VALUES ('Aluno Exemplo', 'aluno@exemplo.com', 'hash_da_senha');

INSERT INTO comodo (nome, id_usuario) VALUES ('Sala', 1);
INSERT INTO comodo (nome, id_usuario) VALUES ('Quarto', 1);

INSERT INTO sensor (nome, tipo, id_comodo) VALUES ('Sensor de temperatura da sala', 'temperatura', 1);
INSERT INTO sensor (nome, tipo, id_comodo) VALUES ('Sensor de presenca da sala', 'presenca', 1);
INSERT INTO sensor (nome, tipo, id_comodo) VALUES ('Sensor de temperatura do quarto', 'temperatura', 2);

INSERT INTO atuador (nome, tipo, estado, id_comodo) VALUES ('Ar-condicionado da sala', 'ar_condicionado', 'desligado', 1);
INSERT INTO atuador (nome, tipo, estado, id_comodo) VALUES ('Lampada da sala', 'lampada', 'desligado', 1);
INSERT INTO atuador (nome, tipo, estado, id_comodo) VALUES ('Ar-condicionado do quarto', 'ar_condicionado', 'desligado', 2);
INSERT INTO atuador (nome, tipo, estado, id_comodo) VALUES ('Lampada do quarto', 'lampada', 'desligado', 2);

INSERT INTO leitura (valor, data_hora, id_sensor) VALUES (29.5, '2026-10-15 14:00:00', 1);
INSERT INTO leitura (valor, data_hora, id_sensor) VALUES (26.0, '2026-10-15 14:30:00', 1);
INSERT INTO leitura (valor, data_hora, id_sensor) VALUES (24.5, '2026-10-15 14:30:00', 3);
INSERT INTO leitura (valor, data_hora, id_sensor) VALUES (31.0, '2026-10-15 15:00:00', 1);


SELECT * FROM usuario;
SELECT * FROM comodo;
SELECT * FROM sensor;
SELECT * FROM atuador;
SELECT * FROM leitura;

SELECT * FROM atuador WHERE tipo = 'lampada';

SELECT * FROM atuador WHERE estado = 'ligado';

SELECT * FROM leitura WHERE valor > 28;

SELECT * FROM leitura ORDER BY data_hora DESC;

SELECT COUNT(*) FROM leitura;

SELECT atuador.nome, comodo.nome
FROM atuador
JOIN comodo ON atuador.id_comodo = comodo.id;


UPDATE atuador SET estado = 'ligado' WHERE id = 1;

UPDATE atuador SET estado = 'desligado' WHERE id = 1;

UPDATE atuador SET estado = 'ligado' WHERE id = 2;

UPDATE comodo SET nome = 'Sala de estar' WHERE id = 1;

UPDATE usuario SET email = 'novo.email@exemplo.com' WHERE id = 1;

SELECT * FROM atuador;
SELECT * FROM comodo;
SELECT * FROM usuario;


DELETE FROM leitura WHERE id = 4;

DELETE FROM atuador WHERE id = 4;

SELECT * FROM leitura;
SELECT * FROM atuador;