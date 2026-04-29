"""Tests : routes publiques véhicules"""

import pytest
from fastapi.testclient import TestClient


class TestPublicVehicleList:
    def test_list_published_vehicles(self, client: TestClient, vehicle):
        response = client.get("/vehicles/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Peugeot 308 SW"

    def test_unpublished_vehicle_not_visible(
        self, client: TestClient, unpublished_vehicle
    ):
        response = client.get("/vehicles/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_list_vehicles_pagination(self, client: TestClient, session):
        """Vérifie que les paramètres limit/offset fonctionnent."""
        from app.models.vehicle import Vehicle
        from app.enums import FuelType, TransmissionType, VehicleStatus

        for i in range(5):
            v = Vehicle(
                title=f"Véhicule {i}",
                brand="Test",
                model=f"Model {i}",
                year=2020,
                mileage=10000,
                fuel=FuelType.PETROL,
                transmission=TransmissionType.MANUAL,
                price=5000 + i * 1000,
                description="Test",
                status=VehicleStatus.AVAILABLE,
                is_published=True,
            )
            session.add(v)
        session.commit()

        response = client.get("/vehicles/?limit=2&offset=0")
        assert response.status_code == 200
        assert len(response.json()) == 2

        response = client.get("/vehicles/?limit=2&offset=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_featured_vehicles_first(self, client: TestClient, session):
        """Vérifie que les véhicules is_featured remontent en premier."""
        from app.models.vehicle import Vehicle
        from app.enums import FuelType, TransmissionType, VehicleStatus

        v1 = Vehicle(
            title="Normal",
            brand="A",
            model="X",
            year=2019,
            mileage=60000,
            fuel=FuelType.PETROL,
            transmission=TransmissionType.MANUAL,
            price=8000,
            description="",
            is_published=True,
            is_featured=False,
        )
        v2 = Vehicle(
            title="Featured",
            brand="B",
            model="Y",
            year=2021,
            mileage=20000,
            fuel=FuelType.DIESEL,
            transmission=TransmissionType.AUTOMATIC,
            price=18000,
            description="",
            is_published=True,
            is_featured=True,
        )
        session.add_all([v1, v2])
        session.commit()

        response = client.get("/vehicles/")
        data = response.json()
        assert data[0]["title"] == "Featured"


class TestPublicVehicleDetail:
    def test_get_published_vehicle(self, client: TestClient, vehicle):
        response = client.get(f"/vehicles/{vehicle.id}")
        assert response.status_code == 200
        assert response.json()["id"] == vehicle.id

    def test_get_unpublished_vehicle_returns_404(
        self, client: TestClient, unpublished_vehicle
    ):
        response = client.get(f"/vehicles/{unpublished_vehicle.id}")
        assert response.status_code == 404

    def test_get_nonexistent_vehicle_returns_404(self, client: TestClient):
        response = client.get("/vehicles/99999")
        assert response.status_code == 404
