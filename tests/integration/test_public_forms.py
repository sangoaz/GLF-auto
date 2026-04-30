"""Tests d'intégration : routes publiques contact et reprise"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


CONTACT_PAYLOAD = {
    "name": "Jean Dupont",
    "email": "jean@dupont.fr",
    "phone": "0601020304",
    "subject": "Demande de renseignement",
    "message": "Bonjour, je souhaite avoir des infos sur la Peugeot 308.",
}

TRADE_IN_PAYLOAD = {
    "name": "Marie Martin",
    "email": "marie@martin.fr",
    "phone": "0607080910",
    "brand": "Renault",
    "model": "Clio",
    "year": 2015,
    "mileage": 120000,
    "condition_note": "Bon état général, quelques rayures",
    "message": "Je souhaite connaitre la valeur de reprise de mon vehicule.",
}


# ──────────────────────────────────────────
# Tests : POST /contact
# ──────────────────────────────────────────

class TestCreateContactRequest:
    def test_creation_succes(self, client: TestClient):
        with patch("app.routes.public_contact.send_contact_notification"):
            response = client.post("/contact", json=CONTACT_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Jean Dupont"
        assert data["email"] == "jean@dupont.fr"
        assert data["subject"] == "Demande de renseignement"
        assert data["is_read"] is False

    def test_creation_sans_email_invalide(self, client: TestClient):
        payload = {**CONTACT_PAYLOAD, "email": "pas_un_email"}
        with patch("app.routes.public_contact.send_contact_notification"):
            response = client.post("/contact", json=payload)
        assert response.status_code == 422

    def test_creation_champs_manquants(self, client: TestClient):
        response = client.post("/contact", json={"name": "Incomplet"})
        assert response.status_code == 422

    def test_email_envoye_apres_creation(self, client: TestClient):
        with patch("app.routes.public_contact.send_contact_notification") as mock_send:
            client.post("/contact", json=CONTACT_PAYLOAD)
        mock_send.assert_called_once()

    def test_echec_email_ne_bloque_pas_creation(self, client: TestClient):
        """Si l'envoi d'email échoue, la demande doit quand même être créée."""
        with patch("app.routes.public_contact.send_contact_notification", side_effect=Exception("SMTP error")):
            response = client.post("/contact", json=CONTACT_PAYLOAD)
        assert response.status_code == 201

    def test_demande_enregistree_en_base(self, client: TestClient, session):
        from app.models.contact_request import ContactRequest
        from sqlmodel import select

        with patch("app.routes.public_contact.send_contact_notification"):
            client.post("/contact", json=CONTACT_PAYLOAD)

        requests = session.exec(select(ContactRequest)).all()
        assert len(requests) == 1
        assert requests[0].email == "jean@dupont.fr"


# ──────────────────────────────────────────
# Tests : POST /trade-in
# ──────────────────────────────────────────

class TestCreateTradeInRequest:
    def test_creation_succes(self, client: TestClient):
        with patch("app.routes.public_trade_in.send_trade_in_notification"):
            response = client.post("/trade-in", json=TRADE_IN_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Marie Martin"
        assert data["brand"] == "Renault"
        assert data["model"] == "Clio"
        assert data["is_read"] is False

    def test_creation_champs_manquants(self, client: TestClient):
        response = client.post("/trade-in", json={"name": "Incomplet"})
        assert response.status_code == 422

    def test_email_envoye_apres_creation(self, client: TestClient):
        with patch("app.routes.public_trade_in.send_trade_in_notification") as mock_send:
            client.post("/trade-in", json=TRADE_IN_PAYLOAD)
        mock_send.assert_called_once()

    def test_echec_email_ne_bloque_pas_creation(self, client: TestClient):
        """Si l'envoi d'email échoue, la demande doit quand même être créée."""
        with patch("app.routes.public_trade_in.send_trade_in_notification", side_effect=Exception("SMTP error")):
            response = client.post("/trade-in", json=TRADE_IN_PAYLOAD)
        assert response.status_code == 201

    def test_demande_enregistree_en_base(self, client: TestClient, session):
        from app.models.trade_in_request import TradeInRequest
        from sqlmodel import select

        with patch("app.routes.public_trade_in.send_trade_in_notification"):
            client.post("/trade-in", json=TRADE_IN_PAYLOAD)

        requests = session.exec(select(TradeInRequest)).all()
        assert len(requests) == 1
        assert requests[0].brand == "Renault"
