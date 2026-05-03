# 🔬 DermAIgnosis — Détection du Cancer de la Peau par IA

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?logo=flask)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)
![MySQL](https://img.shields.io/badge/MySQL-8.x-blue?logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)

> **DermAIgnosis** est une application web d'aide au diagnostic médical qui utilise le deep learning pour détecter les lésions cutanées malignes à partir d'images dermoscopiques.

---

## 🚀 Fonctionnalités

- 🧠 **Diagnostic IA** — Modèle VGG16 entraîné sur des images de cancer de la peau
- 📊 **Tableau de bord** — Statistiques patients, cas malins vs bénins
- 🖼️ **Analyse d'image** — Upload d'image dermoscopique et prédiction instantanée
- 📋 **Recommandations thérapeutiques** — Recommandations personnalisées selon le résultat et l'âge
- 📈 **Suivi patient** — Évolution du volume de la lésion avec taux de croissance
- 🔐 **Authentification** — Connexion sécurisée par session pour le personnel médical
- 🖨️ **Export PDF** — Impression des rapports directement depuis le navigateur

---

## 🛠️ Technologies Utilisées

### Backend
| Technologie | Version | Role |
|-------------|---------|------|
| Python | 3.11 | Langage principal |
| Flask | 3.x | Framework web |
| TensorFlow / Keras | 2.x | Modèle deep learning (VGG16) |
| PyMySQL | latest | Connecteur base de données MySQL |
| NumPy | latest | Traitement des tableaux d'images |
| Pillow | latest | Chargement et traitement des images |

### Frontend
| Technologie | Version | Role |
|-------------|---------|------|
| HTML5 / CSS3 | — | Structure et style |
| Bootstrap | 5.3 | Framework UI responsive |
| Font Awesome | 6.x | Icones |
| Jinja2 | integre | Moteur de templates Flask |

### Base de données
| Technologie | Role |
|-------------|------|
| MySQL | Stockage des données patients |
| phpMyAdmin | Gestion de la base via XAMPP |

### Modele IA
| Detail | Info |
|--------|------|
| Architecture | VGG16 (Transfer Learning) |
| Taille d'entree | 224 x 224 px |
| Sortie | Classification binaire (Malin / Benin) |
| Format | .h5 (Keras) |

---

## 📁 Structure du Projet

```
DermAIgnosis/
│
├── README.md                   # Documentation
├── app.py                      # Application Flask principale
├── database.sql                # Schema et donnees MySQL
│
├── model/
│   └── vgg16_skin_cancer.h5    # Modele IA pre-entraine
│
├── static/
│   ├── style.css               # Styles personnalises
│   └── uploads/                # Images uploadees des patients
│
└── templates/
    ├── login.html              # Page de connexion
    ├── dashboard.html          # Tableau de bord
    ├── predict.html            # Analyse d'image
    ├── result.html             # Resultat du diagnostic
    ├── patients.html           # Liste des patients
    ├── followup.html           # Suivi patient
    ├── recommandation.html     # Recommandations therapeutiques
    └── consignes.html          # Guide d'utilisation
```

---

## ⚙️ Installation

### 1. Cloner le repository
git clone https://github.com/chaima-kidissi/DermAIgnosis.git
cd DermAIgnosis
### 2. Creer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate
### 3. Installer les dependances
pip install flask pymysql tensorflow numpy pillow
### 4. Configurer la base de données
- Demarrer XAMPP (Apache + MySQL)
- Ouvrir phpMyAdmin → creer la base skin_cancer_db
- Importer le fichier database.sql

### 5. Ajouter le modele IA
- Placer vgg16_skin_cancer.h5 dans le dossier model/

### 6. Lancer l'application
python app.py

Ouvrir le navigateur sur : http://127.0.0.1:5000

---

## 🗄️ Schema de la Base de Donnees
```
CREATE TABLE users (
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(100),
password VARCHAR(100)
);
CREATE TABLE patients (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
age INT,
result VARCHAR(20),
probability FLOAT,
image_path VARCHAR(255),
date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
---

## 🧠 Details du Modele IA

- Architecture : VGG16 avec Transfer Learning
- Entree : Image RGB 224x224 pixels
- Sortie : Score de probabilite (0 a 1)
  - superieur a 0.5 → Malin
  - inferieur ou egal a 0.5 → Benin
- Fonction de perte : Binary Cross-Entropy
- Optimiseur : Adam

---

## ⚠️ Modèle IA

Le fichier `vgg16_skin_cancer.h5` n'est pas inclus dans ce repo car il dépasse la limite GitHub (100MB).

Pour l'obtenir :
- Contacte l'auteure : chaima-kidissi

## ⚠️ Avertissement

Cette application est un outil d'aide à la décision clinique uniquement.

Toutes les recommandations générées par l'IA doivent être validées par un professionnel de santé qualifié.

L'application DermAIgnosis ne remplace pas le diagnostic d'un dermatologue.

---

## 🎥 Démonstration

![DermAIgnosis Demo](DermAIgnosis.mp4)

## 👩‍💻 Auteure

Chaima Kidissi
- GitHub : https://github.com/chaima-kidissi

---

## 📄 Licence

No Licence
