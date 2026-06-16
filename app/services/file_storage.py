from uuid import uuid4
from pathlib import Path
from fastapi import UploadFile, HTTPException
from supabase import create_client

import magic

from app.core.config import settings


ALLOWED_IMAGE_TYPES = {
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/jpeg": ".jpeg",
    "image/webp": ".webp",
}


supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY,
)


def save_uploaded_image(file: UploadFile, subfolder: str) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Format d'image non autorisé. Utilisez JPG, PNG ou WEBP.",
        )

    content = file.file.read()

    # On vérifie le vrai type du fichier
    # magic.from_buffer() lit les premiers octets du fichier
    # et retourne le vrai MIME type, indépendamment de ce que le client a déclaré
    real_type = magic.from_buffer(content, mime=True)
    if real_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Le contenu du fichier ne correspond pas à son type déclaré."
        )

    extension = ALLOWED_IMAGE_TYPES[file.content_type]
    filename = f"{uuid4()}{extension}"
    storage_path = f"{subfolder}/{filename}"


    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        path=storage_path,
        file=content,
        file_options={
            "content-type": file.content_type,
            "cache-control": "3600",
            "upsert": "false",
        },
    )

    public_url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(
        storage_path
    )

    return public_url


def delete_uploaded_file(file_url: str) -> None:
    """
    Supprime une image Supabase Storage à partir de son URL publique.
    """
    try:
        marker = f"/storage/v1/object/public/{settings.SUPABASE_BUCKET}/"
        storage_path = file_url.split(marker)[1]

        supabase.storage.from_(settings.SUPABASE_BUCKET).remove([storage_path])
    except Exception:
        # On évite de casser toute la route si la suppression du fichier échoue.
        pass
