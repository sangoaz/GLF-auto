"""Service d'envoie d'email"""

import os
import resend

from dotenv import load_dotenv

from app.models.contact_request import ContactRequest
from app.models.trade_in_request import TradeInRequest

load_dotenv()


resend.api_key = os.getenv("RESEND_API_KEY")

CONTACT_RECEIVER_EMAILS = os.getenv("CONTACT_RECEIVER_EMAILS", "")


def send_email(subject: str, body: str) -> None:
    if not resend.api_key:
        raise RuntimeError("Configuration Resend incomplète")

    recipients = [
        email.strip() for email in CONTACT_RECEIVER_EMAILS.split(",") if email.strip()
    ]

    if not recipients:
        raise RuntimeError("Aucun destinataire configuré")

    resend.Emails.send(
        {
            "from": "onboarding@resend.dev",
            "to": recipients,
            "subject": subject,
            "text": body,
        }
    )


def send_contact_notification(contact: ContactRequest) -> None:

    subject = f"Nouvelle demande de contact - {contact.subject}"

    body = f"""
Nouvelle demande de contact reçue depuis le site.

Nom : {contact.name}
Email : {contact.email}
Téléphone : {contact.phone}
Sujet : {contact.subject}

Message :
{contact.message}
"""

    send_email(subject=subject, body=body)


def send_trade_in_notification(trade_in: TradeInRequest) -> None:

    subject = f"Nouvelle demande de reprise - {trade_in.brand} {trade_in.model}"

    body = f"""
Nouvelle demande de reprise reçue depuis le site.

Nom : {trade_in.name}
Email : {trade_in.email}
Téléphone : {trade_in.phone}

Véhicule proposé :
Marque : {trade_in.brand}
Modèle : {trade_in.model}
Année : {trade_in.year}
Kilométrage : {trade_in.mileage} km
État général : {trade_in.condition_note}

Message :
{trade_in.message}
"""

    send_email(subject=subject, body=body)
