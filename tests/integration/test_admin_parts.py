"""Tests : routes admin pièces détachées"""

import pytest
from fastapi.testclient import TestClient


PART_PAYLOAD = {
    "title": "Démarreur Renault Clio",
    "category": "Electricité",
    "brand": "Renault",
    "compatible_models": "Clio II, Clio III",
    "condition": "Bon état",
    "price": 45,
    "description": "Démarreur testé, fonctionnel.",
    "status": "available",
    "is_featured": True,
    "is_published": True,
}


class TestAdminPartCreate:
    def test_create_part_as_admin(self, client: TestClient, auth_headers):
        response = client.post("/admin/parts", json=PART_PAYLOAD, headers=auth_headers)
        assert response.status_code == 201

    def test_create_part_unauthenticated(self, client: TestClient):
        response = client.post("/admin/parts", json=PART_PAYLOAD)
        assert response.status_code == 401


class TestAdminPartList:
    def test_list_parts_as_admin(self, client: TestClient, auth_headers, part):
        response = client.get("/admin/parts", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_list_parts_unauthenticated(self, client: TestClient):
        response = client.get("/admin/parts")
        assert response.status_code == 401


class TestAdminPartGet:
    def test_get_part_as_admin(self, client: TestClient, auth_headers, part):
        response = client.get(f"/admin/parts/{part.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == part.id

    def test_get_nonexistent_part(self, client: TestClient, auth_headers):
        response = client.get("/admin/parts/99999", headers=auth_headers)
        assert response.status_code == 404


class TestAdminPartPatch:
    def test_patch_price(self, client: TestClient, auth_headers, part):
        response = client.patch(
            f"/admin/parts/{part.id}",
            json={"price": 60},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["price"] == 60

    def test_patch_status_sold_unpublishes(
        self, client: TestClient, auth_headers, part
    ):
        response = client.patch(
            f"/admin/parts/{part.id}",
            json={"status": "SOLD"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_published"] is False
        assert data["is_featured"] is False

    def test_patch_unauthenticated(self, client: TestClient, part):
        response = client.patch(f"/admin/parts/{part.id}", json={"price": 10})
        assert response.status_code == 401
