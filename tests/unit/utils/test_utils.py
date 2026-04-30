"""Tests unitaires : app/utils/vehicle.py, app/utils/part.py, app/utils/image.py, app/utils/services.py, app/utils/messages.py"""

import pytest
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.models.vehicle import Vehicle, VehicleImage
from app.models.part import Part, PartImage
from app.models.service import Service
from app.models.contact_request import ContactRequest
from app.models.trade_in_request import TradeInRequest
from app.enums import FuelType, TransmissionType, VehicleStatus, PartStatus
from app.utils.vehicle import get_vehicle_or_404
from app.utils.part import get_part_or_404
from app.utils.services import get_service_or_404
from app.utils.image import get_vehicle_image_or_404, get_part_image_or_404
from app.utils.messages import get_contact_request_or_404, get_trade_in_request_or_404

# ──────────────────────────────────────────
# Moteur SQLite en memoire local au fichier
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


@pytest.fixture(name="part")
def part_fixture(session):
    p = Part(
        title="Alternateur",
        category="Electricite",
        brand="Peugeot",
        compatible_models="308",
        condition="Bon",
        price=80,
        description="Test",
        status=PartStatus.AVAILABLE,
        is_published=True,
    )
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


@pytest.fixture(name="vehicle_image")
def vehicle_image_fixture(session, vehicle):
    img = VehicleImage(
        image_url="uploads/vehicles/test.jpg",
        is_cover=True,
        display_order=0,
        vehicle_id=vehicle.id,
    )
    session.add(img)
    session.commit()
    session.refresh(img)
    return img


@pytest.fixture(name="part_image")
def part_image_fixture(session, part):
    img = PartImage(
        image_url="uploads/parts/test.jpg",
        is_cover=True,
        display_order=0,
        part_id=part.id,
    )
    session.add(img)
    session.commit()
    session.refresh(img)
    return img


@pytest.fixture(name="service")
def service_fixture(session):
    s = Service(
        title="Révision",
        short_description="Révision du véhicule",
        full_description="Changement d'huile moteur, vérification des liquides, changement des filtres...",
        display_order=0,
        is_active=True,
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


@pytest.fixture(name="contact_request")
def contact_request_fixture(session):
    cr = ContactRequest(
        name="Roger Test",
        email="roger@test.fr",
        phone="06.06.06.07.08",
        subject="Révision de ma clio 3",
        message="Bonjour, combien prenez vous pour la révision d'un clio 3 diesel de 200000km",
        is_read=False,
    )
    session.add(cr)
    session.commit()
    session.refresh(cr)
    return cr


@pytest.fixture(name="trade_in_request")
def trade_in_fixture(session):
    cr = TradeInRequest(
        name="Roger Test Trade",
        email="roger@test.fr",
        phone="06.06.06.07.08",
        brand="Renault",
        model="Clio 3",
        year="2007",
        mileage="180000",
        condition_note="Véhicule d'occasion, bien vécu",
        message="Bonjour, combien me donneriez vous pour ma voiture ?",
        is_read=False,
    )
    session.add(cr)
    session.commit()
    session.refresh(cr)
    return cr


# ──────────────────────────────────────────
# Tests : get_vehicle_or_404
# ──────────────────────────────────────────


class TestGetVehicleOr404:
    def test_retourne_le_vehicule_existant(self, session, vehicle):
        result = get_vehicle_or_404(session, vehicle.id)
        assert result.id == vehicle.id
        assert result.title == "Peugeot 308"

    def test_leve_404_si_inexistant(self, session):
        with pytest.raises(HTTPException) as exc_info:
            get_vehicle_or_404(session, 99999)
        assert exc_info.value.status_code == 404
        assert "introuvable" in exc_info.value.detail.lower()


# ──────────────────────────────────────────
# Tests : get_part_or_404
# ──────────────────────────────────────────


class TestGetPartOr404:
    def test_retourne_la_piece_existante(self, session, part):
        result = get_part_or_404(session, part.id)
        assert result.id == part.id
        assert result.title == "Alternateur"

    def test_leve_404_si_inexistante(self, session):
        with pytest.raises(HTTPException) as exc_info:
            get_part_or_404(session, 99999)
        assert exc_info.value.status_code == 404
        assert "introuvable" in exc_info.value.detail.lower()


# ──────────────────────────────────────────
# Tests : get_vehicle_image_or_404
# ──────────────────────────────────────────


class TestGetVehicleImageOr404:
    def test_retourne_image_existante(self, session, vehicle, vehicle_image):
        result = get_vehicle_image_or_404(session, vehicle.id, vehicle_image.id)
        assert result.id == vehicle_image.id

    def test_leve_404_si_image_inexistante(self, session, vehicle):
        with pytest.raises(HTTPException) as exc_info:
            get_vehicle_image_or_404(session, vehicle.id, 99999)
        assert exc_info.value.status_code == 404

    def test_leve_404_si_image_appartient_a_un_autre_vehicule(
        self, session, vehicle, vehicle_image
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_vehicle_image_or_404(session, 99999, vehicle_image.id)
        assert exc_info.value.status_code == 404


# ──────────────────────────────────────────
# Tests : get_part_image_or_404
# ──────────────────────────────────────────


class TestGetPartImageOr404:
    def test_retourne_image_existante(self, session, part, part_image):
        result = get_part_image_or_404(session, part.id, part_image.id)
        assert result.id == part_image.id

    def test_leve_404_si_image_inexistante(self, session, part):
        with pytest.raises(HTTPException) as exc_info:
            get_part_image_or_404(session, part.id, 99999)
        assert exc_info.value.status_code == 404

    def test_leve_404_si_image_appartient_a_une_autre_piece(
        self, session, part, part_image
    ):
        with pytest.raises(HTTPException) as exc_info:
            get_part_image_or_404(session, 99999, part_image.id)
        assert exc_info.value.status_code == 404


# ──────────────────────────────────────────
# Tests : get_service_or_404
# ──────────────────────────────────────────


class TestGetServiceOr404:
    def test_retourne_le_service_existant(self, session, service):
        result = get_service_or_404(session, service.id)
        assert result.id == service.id
        assert result.title == "Révision"

    def test_leve_404_si_inexistant(self, session):
        with pytest.raises(HTTPException) as exc_info:
            get_service_or_404(session, 99999)
        assert exc_info.value.status_code == 404
        assert "introuvable" in exc_info.value.detail.lower()


# ──────────────────────────────────────────
# Tests : get_contact_request_or_404
# ──────────────────────────────────────────


class TestGetContactRequestOr404:
    def test_retourne_la_request_existante(self, session, contact_request):
        result = get_contact_request_or_404(session, contact_request.id)
        assert result.id == contact_request.id
        assert result.name == "Roger Test"

    def test_leve_404_si_inexistant(self, session):
        with pytest.raises(HTTPException) as exc_info:
            get_contact_request_or_404(session, 99999)
        assert exc_info.value.status_code == 404
        assert "introuvable" in exc_info.value.detail.lower()


# ──────────────────────────────────────────
# Tests : get_trade_in_request_or_404
# ──────────────────────────────────────────


class TestGetTradeInRequestOr404:
    def test_retourne_le_trade_in_existant(self, session, trade_in_request):
        result = get_trade_in_request_or_404(session, trade_in_request.id)
        assert result.id == trade_in_request.id
        assert result.name == "Roger Test Trade"

    def test_leve_404_si_inexistant(self, session):
        with pytest.raises(HTTPException) as exc_info:
            get_trade_in_request_or_404(session, 99999)
        assert exc_info.value.status_code == 404
        assert "introuvable" in exc_info.value.detail.lower()
