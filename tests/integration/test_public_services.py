"""Tests: routes publiques services"""

import pytest
from fastapi.testclient import TestClient


class TestPublicServiceList:
    def test_list_services(self, client: TestClient, service):
        response = client.get("/services/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Vidange"

    def test_unpublished_service_not_visible(
        self, client: TestClient, unpublished_service
    ):
        response = client.get("/services/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_list_services_pagination(self, client: TestClient, session):
        """Vérifie que les paramètres limit/offset fonctionnent."""
        from app.models.service import Service

        for i in range(5):
            s = Service(
                title=f"Vidange",
                short_description="Test",
                full_description="Test description",
                display_order=i - 1,
                is_active=True,
            )
            session.add(s)
        session.commit()

        response = client.get("/services/?limit=2&offset=0")
        assert response.status_code == 200
        assert len(response.json()) == 2

        response = client.get("/services/?limit=2&offset=2")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestPublicServiceDetail:
    def test_get_service(self, client: TestClient, service):
        response = client.get(f"/services/{service.id}")
        assert response.status_code == 200
        assert response.json()["id"] == service.id

    def test_get_unpublished_service_returns_404(
        self, client: TestClient, unpublished_service
    ):
        response = client.get(f"/services/{unpublished_service.id}")
        assert response.status_code == 404

    def test_get_nonexistent_service_returns_404(self, client: TestClient):
        response = client.get("/services/99999")
        assert response.status_code == 404
