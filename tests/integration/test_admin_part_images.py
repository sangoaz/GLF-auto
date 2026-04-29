"""Tests d'intégration : routes admin images pièces"""

import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.models.part import PartImage


def create_part_image(session, part_id, order=0, is_cover=False):
    img = PartImage(
        image_url=f"/uploads/parts/img_{order}.jpg",
        is_cover=is_cover,
        display_order=order,
        part_id=part_id,
    )
    session.add(img)
    session.commit()
    session.refresh(img)
    return img


class TestListPartImages:
    def test_liste_vide(self, client: TestClient, auth_headers, part):
        response = client.get(f"/admin/parts/{part.id}/images", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_liste_avec_images(self, client: TestClient, auth_headers, session, part):
        create_part_image(session, part.id, order=0)
        create_part_image(session, part.id, order=1)

        response = client.get(f"/admin/parts/{part.id}/images", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_piece_inexistante(self, client: TestClient, auth_headers):
        response = client.get("/admin/parts/99999/images", headers=auth_headers)
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, part):
        response = client.get(f"/admin/parts/{part.id}/images")
        assert response.status_code == 401


class TestUploadPartImage:
    def test_upload_succes(self, client: TestClient, auth_headers, part):
        fake_image = io.BytesIO(b"fake image content")

        with patch(
            "app.routes.admin_parts.save_uploaded_image",
            return_value="/uploads/parts/abc123.jpg",
        ):
            response = client.post(
                f"/admin/parts/{part.id}/images/upload",
                files={"file": ("photo.jpg", fake_image, "image/jpeg")},
                data={"display_order": "0", "alt_text": "Photo pièce"},
                headers=auth_headers,
            )

        assert response.status_code == 201
        data = response.json()
        assert data["image_url"] == "/uploads/parts/abc123.jpg"
        assert data["alt_text"] == "Photo pièce"

    def test_upload_piece_inexistante(self, client: TestClient, auth_headers):
        fake_image = io.BytesIO(b"fake image content")

        with patch(
            "app.routes.admin_parts.save_uploaded_image",
            return_value="/uploads/parts/abc123.jpg",
        ):
            response = client.post(
                "/admin/parts/99999/images/upload",
                files={"file": ("photo.jpg", fake_image, "image/jpeg")},
                data={"display_order": "0"},
                headers=auth_headers,
            )

        assert response.status_code == 404

    def test_upload_non_authentifie(self, client: TestClient, part):
        fake_image = io.BytesIO(b"fake image content")
        response = client.post(
            f"/admin/parts/{part.id}/images/upload",
            files={"file": ("photo.jpg", fake_image, "image/jpeg")},
            data={"display_order": "0"},
        )
        assert response.status_code == 401


class TestSetPartCoverImage:
    def test_definir_couverture(self, client: TestClient, auth_headers, session, part):
        img0 = create_part_image(session, part.id, order=0, is_cover=True)
        img1 = create_part_image(session, part.id, order=1, is_cover=False)

        response = client.patch(
            f"/admin/parts/{part.id}/images/{img1.id}/cover",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["is_cover"] is True

        session.refresh(img0)
        assert img0.is_cover is False

    def test_image_inexistante(self, client: TestClient, auth_headers, part):
        response = client.patch(
            f"/admin/parts/{part.id}/images/99999/cover",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, part):
        response = client.patch(f"/admin/parts/{part.id}/images/1/cover")
        assert response.status_code == 401


class TestUpdatePartImage:
    def test_modifier_alt_text(self, client: TestClient, auth_headers, session, part):
        img = create_part_image(session, part.id, order=0)

        response = client.patch(
            f"/admin/parts/{part.id}/images/{img.id}",
            json={"alt_text": "Nouvelle description"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["alt_text"] == "Nouvelle description"

    def test_modifier_display_order(
        self, client: TestClient, auth_headers, session, part
    ):
        img0 = create_part_image(session, part.id, order=0)
        img1 = create_part_image(session, part.id, order=1)

        response = client.patch(
            f"/admin/parts/{part.id}/images/{img1.id}",
            json={"display_order": 0},
            headers=auth_headers,
        )
        assert response.status_code == 200
        session.refresh(img0)
        assert img0.display_order == 1

    def test_image_inexistante(self, client: TestClient, auth_headers, part):
        response = client.patch(
            f"/admin/parts/{part.id}/images/99999",
            json={"alt_text": "Test"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, part):
        response = client.patch(
            f"/admin/parts/{part.id}/images/1",
            json={"alt_text": "Test"},
        )
        assert response.status_code == 401


class TestDeletePartImage:
    def test_supprimer_image(self, client: TestClient, auth_headers, session, part):
        img = create_part_image(session, part.id, order=0)
        img_id = img.id

        with patch("app.services.file_storage.delete_uploaded_file"):
            response = client.delete(
                f"/admin/parts/{part.id}/images/{img_id}",
                headers=auth_headers,
            )

        assert response.status_code == 200
        assert session.get(PartImage, img_id) is None

    def test_suppression_reindexe_les_autres(
        self, client: TestClient, auth_headers, session, part
    ):
        img0 = create_part_image(session, part.id, order=0)
        img1 = create_part_image(session, part.id, order=1)

        with patch("app.services.file_storage.delete_uploaded_file"):
            client.delete(
                f"/admin/parts/{part.id}/images/{img0.id}",
                headers=auth_headers,
            )

        session.refresh(img1)
        assert img1.display_order == 0

    def test_image_inexistante(self, client: TestClient, auth_headers, part):
        response = client.delete(
            f"/admin/parts/{part.id}/images/99999",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, part):
        response = client.delete(f"/admin/parts/{part.id}/images/1")
        assert response.status_code == 401
