-- Création de la base de données
CREATE DATABASE IF NOT EXISTS skin_cancer_db;
USE skin_cancer_db;

-- Table pour l'authentification des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- Table pour l'historique des analyses des patients
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    result VARCHAR(20),
    probability FLOAT,
    image_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertion de l'utilisateur administrateur par défaut
INSERT INTO users (username, password) 
SELECT 'admin', '1234' 
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');