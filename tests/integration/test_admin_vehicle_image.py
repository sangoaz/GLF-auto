"""Tests d'intégration : routes admin images véhicules"""

import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.models.vehicle import VehicleImage


def create_vehicle_image(session, vehicle_id, order=0, is_cover=False):
    img = VehicleImage(
        image_url=f"/uploads/vehicles/img_{order}.jpg",
        is_cover=is_cover,
        display_order=order,
        vehicle_id=vehicle_id,
    )
    session.add(img)
    session.commit()
    session.refresh(img)
    return img


class TestListVehicleImages:
    def test_liste_vide(self, client: TestClient, auth_headers, vehicle):
        response = client.get(
            f"/admin/vehicles/{vehicle.id}/images", headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_liste_avec_images(
        self, client: TestClient, auth_headers, session, vehicle
    ):
        create_vehicle_image(session, vehicle.id, order=0)
        create_vehicle_image(session, vehicle.id, order=1)

        response = client.get(
            f"/admin/vehicles/{vehicle.id}/images", headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_vehicule_inexistant(self, client: TestClient, auth_headers):
        response = client.get("/admin/vehicles/99999/images", headers=auth_headers)
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, vehicle):
        response = client.get(f"/admin/vehicles/{vehicle.id}/images")
        assert response.status_code == 401


class TestUploadVehicleImage:
    def test_upload_succes(self, client: TestClient, auth_headers, vehicle):
        fake_image = io.BytesIO(b"fake image content")

        with patch(
            "app.routes.admin_vehicles.save_uploaded_image",
            return_value="/uploads/vehicles/abc123.jpg",
        ):
            response = client.post(
                f"/admin/vehicles/{vehicle.id}/images/upload",
                files={"file": ("photo.jpg", fake_image, "image/jpeg")},
                data={"display_order": "0", "alt_text": "Photo principale"},
                headers=auth_headers,
            )

        assert response.status_code == 201
        data = response.json()
        assert data["image_url"] == "/uploads/vehicles/abc123.jpg"
        assert data["alt_text"] == "Photo principale"
        assert data["display_order"] == 0

    def test_upload_sans_alt_text(self, client: TestClient, auth_headers, vehicle):
        fake_image = io.BytesIO(b"fake image content")

        with patch(
            "app.routes.admin_vehicles.save_uploaded_image",
            return_value="/uploads/vehicles/abc123.jpg",
        ):
            response = client.post(
                f"/admin/vehicles/{vehicle.id}/images/upload",
                files={"file": ("photo.jpg", fake_image, "image/jpeg")},
                data={"display_order": "0"},
                headers=auth_headers,
            )

        assert response.status_code == 201
        assert response.json()["alt_text"] is None

    def test_upload_vehicule_inexistant(self, client: TestClient, auth_headers):
        fake_image = io.BytesIO(b"fake image content")

        with patch(
            "app.routes.admin_vehicles.save_uploaded_image",
            return_value="/uploads/vehicles/abc123.jpg",
        ):
            response = client.post(
                "/admin/vehicles/99999/images/upload",
                files={"file": ("photo.jpg", fake_image, "image/jpeg")},
                data={"display_order": "0"},
                headers=auth_headers,
            )

        assert response.status_code == 404

    def test_upload_non_authentifie(self, client: TestClient, vehicle):
        fake_image = io.BytesIO(b"fake image content")
        response = client.post(
            f"/admin/vehicles/{vehicle.id}/images/upload",
            files={"file": ("photo.jpg", fake_image, "image/jpeg")},
            data={"display_order": "0"},
        )
        assert response.status_code == 401


class TestSetVehicleCoverImage:
    def test_definir_couverture(
        self, client: TestClient, auth_headers, session, vehicle
    ):
        img0 = create_vehicle_image(session, vehicle.id, order=0, is_cover=True)
        img1 = create_vehicle_image(session, vehicle.id, order=1, is_cover=False)

        response = client.patch(
            f"/admin/vehicles/{vehicle.id}/images/{img1.id}/cover",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["is_cover"] is True

        # Vérifier que l'ancienne couverture est bien retirée
        session.refresh(img0)
        assert img0.is_cover is False

    def test_image_inexistante(self, client: TestClient, auth_headers, vehicle):
        response = client.patch(
            f"/admin/vehicles/{vehicle.id}/images/99999/cover",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, vehicle):
        response = client.patch(f"/admin/vehicles/{vehicle.id}/images/1/cover")
        assert response.status_code == 401


class TestUpdateVehicleImage:
    def test_modifier_alt_text(
        self, client: TestClient, auth_headers, session, vehicle
    ):
        img = create_vehicle_image(session, vehicle.id, order=0)

        response = client.patch(
            f"/admin/vehicles/{vehicle.id}/images/{img.id}",
            json={"alt_text": "Nouvelle description"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["alt_text"] == "Nouvelle description"

    def test_modifier_display_order(
        self, client: TestClient, auth_headers, session, vehicle
    ):
        img0 = create_vehicle_image(session, vehicle.id, order=0)
        img1 = create_vehicle_image(session, vehicle.id, order=1)

        response = client.patch(
            f"/admin/vehicles/{vehicle.id}/images/{img1.id}",
            json={"display_order": 0},
            headers=auth_headers,
        )
        assert response.status_code == 200
        session.refresh(img0)
        assert img0.display_order == 1

    def test_image_inexistante(self, client: TestClient, auth_headers, vehicle):
        response = client.patch(
            f"/admin/vehicles/{vehicle.id}/images/99999",
            json={"alt_text": "Test"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, vehicle):
        response = client.patch(
            f"/admin/vehicles/{vehicle.id}/images/1",
            json={"alt_text": "Test"},
        )
        assert response.status_code == 401


class TestDeleteVehicleImage:
    def test_supprimer_image(self, client: TestClient, auth_headers, session, vehicle):
        img = create_vehicle_image(session, vehicle.id, order=0)
        img_id = img.id

        with patch("app.services.file_storage.delete_uploaded_file"):
            response = client.delete(
                f"/admin/vehicles/{vehicle.id}/images/{img_id}",
                headers=auth_headers,
            )

        assert response.status_code == 200
        assert session.get(VehicleImage, img_id) is None

    def test_suppression_reindexe_les_autres(
        self, client: TestClient, auth_headers, session, vehicle
    ):
        img0 = create_vehicle_image(session, vehicle.id, order=0)
        img1 = create_vehicle_image(session, vehicle.id, order=1)

        with patch("app.services.file_storage.delete_uploaded_file"):
            client.delete(
                f"/admin/vehicles/{vehicle.id}/images/{img0.id}",
                headers=auth_headers,
            )

        session.refresh(img1)
        assert img1.display_order == 0

    def test_image_inexistante(self, client: TestClient, auth_headers, vehicle):
        response = client.delete(
            f"/admin/vehicles/{vehicle.id}/images/99999",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, vehicle):
        response = client.delete(f"/admin/vehicles/{vehicle.id}/images/1")
        assert response.status_code == 401
