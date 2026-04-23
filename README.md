# GLF - Plateforme Garage

## Présentation

Ce projet vise à créer une plateforme web pour un garage automobile, avec :

- Un site public pour les clients
- Un espace d’administration privé pour le gérant

## Fonctionnalités prévues (V1)

### Côté visiteur (site public)

- Page d’accueil : présentation du garage, zone géographique, points forts, services principaux, accès rapide aux véhicules/pièces/reprise, bouton contact
- Liste des services proposés
- Consultation des véhicules d’occasion (listing + fiche détail)
- Consultation des pièces d’occasion (listing + fiche détail)
- Formulaire de contact
- Formulaire de demande de reprise de véhicule

### Côté admin (espace privé)

- Authentification (connexion sécurisée)
- Gestion des véhicules d’occasion : ajouter, modifier, supprimer/masquer, publier/dépublier, marquer comme vendu, gestion des photos (ajout, ordre, image principale)
- Gestion des pièces d’occasion : ajouter, modifier, supprimer, publier/dépublier, gestion des photos
- Gestion des services affichés sur le site
- Lecture des demandes de contact et de reprise
- Tableau de bord synthétique (nombre de véhicules/pièces publiés, demandes récentes)

## Stack technique

- Backend : Python (FastAPI)
- Base de données : (à préciser, probablement PostgreSQL ou SQLite)
- ORM : SQLAlchemy
- Validation : Pydantic
- Authentification : JWT (JSON Web Token)
- Gestion des fichiers : Stockage local (uploads/)
- Tests : (à compléter, Pytest recommandé)
- Frontend : (à développer, non inclus dans ce dépôt pour l’instant)

## Structure du projet

```
app/
  auth.py
  enums.py
  main.py
  core/
    config.py
    database.py
    security.py
  deps/
    auth.py
  models/
    contact_request.py
    part.py
    service.py
    trade_in_request.py
    user.py
    vehicle.py
  routes/
    admin_messages.py
    admin_parts.py
    admin_services.py
    admin_vehicles.py
    auth.py
    public_contact.py
    public_parts.py
    public_services.py
    public_trade_in.py
    public_vehicles.py
  schemas/
    auth.py
    contact_request.py
    image.py
    part.py
    service.py
    trade_in_request.py
    vehicle.py
  services/
    email_service.py
    file_storage.py
    image_service.py
  uploads/
    parts/
    vehicles/
  utils/
    auth.py
    image.py
    part.py
    vehicle.py
tests/
requirements.txt
VERSION
TODO.txt
```

## Ce qui est déjà codé

- Structure backend en Python (probablement FastAPI)
- Modèles pour : véhicules, pièces, services, utilisateurs, demandes de contact, demandes de reprise
- Routes pour : gestion admin/public des véhicules, pièces, services, messages, authentification
- Services pour : gestion des emails, stockage de fichiers/images
- Système d’authentification (admin)
- Gestion des uploads (photos véhicules/pièces)
- Schémas de validation (Pydantic)
- Fichiers de configuration, sécurité, base de données

## Ce qu’il reste à faire

- Finaliser les pages frontend (site public + admin)
- Intégrer les formulaires (contact, reprise)
- Améliorer l’UI/UX (navigation, affichage, responsive)
- Ajouter les tests automatisés
- Rédiger la documentation utilisateur/admin
- Déployer en production

## Installation détaillée

### Prérequis

- Python 3.9 ou supérieur
- (Optionnel) PostgreSQL ou SQLite installé pour la base de données
- (Optionnel) Outil de gestion d’environnement virtuel (venv, virtualenv, poetry...)

### Étapes d’installation

1. Cloner le dépôt

```bash
git clone <url-du-repo>
cd GLF
```

2. Créer et activer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Installer les dépendances

```bash
pip install -r requirements.txt
```

4. Configurer la base de données

- Modifier les variables d’environnement ou le fichier config.py selon votre configuration (URL de la base, clés secrètes, etc.)
- Créer la base de données si besoin
- Lancer les migrations (si applicable)
  (À compléter selon l’outil utilisé, ex : Alembic)

5. Démarrer le serveur

```bash
uvicorn app.main:app --reload
```

6. Accéder à l’API

- Documentation interactive : http://localhost:8000/docs
- API root : http://localhost:8000

## TODO

Voir le fichier `TODO.txt` pour la liste détaillée des tâches à venir.
