from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import HTTPException, UploadFile


ALLOWED_IMAGE_EXTENSIOS = {".jpg", ".jpeg", ".png", ".webp"}
UPLOAD_DIR = Path("uploads")


# Fonction d'enregistrement de fichiers en local
def save_uploaded_image(file: UploadFile, subfolder: str) -> str:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Fichier invalide")

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_IMAGE_EXTENSIOS:
        raise HTTPException(status_code=400, detail="Format d'image non supporté")

    target_dir = UPLOAD_DIR / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    unique_filename = f"{uuid4().hex}{extension}"
    file_path = target_dir / unique_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/uploads/{subfolder}/{unique_filename}"


# Fonction de suppression de fichiers en local
def delete_uploaded_file(file_url: str) -> None:
    """
    Supprime un fichier stocké localement à partir de son URL publique.
    Exemple: /uploads/vehicles/abc123.jpg
    """
    if not file_url.startswith("/uploads/"):
        return

    relative_path = file_url.removeprefix("/uploads/")
    file_path = UPLOAD_DIR / relative_path

    if file_path.exists() and file_path.is_file():
        file_path.unlink()
