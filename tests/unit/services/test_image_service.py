"""Tests unitaires : app/services/image_service.py"""

import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.models.vehicle import Vehicle, VehicleImage
from app.enums import FuelType, TransmissionType, VehicleStatus
from app.services.image_service import (
    insert_image_with_order,
    reorder_image,
    delete_image_with_reindex,
    set_cover_image,
)


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


@pytest.fixture(name="vehicle")
def vehicle_fixture(session):
    v = Vehicle(
        title="Peugeot 308",
        brand="Peugeot",
        model="308",
        year=2020,
        mileage=40000,
        fuel=FuelType.DIESEL,
        transmission=TransmissionType.MANUAL,
        price=14000,
        description="Test",
        status=VehicleStatus.AVAILABLE,
        is_published=True,
    )
    session.add(v)
    session.commit()
    session.refresh(v)
    return v


def make_image(session, vehicle_id, order, is_cover=False, url=None):
    """Helper pour créer une image et la persister."""
    img = VehicleImage(
        image_url=url or f"uploads/vehicles/img_{order}.jpg",
        is_cover=is_cover,
        display_order=order,
        vehicle_id=vehicle_id,
    )
    session.add(img)
    session.commit()
    session.refresh(img)
    return img


# ──────────────────────────────────────────
# Tests : insert_image_with_order
# ──────────────────────────────────────────


class TestInsertImageWithOrder:
    def test_insertion_dans_liste_vide(self, session, vehicle):
        new_img = VehicleImage(
            image_url="uploads/vehicles/new.jpg",
            display_order=0,
            vehicle_id=vehicle.id,
        )
        insert_image_with_order(
            session, VehicleImage, "vehicle_id", vehicle.id, new_img
        )
        session.commit()
        assert new_img.display_order == 0

    def test_insertion_en_debut_de_liste(self, session, vehicle):
        """Insérer en position 0 doit décaler les autres."""
        img0 = make_image(session, vehicle.id, 0)
        img1 = make_image(session, vehicle.id, 1)

        new_img = VehicleImage(
            image_url="uploads/vehicles/new.jpg",
            display_order=0,
            vehicle_id=vehicle.id,
        )
        insert_image_with_order(
            session, VehicleImage, "vehicle_id", vehicle.id, new_img
        )
        session.commit()
        session.refresh(img0)
        session.refresh(img1)

        assert new_img.display_order == 0
        assert img0.display_order == 1
        assert img1.display_order == 2

    def test_insertion_en_milieu_de_liste(self, session, vehicle):
        """Insérer en position 1 ne doit décaler que les images >= 1."""
        img0 = make_image(session, vehicle.id, 0)
        img1 = make_image(session, vehicle.id, 1)
        img2 = make_image(session, vehicle.id, 2)

        new_img = VehicleImage(
            image_url="uploads/vehicles/new.jpg",
            display_order=1,
            vehicle_id=vehicle.id,
        )
        insert_image_with_order(
            session, VehicleImage, "vehicle_id", vehicle.id, new_img
        )
        session.commit()
        session.refresh(img0)
        session.refresh(img1)
        session.refresh(img2)

        assert img0.display_order == 0
        assert new_img.display_order == 1
        assert img1.display_order == 2
        assert img2.display_order == 3

    def test_ordre_trop_grand_ramene_a_la_fin(self, session, vehicle):
        """Un ordre > nombre d'images doit être ramené au maximum."""
        make_image(session, vehicle.id, 0)
        make_image(session, vehicle.id, 1)

        new_img = VehicleImage(
            image_url="uploads/vehicles/new.jpg",
            display_order=999,
            vehicle_id=vehicle.id,
        )
        insert_image_with_order(
            session, VehicleImage, "vehicle_id", vehicle.id, new_img
        )
        session.commit()

        assert new_img.display_order == 2


# ──────────────────────────────────────────
# Tests : reorder_image
# ──────────────────────────────────────────


class TestReorderImage:
    def test_deplacer_vers_le_haut(self, session, vehicle):
        """Déplacer l'image en position 2 vers la position 0."""
        img0 = make_image(session, vehicle.id, 0)
        img1 = make_image(session, vehicle.id, 1)
        img2 = make_image(session, vehicle.id, 2)

        reorder_image(session, VehicleImage, "vehicle_id", vehicle.id, img2, 0)
        session.commit()
        session.refresh(img0)
        session.refresh(img1)
        session.refresh(img2)

        assert img2.display_order == 0
        assert img0.display_order == 1
        assert img1.display_order == 2

    def test_deplacer_vers_le_bas(self, session, vehicle):
        """Déplacer l'image en position 0 vers la position 2."""
        img0 = make_image(session, vehicle.id, 0)
        img1 = make_image(session, vehicle.id, 1)
        img2 = make_image(session, vehicle.id, 2)

        reorder_image(session, VehicleImage, "vehicle_id", vehicle.id, img0, 2)
        session.commit()
        session.refresh(img0)
        session.refresh(img1)
        session.refresh(img2)

        assert img0.display_order == 2
        assert img1.display_order == 0
        assert img2.display_order == 1

    def test_meme_position_ne_change_rien(self, session, vehicle):
        """Réordonner vers la même position ne doit rien modifier."""
        img0 = make_image(session, vehicle.id, 0)
        img1 = make_image(session, vehicle.id, 1)

        reorder_image(session, VehicleImage, "vehicle_id", vehicle.id, img0, 0)
        session.commit()
        session.refresh(img0)
        session.refresh(img1)

        assert img0.display_order == 0
        assert img1.display_order == 1

    def test_ordre_negatif_ramene_a_zero(self, session, vehicle):
        img0 = make_image(session, vehicle.id, 0)
        img1 = make_image(session, vehicle.id, 1)

        reorder_image(session, VehicleImage, "vehicle_id", vehicle.id, img1, -5)
        session.commit()
        session.refresh(img1)

        assert img1.display_order == 0


# ──────────────────────────────────────────
# Tests : delete_image_with_reindex
# ──────────────────────────────────────────


class TestDeleteImageWithReindex:
    def test_suppression_reindexe_les_suivantes(self, session, vehicle):
        """Supprimer l'image en position 0 doit décaler les suivantes."""
        img0 = make_image(session, vehicle.id, 0)
        img1 = make_image(session, vehicle.id, 1)
        img2 = make_image(session, vehicle.id, 2)

        delete_image_with_reindex(session, VehicleImage, "vehicle_id", vehicle.id, img0)
        session.commit()
        session.refresh(img1)
        session.refresh(img2)

        assert img1.display_order == 0
        assert img2.display_order == 1

    def test_suppression_derniere_image(self, session, vehicle):
        """Supprimer la dernière image ne doit pas modifier les autres."""
        img0 = make_image(session, vehicle.id, 0)
        img1 = make_image(session, vehicle.id, 1)

        delete_image_with_reindex(session, VehicleImage, "vehicle_id", vehicle.id, img1)
        session.commit()
        session.refresh(img0)

        assert img0.display_order == 0

    def test_image_supprimee_absente_de_la_base(self, session, vehicle):
        img0 = make_image(session, vehicle.id, 0)
        img0_id = img0.id

        delete_image_with_reindex(session, VehicleImage, "vehicle_id", vehicle.id, img0)
        session.commit()

        assert session.get(VehicleImage, img0_id) is None


# ──────────────────────────────────────────
# Tests : set_cover_image
# ──────────────────────────────────────────


class TestSetCoverImage:
    def test_definit_la_nouvelle_couverture(self, session, vehicle):
        img0 = make_image(session, vehicle.id, 0, is_cover=True)
        img1 = make_image(session, vehicle.id, 1, is_cover=False)

        set_cover_image(session, VehicleImage, "vehicle_id", vehicle.id, img1)
        session.commit()
        session.refresh(img0)
        session.refresh(img1)

        assert img1.is_cover is True
        assert img0.is_cover is False

    def test_une_seule_couverture_possible(self, session, vehicle):
        """Après set_cover, une seule image doit avoir is_cover=True."""
        images = [
            make_image(session, vehicle.id, i, is_cover=(i == 0)) for i in range(4)
        ]

        set_cover_image(session, VehicleImage, "vehicle_id", vehicle.id, images[3])
        session.commit()
        for img in images:
            session.refresh(img)

        covers = [img for img in images if img.is_cover]
        assert len(covers) == 1
        assert covers[0].id == images[3].id

    def test_redefinir_la_meme_couverture(self, session, vehicle):
        """Définir comme couverture une image déjà couverture doit fonctionner."""
        img0 = make_image(session, vehicle.id, 0, is_cover=True)
        img1 = make_image(session, vehicle.id, 1, is_cover=False)

        set_cover_image(session, VehicleImage, "vehicle_id", vehicle.id, img0)
        session.commit()
        session.refresh(img0)
        session.refresh(img1)

        assert img0.is_cover is True
        assert img1.is_cover is False
