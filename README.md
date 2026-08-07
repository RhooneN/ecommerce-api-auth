
# 🔐 Auth Service - SHIDO

<div align="center">

![SHIDO](https://img.shields.io/badge/SHIDO-Auth%20Service-6366f1?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14-red?logo=django)](https://django-rest-framework.org)
[![Health](https://img.shields.io/badge/health-online-brightgreen)]()
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0.3-6ba539?logo=openapiinitiative)]()

**Gestion centralisée de l'authentification et des profils utilisateurs**

[📖 Endpoints](#-api-endpoints) · [🚀 Quick Start](#-quick-start) · [🔧 Config](#-configuration) · [📊 Monitoring](#-monitoring)

</div>

---

## 📖 Aperçu

Le **Auth Service** est le point d'entrée unique pour l'authentification dans l'écosystème SHIDO. Il gère l'enregistrement, la connexion et la validation des tokens JWT pour tous les autres microservices.

### 🎯 Responsabilités

- ✅ Enregistrement utilisateurs (`/register/`)
- ✅ Authentification JWT (`/login/`)
- ✅ Validation de tokens inter-services
- ✅ Gestion des permissions et rôles

### 🏗️ Architecture

```mermaid
graph LR
    A[Client Mobile/Web] --> B[API Gateway]
    B --> C[Auth Service :8001]
    C --> D[(PostgreSQL)]
    C --> E[Redis Cache]
    F[Product Service] -.->|JWT Validation| C
    G[Cart Service] -.->|JWT Validation| C
    H[Order Service] -.->|JWT Validation| C
    
    ###🚀 Quick Start
    ## 1. Cloner le repository
git clone https://github.com/SHIDO/auth-service.git
cd auth-service

## 2. Copier les variables d'environnement
cp .env.example .env
## → Éditer .env avec vos valeurs

## 3. Lancer avec Make
make setup
### ✅ Installe les dépendances Python
### ✅ Lance les migrations Django
### ✅ Crée un superuser admin
### ✅ Seed la base de données

### 4. Démarrer le serveur
make run
### → http://localhost:8001

## 5. Vérifier la santé
curl http://localhost:8001/health/
### → {"status": "healthy", "database": "connected", "timestamp": "2026-06-09T10:00:00Z"}

##📡 API Endpoints
Méthode	Endpoint	Description	Auth	Corps Requête
POST	/register/	Créer un compte	❌	{email, password, name}
POST	/login/	Obtenir token JWT	❌	{email, password}
GET	/health/	Health check	❌	-
##📖 Documentation Interactive
Interface	URL
Swagger UI (interactive)	http://localhost:8001/api/schema/swagger-ui/
ReDoc (élégante)	http://localhost:8001/api/schema/redoc/
Spécification OpenAPI (JSON)	http://localhost:8001/api/schema/

##Exemples d'utilisation
# S'enregistrer
curl -X POST http://localhost:8001/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@shido.com",
    "password": "SecurePass123!",
    "name": "Jean Dupont"
  }'

# Réponse
{
  "id": 1,
  "email": "client@shido.com",
  "name": "Jean Dupont",
  "created_at": "2026-06-09T10:00:00Z"
}

# Se connecter
curl -X POST http://localhost:8001/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "client@shido.com", "password": "SecurePass123!"}'

# Réponse
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "email": "client@shido.com",
    "name": "Jean Dupont"
  }
}

##🔧 Configuration
#Variables d'environnement
# .env
# === Base de données ===
DB_NAME=shido_auth
DB_USER=admin
DB_PASSWORD=change_me_in_production
DB_HOST=localhost
DB_PORT=5432

# === JWT ===
JWT_SECRET_KEY=votre_secret_tres_long_et_aleatoire
JWT_ACCESS_TOKEN_LIFETIME=3600      # 1 heure
JWT_REFRESH_TOKEN_LIFETIME=604800   # 7 jours

# === Sécurité ===
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000

# === Rate Limiting ===
LOGIN_RATE_LIMIT=5/minute           # Max 5 tentatives/minute
REGISTER_RATE_LIMIT=3/minute        # Max 3 inscriptions/minute

# === Email (optionnel) ===
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.votre_cle_api

Parfait ! Voici les READMEs complets pour chaque service de SHIDO. Je les ai générés en format polyrepo (un README par service), prêts à être déposés dans chaque repository.
📦 1. Service Authentification (auth-service)
markdown

# 🔐 Auth Service - SHIDO

<div align="center">

![SHIDO](https://img.shields.io/badge/SHIDO-Auth%20Service-6366f1?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14-red?logo=django)](https://django-rest-framework.org)
[![Health](https://img.shields.io/badge/health-online-brightgreen)]()
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0.3-6ba539?logo=openapiinitiative)]()

**Gestion centralisée de l'authentification et des profils utilisateurs**

[📖 Endpoints](#-api-endpoints) · [🚀 Quick Start](#-quick-start) · [🔧 Config](#-configuration) · [📊 Monitoring](#-monitoring)

</div>

---

## 📖 Aperçu

Le **Auth Service** est le point d'entrée unique pour l'authentification dans l'écosystème SHIDO. Il gère l'enregistrement, la connexion et la validation des tokens JWT pour tous les autres microservices.

### 🎯 Responsabilités

- ✅ Enregistrement utilisateurs (`/register/`)
- ✅ Authentification JWT (`/login/`)
- ✅ Validation de tokens inter-services
- ✅ Gestion des permissions et rôles

### 🏗️ Architecture

```mermaid
graph LR
    A[Client Mobile/Web] --> B[API Gateway]
    B --> C[Auth Service :8001]
    C --> D[(PostgreSQL)]
    C --> E[Redis Cache]
    F[Product Service] -.->|JWT Validation| C
    G[Cart Service] -.->|JWT Validation| C
    H[Order Service] -.->|JWT Validation| C

🚀 Quick Start
bash

# 1. Cloner le repository
git clone https://github.com/SHIDO/auth-service.git
cd auth-service

# 2. Copier les variables d'environnement
cp .env.example .env
# → Éditer .env avec vos valeurs

# 3. Lancer avec Make
make setup
# ✅ Installe les dépendances Python
# ✅ Lance les migrations Django
# ✅ Crée un superuser admin
# ✅ Seed la base de données

# 4. Démarrer le serveur
make run
# → http://localhost:8001

# 5. Vérifier la santé
curl http://localhost:8001/health/
# → {"status": "healthy", "database": "connected", "timestamp": "2026-06-09T10:00:00Z"}

📡 API Endpoints
Méthode	Endpoint	Description	Auth	Corps Requête
POST	/register/	Créer un compte	❌	{email, password, name}
POST	/login/	Obtenir token JWT	❌	{email, password}
GET	/health/	Health check	❌	-
📖 Documentation Interactive
Interface	URL
Swagger UI (interactive)	http://localhost:8001/api/schema/swagger-ui/
ReDoc (élégante)	http://localhost:8001/api/schema/redoc/
Spécification OpenAPI (JSON)	http://localhost:8001/api/schema/
Exemples d'utilisation
bash

## S'enregistrer
curl -X POST http://localhost:8001/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@shido.com",
    "password": "SecurePass123!",
    "name": "Jean Dupont"
  }'

## Réponse
{
  "id": 1,
  "email": "client@shido.com",
  "name": "Jean Dupont",
  "created_at": "2026-06-09T10:00:00Z"
}

## Se connecter
curl -X POST http://localhost:8001/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "client@shido.com", "password": "SecurePass123!"}'

## Réponse
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "email": "client@shido.com",
    "name": "Jean Dupont"
  }
}

🔧 Configuration
Variables d'environnement
bash

### .env
### === Base de données ===
DB_NAME=shido_auth
DB_USER=admin
DB_PASSWORD=change_me_in_production
DB_HOST=localhost
DB_PORT=5432

### === JWT ===
JWT_SECRET_KEY=votre_secret_tres_long_et_aleatoire
JWT_ACCESS_TOKEN_LIFETIME=3600      # 1 heure
JWT_REFRESH_TOKEN_LIFETIME=604800   # 7 jours

### === Sécurité ===
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000

### === Rate Limiting ===
LOGIN_RATE_LIMIT=5/minute           # Max 5 tentatives/minute
REGISTER_RATE_LIMIT=3/minute        # Max 3 inscriptions/minute

### === Email (optionnel) ===
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.votre_cle_api

###📊 Monitoring
###Health Check
curl http://localhost:8001/health/
### {
####   "status": "healthy",
####   "database": "connected",
####   "redis": "connected",
####   "uptime": "48h 23m",
####   "version": "1.0.0"
#### }

###Métriques Prometheus
Endpoint: :9090/metrics
- http_requests_total
- login_attempts_total
- registration_total
- active_users_gauge
- jwt_token_validations_total

##Alertes Grafana

    🔴 auth_service_down : Service inaccessible > 30s

    🟡 login_rate_high : > 100 tentatives/minute

    🟠 registration_spike : > 50 inscriptions/minute

##🐛 Debugging
#### Voir les logs en direct
docker logs -f shido-auth-service

#### Accéder au shell Django
docker exec -it shido-auth python manage.py shell

#### Lister les utilisateurs
docker exec -it shido-auth python manage.py list_users

#### Vérifier un token
curl -X POST http://localhost:8001/api/token/verify/ \
  -d '{"token": "eyJhbGciOi..."}'

####	  Mode debug
export DEBUG=True

🔗 Dépendances
Service	Relation
Aucun	Service indépendant
Tous les autres services	← Valident les tokens JWT émis par Auth

##📁 Structure du Projet
auth-service/
├── auth_app/
│   ├── models.py          # Modèle User personnalisé
│   ├── serializers.py     # Register/Login serializers
│   ├── views.py           # UserCreateView, LoginView
│   ├── urls.py            # Routage endpoints
│   └── tests/
├── config/
│   ├── settings.py        # Configuration Django
│   ├── urls.py            # Routes principales
│   └── wsgi.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── openapi.yaml       # Spécification OpenAPI exportée
│   └── postman.json       # Collection Postman
├── scripts/
│   ├── setup.sh
│   └── seed_data.py
├── .env.example
├── Makefile
├── requirements.txt
└── README.md

👤 Auteur

SOKE Honoré

    GitHub : @sokehonore

    Email : sokehonore@shido.com

    Projet SHIDO : Plateforme e-commerce microservices

📄 Licence

Copyright © 2026 SHIDO. Tous droits réservés.
