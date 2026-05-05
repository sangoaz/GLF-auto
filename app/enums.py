"""Fichier pour déterminer les structures de données"""

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"


class VehicleStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"
    RESERVED = "RESERVED"


class PartStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"
    RESERVED = "RESERVED"


class FuelType(str, Enum):
    PETROL = "PETROL"  # Essence
    DIESEL = "DIESEL"  # Diesel
    HYBRID = "HYBRID"  # Hybride classique
    PLUG_IN_HYBRID = "PLUG_IN_HYBRID"  # Hybride rechargeable
    ELECTRIC = "ELECTRIC"  # Electrique
    LPG = "LPG"  # GPL
    CNG = "CNG"  # Gaz naturel


class TransmissionType(str, Enum):
    MANUAL = "MANUAL"  # Boite manuelle
    AUTOMATIC = "AUTOMATIC"  # Boite auto classique
    SEMI_AUTOMATIC = "SEMI_AUTOMATIC"  # Robotisée / palettes


class PartCondition(str, Enum):
    NEW = "NEW"
    USED_GOOD = "USED_GOOD"
    USED_FAIR = "USED_FAIR"
    FOR_PARTS = "FOR_PARTS"
