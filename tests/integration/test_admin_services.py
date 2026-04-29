"""Tests d'intégration: routes admin services"""

import pytest
from fastapi.testclient import TestClient

SERVICE_PAYLOAD = {
    "title": "Vidange",
    "short_description": "Vidange toutes marques",
    "full_description": "Vidange moteur + filtre à huile pour toutes marques.",
    "display_order": 1,
    "is_active": True,
}


class TestAdminServiceCreate:
    def test_create_service_as_admin(self, client: TestClient, auth_headers):
        response = client.post(
            "/admin/services", json=SERVICE_PAYLOAD, headers=auth_headers
        )
        print(response.json())
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Vidange"
        assert (
            data["full_description"]
            == "Vidange moteur + filtre à huile pour toutes marques."
        )

    def test_create_service_unauthenticated(self, client: TestClient):
        response = client.post("/admin/services", json=SERVICE_PAYLOAD)
        assert response.status_code == 401

    def test_create_service_missing_fields(self, client: TestClient, auth_headers):
        response = client.post(
            "/admin/services", json={"title": "Incomplet"}, headers=auth_headers
        )
        assert response.status_code == 422


class TestAdminServiceList:
    def test_list_services_as_admin(self, client: TestClient, auth_headers, service):
        response = client.get("/admin/services", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_list_services_unauthenticated(self, client: TestClient):
        response = client.get("/admin/services")
        assert response.status_code == 401


class TestAdminServiceGet:
    def test_get_service_as_admin(self, client: TestClient, auth_headers, service):
        response = client.get(f"/admin/services/{service.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == service.id

    def test_get_nonexistent_service(self, client: TestClient, auth_headers):
        response = client.get("/admin/services/99999", headers=auth_headers)
        assert response.status_code == 404


class TestAdminServicePatch:
    def test_patch_price(self, client: TestClient, auth_headers, service):
        response = client.patch(
            f"/admin/services/{service.id}",
            json={"title": "Lavage Auto"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Lavage Auto"
