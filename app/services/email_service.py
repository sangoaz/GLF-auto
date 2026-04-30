"""Service d'envoie d'email"""

import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

from app.models.contact_request import ContactRequest
from app.models.trade_in_request import TradeInRequest

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CONTACT_RECEIVER_EMAIL = os.getenv("CONTACT_RECEIVER_EMAIL")


def send_email(subject: str, body: str) -> None:
    if not all([SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, CONTACT_RECEIVER_EMAIL]):
        raise RuntimeError("Configuration SMTP incomplète")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = SMTP_USERNAME
    message["To"] = CONTACT_RECEIVER_EMAIL
    message.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(message)


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
