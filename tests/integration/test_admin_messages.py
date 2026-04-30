"""Tests d'intégration : routes admin messages (contact + reprise)"""

import pytest
from fastapi.testclient import TestClient
from app.models.contact_request import ContactRequest
from app.models.trade_in_request import TradeInRequest


def create_contact(session, name="Jean Dupont", email="jean@dupont.fr", is_read=False):
    cr = ContactRequest(
        name=name,
        email=email,
        phone="0601020304",
        subject="Test",
        message="Message de test",
        is_read=is_read,
    )
    session.add(cr)
    session.commit()
    session.refresh(cr)
    return cr


def create_trade_in(session, name="Marie Martin", is_read=False):
    tr = TradeInRequest(
        name=name,
        email="marie@martin.fr",
        phone="0607080910",
        brand="Renault",
        model="Clio",
        year=2015,
        mileage=120000,
        condition_note="Bon état",
        message="Message de test",
        is_read=is_read,
    )
    session.add(tr)
    session.commit()
    session.refresh(tr)
    return tr


# ──────────────────────────────────────────
# Tests : GET /admin/contact-requests
# ──────────────────────────────────────────

class TestListContactRequests:
    def test_liste_vide(self, client: TestClient, auth_headers):
        response = client.get("/admin/contact-requests", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_liste_avec_demandes(self, client: TestClient, auth_headers, session):
        create_contact(session, name="Jean")
        create_contact(session, name="Marie")

        response = client.get("/admin/contact-requests", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_non_authentifie(self, client: TestClient):
        response = client.get("/admin/contact-requests")
        assert response.status_code == 401


class TestGetContactRequest:
    def test_get_existant(self, client: TestClient, auth_headers, session):
        cr = create_contact(session)
        response = client.get(f"/admin/contact-requests/{cr.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "jean@dupont.fr"

    def test_get_inexistant(self, client: TestClient, auth_headers):
        response = client.get("/admin/contact-requests/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, session):
        cr = create_contact(session)
        response = client.get(f"/admin/contact-requests/{cr.id}")
        assert response.status_code == 401


class TestPatchContactRequest:
    def test_marquer_comme_lu(self, client: TestClient, auth_headers, session):
        cr = create_contact(session, is_read=False)

        response = client.patch(
            f"/admin/contact-requests/{cr.id}",
            json={"is_read": True},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["is_read"] is True

    def test_patch_inexistant(self, client: TestClient, auth_headers):
        response = client.patch(
            "/admin/contact-requests/99999",
            json={"is_read": True},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, session):
        cr = create_contact(session)
        response = client.patch(
            f"/admin/contact-requests/{cr.id}",
            json={"is_read": True},
        )
        assert response.status_code == 401


# ──────────────────────────────────────────
# Tests : GET /admin/trade-in-requests
# ──────────────────────────────────────────

class TestListTradeInRequests:
    def test_liste_vide(self, client: TestClient, auth_headers):
        response = client.get("/admin/trade-in-requests", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_liste_avec_demandes(self, client: TestClient, auth_headers, session):
        create_trade_in(session, name="Jean")
        create_trade_in(session, name="Marie")

        response = client.get("/admin/trade-in-requests", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_non_authentifie(self, client: TestClient):
        response = client.get("/admin/trade-in-requests")
        assert response.status_code == 401


class TestGetTradeInRequest:
    def test_get_existant(self, client: TestClient, auth_headers, session):
        tr = create_trade_in(session)
        response = client.get(f"/admin/trade-in-requests/{tr.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["brand"] == "Renault"

    def test_get_inexistant(self, client: TestClient, auth_headers):
        response = client.get("/admin/trade-in-requests/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, session):
        tr = create_trade_in(session)
        response = client.get(f"/admin/trade-in-requests/{tr.id}")
        assert response.status_code == 401


class TestPatchTradeInRequest:
    def test_marquer_comme_lu(self, client: TestClient, auth_headers, session):
        tr = create_trade_in(session, is_read=False)

        response = client.patch(
            f"/admin/trade-in-requests/{tr.id}",
            json={"is_read": True},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["is_read"] is True

    def test_patch_inexistant(self, client: TestClient, auth_headers):
        response = client.patch(
            "/admin/trade-in-requests/99999",
            json={"is_read": True},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_non_authentifie(self, client: TestClient, session):
        tr = create_trade_in(session)
        response = client.patch(
            f"/admin/trade-in-requests/{tr.id}",
            json={"is_read": True},
        )
        assert response.status_code == 401
