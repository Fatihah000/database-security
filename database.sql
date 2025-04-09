-- Création de la table des rôles
CREATE TABLE IF NOT EXISTS role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Insertion des rôles de base
INSERT INTO role (name) VALUES ('Secrétaire');
INSERT INTO role (name) VALUES ('Enseignant');
INSERT INTO role (name) VALUES ('Élève');

-- Création de la table des utilisateurs
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

-- Insertion de quelques utilisateurs pour les tests
-- Utilisateur Secrétaire
INSERT INTO user (username, password, role_id) VALUES ('secretaire1', 'password_secretaire', 1);
-- Utilisateurs Enseignants
INSERT INTO user (username, password, role_id) VALUES ('prof1', 'password_prof', 2);
INSERT INTO user (username, password, role_id) VALUES ('prof2', 'password_prof2', 2);
-- Utilisateurs Élèves
INSERT INTO user (username, password, role_id) VALUES ('eleve1', 'password_eleve1', 3);
INSERT INTO user (username, password, role_id) VALUES ('eleve2', 'password_eleve2', 3);
INSERT INTO user (username, password, role_id) VALUES ('eleve3', 'password_eleve3', 3);

-- Création de la table des cours
CREATE TABLE IF NOT EXISTS course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description VARCHAR(500) NOT NULL,
    hours INT NOT NULL,
    course_type VARCHAR(50) NOT NULL
);

-- Insertion de quelques cours pour les tests
INSERT INTO course (title, description, hours, course_type) 
VALUES 
('Introduction à la Programmation', 'Cours d\'introduction à la programmation en Python.', 30, 'CM'),
('Bases de données', 'Apprendre les concepts fondamentaux des bases de données.', 20, 'TD'),
('Systèmes d\'information', 'Cours sur la gestion des systèmes d\'information dans les entreprises.', 40, 'TP');

-- Création de la table des inscriptions
CREATE TABLE IF NOT EXISTS enrollment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    date_enrolled DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (course_id) REFERENCES course(id)
);

-- Insertion de quelques inscriptions pour les tests
-- Élèves inscrits aux cours
INSERT INTO enrollment (user_id, course_id) VALUES (4, 1); -- eleve1 inscrit à 'Introduction à la Programmation'
INSERT INTO enrollment (user_id, course_id) VALUES (4, 2); -- eleve1 inscrit à 'Bases de données'
INSERT INTO enrollment (user_id, course_id) VALUES (5, 1); -- eleve2 inscrit à 'Introduction à la Programmation'
INSERT INTO enrollment (user_id, course_id) VALUES (6, 3); -- eleve3 inscrit à 'Systèmes d\'information'

-- Création de la table des notes
CREATE TABLE IF NOT EXISTS grade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    grade FLOAT NOT NULL,
    exam_type VARCHAR(50) NOT NULL,
    description VARCHAR(500),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (course_id) REFERENCES course(id)
);

-- Insertion de quelques notes pour les tests
-- Notes des étudiants dans les différents cours
INSERT INTO grade (user_id, course_id, grade, exam_type, description) 
VALUES (4, 1, 15.5, 'Examen final', 'Bonne performance générale');
INSERT INTO grade (user_id, course_id, grade, exam_type, description) 
VALUES (4, 2, 13.0, 'Examen final', 'Doit améliorer la gestion des requêtes SQL');
INSERT INTO grade (user_id, course_id, grade, exam_type, description) 
VALUES (5, 1, 18.0, 'Examen partiel', 'Excellente maîtrise du langage Python');
INSERT INTO grade (user_id, course_id, grade, exam_type, description) 
VALUES (6, 3, 12.0, 'Examen final', 'Doit approfondir les concepts théoriques');
