"""Tests : authentification (login, /me)"""

import pytest
from fastapi.testclient import TestClient


class TestLogin:
    def test_login_success(self, client: TestClient, admin_user):
        response = client.post(
            "/auth/login",
            data={"username": "admin@glf.fr", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, admin_user):
        response = client.post(
            "/auth/login",
            data={"username": "admin@glf.fr", "password": "mauvais_mdp"},
        )
        assert response.status_code == 401

    def test_login_unknown_email(self, client: TestClient):
        response = client.post(
            "/auth/login",
            data={"username": "inconnu@glf.fr", "password": "password123"},
        )
        assert response.status_code == 401

    def test_login_missing_fields(self, client: TestClient):
        response = client.post("/auth/login", data={})
        assert response.status_code == 422


class TestGetMe:
    def test_get_me_authenticated(self, client: TestClient, auth_headers, admin_user):
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "admin@glf.fr"
        assert data["role"] == "ADMIN"

    def test_get_me_unauthenticated(self, client: TestClient):
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self, client: TestClient):
        response = client.get(
            "/auth/me", headers={"Authorization": "Bearer token_invalide"}
        )
        assert response.status_code == 401
