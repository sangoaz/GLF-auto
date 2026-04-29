import pytest
from fastapi.testclient import TestClient
from app.enums import VehicleStatus


VEHICLE_PAYLOAD = {
    "title": "Citroën C3",
    "brand": "Citroën",
    "model": "C3",
    "year": 2021,
    "mileage": 30000,
    "fuel": "PETROL",
    "transmission": "MANUAL",
    "price": 11500,
    "description": "Première main, entretien OK.",
    "status": "available",
    "is_featured": True,
    "is_published": True,
}


class TestAdminVehicleCreate:
    def test_create_vehicle_as_admin(self, client: TestClient, auth_headers):
        response = client.post(
            "/admin/vehicles", json=VEHICLE_PAYLOAD, headers=auth_headers
        )
        print(response.json())
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Citroën C3"
        assert data["price"] == 11500

    def test_create_vehicle_unauthenticated(self, client: TestClient):
        response = client.post("/admin/vehicles", json=VEHICLE_PAYLOAD)
        assert response.status_code == 401

    def test_create_vehicle_missing_fields(self, client: TestClient, auth_headers):
        response = client.post(
            "/admin/vehicles", json={"title": "Incomplet"}, headers=auth_headers
        )
        assert response.status_code == 422


class TestAdminVehicleList:
    def test_list_vehicles_as_admin(self, client: TestClient, auth_headers, vehicle):
        response = client.get("/admin/vehicles", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_list_vehicles_unauthenticated(self, client: TestClient):
        response = client.get("/admin/vehicles")
        assert response.status_code == 401

    def test_list_includes_unpublished(
        self, client: TestClient, auth_headers, unpublished_vehicle
    ):
        """L'admin voit aussi les véhicules non publiés."""
        response = client.get("/admin/vehicles", headers=auth_headers)
        ids = [v["id"] for v in response.json()]
        assert unpublished_vehicle.id in ids


class TestAdminVehicleGet:
    def test_get_vehicle_as_admin(self, client: TestClient, auth_headers, vehicle):
        response = client.get(f"/admin/vehicles/{vehicle.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == vehicle.id

    def test_get_nonexistent_vehicle(self, client: TestClient, auth_headers):
        response = client.get("/admin/vehicles/99999", headers=auth_headers)
        assert response.status_code == 404


class TestAdminVehiclePatch:
    def test_patch_price(self, client: TestClient, auth_headers, vehicle):
        response = client.patch(
            f"/admin/vehicles/{vehicle.id}",
            json={"price": 13000},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["price"] == 13000

    def test_patch_status_sold_unpublishes(
        self, client: TestClient, auth_headers, vehicle
    ):
        """Marquer comme vendu doit dépublier et retirer de la mise en avant."""
        response = client.patch(
            f"/admin/vehicles/{vehicle.id}",
            json={"status": "SOLD"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SOLD"
        assert data["is_published"] is False
        assert data["is_featured"] is False

    def test_patch_status_reserved_removes_featured(
        self, client: TestClient, auth_headers, vehicle
    ):
        """Marquer comme réservé doit retirer la mise en avant."""
        response = client.patch(
            f"/admin/vehicles/{vehicle.id}",
            json={"status": "RESERVED"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_featured"] is False

    def test_patch_nonexistent_vehicle(self, client: TestClient, auth_headers):
        response = client.patch(
            "/admin/vehicles/99999", json={"price": 1000}, headers=auth_headers
        )
        assert response.status_code == 404

    def test_patch_unauthenticated(self, client: TestClient, vehicle):
        response = client.patch(f"/admin/vehicles/{vehicle.id}", json={"price": 1000})
        assert response.status_code == 401
