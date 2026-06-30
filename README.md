# GLF Auto — Backend

API backend pour [GLF Auto](https://glf-auto.vercel.app/), plateforme web développée pour un garage automobile permettant la gestion et la mise en vente de véhicules et pièces d'occasion. Le projet est **déployé en production** et utilisé par un client réel (petit garage automobile).

## Présentation

GLF Auto centralise la gestion d'un garage automobile à travers deux interfaces :

- un **site public** où les clients consultent les véhicules et pièces disponibles, les services proposés, et peuvent faire une demande de contact ou de reprise de véhicule
- un **espace d'administration** où le gérant gère l'ensemble du catalogue (véhicules, pièces, services), les photos associées, et les demandes entrantes

Le client est un petit garage indépendant : le volume de trafic et de demandes reste donc modeste, mais l'application est pleinement fonctionnelle et utilisée en conditions réelles.

## Fonctionnalités

### Côté public

- Présentation du garage et de ses services
- Catalogue de véhicules d'occasion (listing + fiche détaillée)
- Catalogue de pièces d'occasion (listing + fiche détaillée)
- Formulaire de contact
- Formulaire de demande de reprise de véhicule

### Côté administration

- Authentification sécurisée (JWT)
- Gestion complète des véhicules : création, modification, suppression, publication/dépublication, statut vendu, gestion des photos (ajout, ordre, image principale)
- Gestion complète des pièces : création, modification, suppression, publication, photos
- Gestion des services affichés sur le site
- Consultation des demandes de contact et de reprise
- Tableau de bord synthétique (nombre de véhicules/pièces publiés, demandes récentes)

## Stack technique

- **Langage** : Python 3.11+
- **Framework** : FastAPI
- **Base de données** : PostgreSQL, hébergée sur Supabase
- **ORM** : SQLAlchemy / SQLModel
- **Migrations** : Alembic
- **Validation des données** : Pydantic
- **Authentification** : JWT (python-jose, passlib, bcrypt pour le hashage des mots de passe)
- **Stockage de fichiers** : Supabase Storage (photos véhicules/pièces)
- **Emails** : Resend (notifications de contact/reprise)
- **Limitation de débit (rate limiting)** : SlowAPI
- **Tests** : Pytest (présent dans le projet, à remettre à jour suite aux dernières évolutions)

## Architecture du projet

```
app/
  main.py              # Point d'entrée FastAPI
  auth.py              # Logique d'authentification
  enums.py
  core/
    config.py           # Configuration (variables d'environnement, etc.)
    database.py          # Connexion et session DB
    security.py          # Hashage, gestion des tokens JWT
  deps/
    auth.py              # Dépendances d'authentification (routes protégées)
  models/                # Modèles SQLAlchemy (véhicules, pièces, services, utilisateurs, demandes)
  routes/                # Endpoints API (admin et public, par ressource)
  schemas/                # Schémas Pydantic (validation entrée/sortie)
  services/                # Logique métier (emails, stockage de fichiers, traitement d'images)
  uploads/                  # Fichiers reçus (legacy / fallback local)
alembic/                  # Migrations de base de données
tests/                     # Tests unitaires et d'intégration (Pytest)
```

## Installation et lancement en local

### Prérequis

- Python 3.11+
- Une instance PostgreSQL accessible (ou un projet Supabase)

### Étapes

1. **Cloner le dépôt**

   ```bash
   git clone <url-du-repo>
   cd GLF-auto
   ```

2. **Créer et activer un environnement virtuel**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**

   Créer un fichier `.env` à la racine avec, a minima :

   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   SECRET_KEY=...
   RESEND_API_KEY=...
   ```

5. **Appliquer les migrations**

   ```bash
   alembic upgrade head
   ```

6. **Lancer le serveur**

   ```bash
   uvicorn app.main:app --reload
   ```

   L'API est disponible sur `http://localhost:8000`, avec une documentation interactive générée automatiquement sur `/docs`.

## Déploiement

Le projet est actuellement déployé en production, avec :

- backend hébergé sur Render
- frontend (Next.js) hébergé sur Vercel, voir le dépôt [GLF-auto-Frontend](https://github.com/sangoaz/GLF-auto-Frontend)
- base de données et stockage de fichiers gérés via Supabase
- frontend accessible sur [glf-auto.vercel.app](https://glf-auto.vercel.app/)

## Pistes d'évolution

- Compléter et automatiser la suite de tests (CI)
- Statistiques avancées pour le tableau de bord admin (coûts, historique des ventes)
- Export de données (CSV, PDF)
- Application mobile dédiée pour la gestion côté gérant

---

**Auteur** : Kévin Fruchon (sangoaz)
**Licence** : MIT
