"""Tests : routes publiques pièces d'occasion"""

import pytest
from fastapi.testclient import TestClient
from app.models.part import Part
from app.enums import PartStatus


class TestPublicPartList:
    def test_list_published_parts(self, client: TestClient, part):
        response = client.get("/parts/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Alternateur Peugeot 308"

    def test_unpublished_part_not_visible(self, client: TestClient, session):
        p = Part(
            title="Pièce masquée",
            category="Carrosserie",
            brand="Test",
            compatible_models="X",
            condition="Usé",
            price=10,
            description="",
            is_published=False,
        )
        session.add(p)
        session.commit()

        response = client.get("/parts/")
        assert response.status_code == 200
        titles = [p["title"] for p in response.json()]
        assert "Pièce masquée" not in titles

    def test_get_published_part(self, client: TestClient, part):
        response = client.get(f"/parts/{part.id}")
        assert response.status_code == 200
        assert response.json()["id"] == part.id

    def test_get_nonexistent_part(self, client: TestClient):
        response = client.get("/parts/99999")
        assert response.status_code == 404
