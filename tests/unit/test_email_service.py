"""Tests unitaires : app/services/email_service.py"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.email_service import (
    send_email,
    send_contact_notification,
    send_trade_in_notification,
)
from app.models.contact_request import ContactRequest
from app.models.trade_in_request import TradeInRequest

# ──────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────


@pytest.fixture
def contact():
    return ContactRequest(
        name="Jean Dupont",
        email="jean@dupont.fr",
        phone="0601020304",
        subject="Demande de renseignement",
        message="Bonjour, je voudrais des infos.",
        is_read=False,
    )


@pytest.fixture
def trade_in():
    return TradeInRequest(
        name="Marie Martin",
        email="marie@martin.fr",
        phone="0607080910",
        brand="Renault",
        model="Clio",
        year=2015,
        mileage=120000,
        condition_note="Bon état général",
        message="Combien pour ma voiture ?",
        is_read=False,
    )


SMTP_ENV = {
    "SMTP_HOST": "smtp.example.com",
    "SMTP_PORT": "587",
    "SMTP_USERNAME": "user@example.com",
    "SMTP_PASSWORD": "secret",
    "CONTACT_RECEIVER_EMAIL": "garage@glf.fr",
}


# ──────────────────────────────────────────
# Tests : send_email
# ──────────────────────────────────────────


class TestSendEmail:
    def test_envoie_email_avec_config_complete(self):
        with patch("app.services.email_service.resend.api_key", "re_test"), patch(
            "app.services.email_service.CONTACT_RECEIVER_EMAILS",
            "garage@glf.fr,admin@glf.fr",
        ), patch("app.services.email_service.resend.Emails.send") as mock_send:

            send_email("Sujet test", "Corps du message")

            mock_send.assert_called_once_with(
                {
                    "from": "onboarding@resend.dev",
                    "to": ["garage@glf.fr", "admin@glf.fr"],
                    "subject": "Sujet test",
                    "text": "Corps du message",
                }
            )

    def test_leve_erreur_si_config_incomplete(self):
        with patch("app.services.email_service.resend.api_key", None):
            with pytest.raises(RuntimeError) as exc_info:
                send_email("Sujet", "Corps")

            assert "Resend" in str(exc_info.value)

    def test_leve_erreur_si_receiver_manquant(self):
        with patch("app.services.email_service.resend.api_key", "re_test"), patch(
            "app.services.email_service.CONTACT_RECEIVER_EMAILS", ""
        ):
            with pytest.raises(RuntimeError) as exc_info:
                send_email("Sujet", "Corps")

            assert "destinataire" in str(exc_info.value)


# ──────────────────────────────────────────
# Tests : send_contact_notification
# ──────────────────────────────────────────


class TestSendContactNotification:
    def test_appelle_send_email(self, contact):
        with patch("app.services.email_service.send_email") as mock_send:
            send_contact_notification(contact)
            mock_send.assert_called_once()

    def test_sujet_contient_le_sujet_du_contact(self, contact):
        with patch("app.services.email_service.send_email") as mock_send:
            send_contact_notification(contact)
            subject = mock_send.call_args[1]["subject"]
            assert "Demande de renseignement" in subject

    def test_corps_contient_les_infos_du_contact(self, contact):
        with patch("app.services.email_service.send_email") as mock_send:
            send_contact_notification(contact)
            body = mock_send.call_args[1]["body"]
            assert "Jean Dupont" in body
            assert "jean@dupont.fr" in body
            assert "Bonjour, je voudrais des infos." in body


# ──────────────────────────────────────────
# Tests : send_trade_in_notification
# ──────────────────────────────────────────


class TestSendTradeInNotification:
    def test_appelle_send_email(self, trade_in):
        with patch("app.services.email_service.send_email") as mock_send:
            send_trade_in_notification(trade_in)
            mock_send.assert_called_once()

    def test_sujet_contient_marque_et_modele(self, trade_in):
        with patch("app.services.email_service.send_email") as mock_send:
            send_trade_in_notification(trade_in)
            subject = mock_send.call_args[1]["subject"]
            assert "Renault" in subject
            assert "Clio" in subject

    def test_corps_contient_les_infos_du_vehicule(self, trade_in):
        with patch("app.services.email_service.send_email") as mock_send:
            send_trade_in_notification(trade_in)
            body = mock_send.call_args[1]["body"]
            assert "Marie Martin" in body
            assert "Renault" in body
            assert "120000" in body
            assert "Bon état général" in body
