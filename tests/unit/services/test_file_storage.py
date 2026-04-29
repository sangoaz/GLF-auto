"""Tests unitaires : app/services/file_storage.py"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services.file_storage import save_uploaded_image, delete_uploaded_file


def make_upload_file(filename: str, content: bytes = b"fake image data"):
    """Helper pour créer un UploadFile mocké."""
    mock_file = MagicMock()
    mock_file.filename = filename
    mock_file.file = MagicMock()
    return mock_file


# ──────────────────────────────────────────
# Tests : save_uploaded_image
# ──────────────────────────────────────────


class TestSaveUploadedImage:
    def test_extension_invalide_leve_400(self):
        file = make_upload_file("document.pdf")
        with pytest.raises(HTTPException) as exc_info:
            save_uploaded_image(file, "vehicles")
        assert exc_info.value.status_code == 400
        assert "non supporté" in exc_info.value.detail.lower()

    def test_filename_vide_leve_400(self):
        file = make_upload_file("")
        with pytest.raises(HTTPException) as exc_info:
            save_uploaded_image(file, "vehicles")
        assert exc_info.value.status_code == 400
        assert "invalide" in exc_info.value.detail.lower()

    def test_filename_none_leve_400(self):
        file = make_upload_file(None)
        with pytest.raises(HTTPException) as exc_info:
            save_uploaded_image(file, "vehicles")
        assert exc_info.value.status_code == 400

    @pytest.mark.parametrize(
        "filename",
        [
            "photo.jpg",
            "photo.jpeg",
            "photo.png",
            "photo.webp",
        ],
    )
    def test_extensions_valides_acceptees(self, filename, tmp_path):
        """Toutes les extensions autorisées doivent être acceptées."""
        file = make_upload_file(filename)

        with patch("app.services.file_storage.UPLOAD_DIR", tmp_path), patch(
            "shutil.copyfileobj"
        ):
            result = save_uploaded_image(file, "vehicles")

        assert result.startswith("/uploads/vehicles/")
        ext = Path(filename).suffix.lower()
        assert result.endswith(ext)

    def test_retourne_un_chemin_unique(self, tmp_path):
        """Deux uploads du même fichier doivent retourner des chemins différents."""
        file1 = make_upload_file("photo.jpg")
        file2 = make_upload_file("photo.jpg")

        with patch("app.services.file_storage.UPLOAD_DIR", tmp_path), patch(
            "shutil.copyfileobj"
        ):
            path1 = save_uploaded_image(file1, "vehicles")
            path2 = save_uploaded_image(file2, "vehicles")

        assert path1 != path2

    def test_cree_le_sous_dossier_si_absent(self, tmp_path):
        file = make_upload_file("photo.jpg")

        with patch("app.services.file_storage.UPLOAD_DIR", tmp_path), patch(
            "shutil.copyfileobj"
        ):
            save_uploaded_image(file, "vehicles")

        assert (tmp_path / "vehicles").exists()


# ──────────────────────────────────────────
# Tests : delete_uploaded_file
# ──────────────────────────────────────────


class TestDeleteUploadedFile:
    def test_supprime_fichier_existant(self, tmp_path):
        # Créer un vrai fichier temporaire
        subfolder = tmp_path / "vehicles"
        subfolder.mkdir()
        fake_file = subfolder / "abc123.jpg"
        fake_file.write_bytes(b"fake")

        with patch("app.services.file_storage.UPLOAD_DIR", tmp_path):
            delete_uploaded_file("/uploads/vehicles/abc123.jpg")

        assert not fake_file.exists()

    def test_ignore_url_sans_prefix_uploads(self, tmp_path):
        """Une URL qui ne commence pas par /uploads/ doit être ignorée silencieusement."""
        with patch("app.services.file_storage.UPLOAD_DIR", tmp_path):
            delete_uploaded_file("/media/vehicles/abc123.jpg")  # ne doit pas planter

    def test_ignore_fichier_inexistant(self, tmp_path):
        """Supprimer un fichier qui n'existe pas ne doit pas planter."""
        with patch("app.services.file_storage.UPLOAD_DIR", tmp_path):
            delete_uploaded_file("/uploads/vehicles/inexistant.jpg")

    def test_ignore_si_cest_un_dossier(self, tmp_path):
        """Ne doit pas supprimer un dossier même si le chemin correspond."""
        subfolder = tmp_path / "vehicles"
        subfolder.mkdir()
        fake_dir = subfolder / "monrepertoire"
        fake_dir.mkdir()

        with patch("app.services.file_storage.UPLOAD_DIR", tmp_path):
            delete_uploaded_file("/uploads/vehicles/monrepertoire")

        assert fake_dir.exists()
