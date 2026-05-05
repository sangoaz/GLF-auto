"""
Configuration des fixtures Pytest pour le projet GLF.
Utilise une base SQLite en mémoire pour les tests.
"""

import os

# ⚠️ Ces lignes DOIVENT être avant tout import de l'app
# pour éviter que database.py tente de se connecter à PostgreSQL
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test_secret_key_for_pytest"

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.database import get_session
from app.core.security import hash_password, create_access_token
from app.models.user import User
from app.models.vehicle import Vehicle, VehicleImage
from app.models.part import Part, PartImage
from app.models.service import Service
from app.models.contact_request import ContactRequest
from app.models.trade_in_request import TradeInRequest
from app.enums import (
    UserRole,
    VehicleStatus,
    FuelType,
    TransmissionType,
    PartStatus,
    PartCondition,
)


# ──────────────────────────────────────────
# Moteur SQLite en mémoire pour les tests
# ──────────────────────────────────────────


@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ──────────────────────────────────────────
# Fixtures : données de base
# ──────────────────────────────────────────


@pytest.fixture(name="admin_user")
def admin_user_fixture(session):
    user = User(
        email="admin@glf.fr",
        password_hash=hash_password("password123"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="admin_token")
def admin_token_fixture(admin_user):
    return create_access_token(
        data={"sub": str(admin_user.id), "role": admin_user.role.value}
    )


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(name="vehicle")
def vehicle_fixture(session):
    v = Vehicle(
        title="Peugeot 308 SW",
        brand="Peugeot",
        model="308 SW",
        year=2020,
        mileage=45000,
        fuel=FuelType.DIESEL,
        transmission=TransmissionType.MANUAL,
        price=14900,
        description="Très bon état, entretien suivi.",
        status=VehicleStatus.AVAILABLE,
        is_featured=True,
        is_published=True,
    )
    session.add(v)
    session.commit()
    session.refresh(v)
    return v


@pytest.fixture(name="unpublished_vehicle")
def unpublished_vehicle_fixture(session):
    v = Vehicle(
        title="Renault Clio (non publiée)",
        brand="Renault",
        model="Clio",
        year=2018,
        mileage=80000,
        fuel=FuelType.PETROL,
        transmission=TransmissionType.MANUAL,
        price=7500,
        description="Véhicule non publié.",
        status=VehicleStatus.AVAILABLE,
        is_featured=False,
        is_published=False,
    )
    session.add(v)
    session.commit()
    session.refresh(v)
    return v


@pytest.fixture(name="part")
def part_fixture(session):
    p = Part(
        title="Alternateur Peugeot 308",
        category="Electricité",
        brand="Peugeot",
        compatible_models="308, 3008",
        condition=PartCondition.USED_GOOD,
        price=85,
        description="Alternateur d'occasion testé.",
        status=PartStatus.AVAILABLE,
        is_featured=True,
        is_published=True,
    )
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


@pytest.fixture(name="service")
def service_fixture(session):
    s = Service(
        title="Vidange",
        short_description="Vidange toutes marques",
        full_description="Vidange moteur + filtre à huile pour toutes marques.",
        display_order=1,
        is_active=True,
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


@pytest.fixture(name="unpublished_service")
def unpublished_service_fixture(session):
    s = Service(
        title="Vidange",
        short_description="Vidange toutes marques",
        full_description="Vidange moteur + filtre à huile pour toutes marques.",
        display_order=1,
        is_active=False,
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s
