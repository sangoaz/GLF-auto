"""Tests unitaires : app/utils/auth.py et app/core/security.py"""

import os

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test_secret_key_for_pytest")

import pytest
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.models.user import User
from app.enums import UserRole
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from app.utils.auth import authenticate_user, invalid_credentials


# ──────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="active_user")
def active_user_fixture(session):
    user = User(
        email="user@glf.fr",
        password_hash=hash_password("motdepasse"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="inactive_user")
def inactive_user_fixture(session):
    user = User(
        email="inactif@glf.fr",
        password_hash=hash_password("motdepasse"),
        role=UserRole.ADMIN,
        is_active=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# ──────────────────────────────────────────
# Tests : security.py
# ──────────────────────────────────────────


class TestPasswordHashing:
    def test_hash_different_du_mot_de_passe(self):
        hashed = hash_password("secret")
        assert hashed != "secret"

    def test_verify_correct(self):
        hashed = hash_password("secret")
        assert verify_password("secret", hashed) is True

    def test_verify_incorrect(self):
        hashed = hash_password("secret")
        assert verify_password("mauvais", hashed) is False

    def test_deux_hash_differents_pour_meme_mdp(self):
        """bcrypt génère un salt aléatoire donc deux hash doivent être différents."""
        h1 = hash_password("secret")
        h2 = hash_password("secret")
        assert h1 != h2


class TestJWT:
    def test_creation_et_decodage_token(self):
        token = create_access_token(data={"sub": "1", "role": "ADMIN"})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "1"
        assert payload["role"] == "ADMIN"

    def test_token_invalide_retourne_none(self):
        result = decode_access_token("token.invalide.ici")
        assert result is None

    def test_token_contient_expiration(self):
        token = create_access_token(data={"sub": "1"})
        payload = decode_access_token(token)
        assert "exp" in payload


# ──────────────────────────────────────────
# Tests : authenticate_user
# ──────────────────────────────────────────


class TestAuthenticateUser:
    def test_authentification_reussie(self, session, active_user):
        result = authenticate_user(session, "user@glf.fr", "motdepasse")
        assert result is not None
        assert result.email == "user@glf.fr"

    def test_mauvais_mot_de_passe(self, session, active_user):
        result = authenticate_user(session, "user@glf.fr", "mauvais")
        assert result is None

    def test_email_inconnu(self, session):
        result = authenticate_user(session, "inconnu@glf.fr", "motdepasse")
        assert result is None

    def test_user_inactif(self, session, inactive_user):
        result = authenticate_user(session, "inactif@glf.fr", "motdepasse")
        assert result is None


# ──────────────────────────────────────────
# Tests : invalid_credentials
# ──────────────────────────────────────────


class TestInvalidCredentials:
    def test_leve_401(self):
        with pytest.raises(HTTPException) as exc_info:
            invalid_credentials()
        assert exc_info.value.status_code == 401

    def test_contient_header_www_authenticate(self):
        with pytest.raises(HTTPException) as exc_info:
            invalid_credentials()
        assert "WWW-Authenticate" in exc_info.value.headers
