# 🎓 Application de Gestion Académique Sécurisée – Flask & MySQL

Bienvenue dans ce projet web réalisé dans le cadre d’un travail pratique sur la **sécurité des bases de données**. Il s'agit d'une **application Flask** permettant de gérer les cours universitaires, les utilisateurs (étudiants, enseignants, personnel administratif), les inscriptions, les notes, et bien plus encore — le tout avec un accent fort sur la **sécurité et la performance** des données.

---

## 🚀 Fonctionnalités principales

- Connexion / inscription sécurisées avec rôles
- Interface personnalisée pour chaque type d’utilisateur :
  - **Étudiants** : inscription aux cours, consultation des notes
  - **Enseignants** : gestion des séances et attribution des notes
  - **Secrétaires** : administration des cours, enseignants, et inscriptions
- Formulaires sécurisés (CSRF, méthode POST)
- Requêtes SQL protégées contre les injections
- Architecture orientée rôles avec contrôles d’accès précis
- Optimisation des requêtes et indexation pour de meilleures performances

---

## 🧱 Technologies utilisées

- **Flask** (framework backend Python)
- **MySQL** (base de données relationnelle)
- **HTML/CSS** (frontend simple et responsive)
- Optionnel : **SQLAlchemy** (non utilisé ici mais facilement intégrable)

---

## 📦 Installation et exécution

1. **Cloner le projet**
   ```bash
   git clone https://github.com/Fatihah000/database-security.git
   cd database-security
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Créer et remplir la base de données**
   - Exécute le fichier SQL fourni (`database.sql`) dans ton SGBD MySQL pour :
     - Créer la base de données
     - Générer les tables
     - Remplir les données de test

5. **Lancer l'application**
   ```bash
   python run.py
   ```

6. **Accéder à l'application**
   - Rendez-vous sur [http://localhost:5000](http://localhost:5000)

---

## 🛡️ Sécurité intégrée

Le projet implémente plusieurs **bonnes pratiques de cybersécurité** :

- **Requêtes préparées** : protection contre les injections SQL
- **Rôles utilisateur & autorisations** : accès limité selon le profil
- **Formulaires protégés** par tokens CSRF
- **Logs de requêtes** activés pour détection d’anomalies
- **Gestion centralisée des permissions** dans la base

---

## 🗃️ Structure de la base de données

Les tables principales :

- `utilisateurs` : identité, rôle, mot de passe (haché)
- `cours` : cours proposés
- `inscriptions` : relation étudiants-cours
- `notes` : résultats des étudiants
- Autres : `séances`, `exercices`, `questions`

La base est **normalisée**, **indexée**, et pensée pour **l’évolutivité**.

---

## 📈 Optimisations

- Index sur les colonnes critiques
- Requêtes optimisées et profilées
- Résultats mis en cache côté serveur pour améliorer les performances

---

## 📍 À propos du projet

Ce projet a été conçu pour illustrer comment une **architecture sécurisée** et **efficace** peut être mise en place dans un système multi-utilisateur de gestion académique. Il montre l’importance d’une conception rigoureuse, tant sur le plan **fonctionnel** que **sécuritaire**.

---

## ✅ À venir / pistes d’amélioration

- Intégration de SQLAlchemy pour un ORM plus souple
- Refonte frontend avec un framework JS (React, Vue…)
- Tests unitaires / automatisés
- Déploiement sur un serveur distant (Heroku, Render, etc.)

---

## 📄 Auteur

Projet réalisé par **DERMANE Fatihah**  
Dans le cadre du TP de **Sécurité des Bases de Données**
