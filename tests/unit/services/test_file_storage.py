"""Tests unitaires : app/services/file_storage.py (Supabase)"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services.file_storage import save_uploaded_image, delete_uploaded_file


def make_upload_file(content_type: str, filename: str = "photo.jpg"):
    mock_file = MagicMock()
    mock_file.content_type = content_type
    mock_file.filename = filename
    mock_file.file = MagicMock()
    mock_file.file.read.return_value = b"fake image content"
    return mock_file


def make_supabase_mock(
    public_url="https://supabase.co/storage/v1/object/public/bucket/vehicles/abc.jpg",
):
    mock_supabase = MagicMock()
    mock_bucket = MagicMock()
    mock_supabase.storage.from_.return_value = mock_bucket
    mock_bucket.get_public_url.return_value = public_url
    return mock_supabase, mock_bucket


# ──────────────────────────────────────────
# Tests : save_uploaded_image
# ──────────────────────────────────────────


class TestSaveUploadedImage:
    def test_content_type_invalide_leve_400(self):
        file = make_upload_file("application/pdf")
        with pytest.raises(HTTPException) as exc_info:
            save_uploaded_image(file, "vehicles")
        assert exc_info.value.status_code == 400

    def test_message_erreur_content_type_invalide(self):
        file = make_upload_file("application/pdf")
        with pytest.raises(HTTPException) as exc_info:
            save_uploaded_image(file, "vehicles")
        assert "autorisé" in exc_info.value.detail.lower()

    @pytest.mark.parametrize(
        "content_type,expected_ext",
        [
            ("image/jpeg", ".jpg"),
            ("image/png", ".png"),
            ("image/webp", ".webp"),
        ],
    )
    def test_content_types_valides_acceptes(self, content_type, expected_ext):
        file = make_upload_file(content_type)
        mock_supabase, mock_bucket = make_supabase_mock(
            f"https://supabase.co/storage/v1/object/public/bucket/vehicles/abc{expected_ext}"
        )

        with patch("app.services.file_storage.supabase", mock_supabase):
            result = save_uploaded_image(file, "vehicles")

        assert result.endswith(expected_ext)

    def test_retourne_url_publique_supabase(self):
        file = make_upload_file("image/jpeg")
        expected_url = (
            "https://supabase.co/storage/v1/object/public/bucket/vehicles/abc.jpg"
        )
        mock_supabase, mock_bucket = make_supabase_mock(expected_url)

        with patch("app.services.file_storage.supabase", mock_supabase):
            result = save_uploaded_image(file, "vehicles")

        assert result == expected_url

    def test_upload_appelle_supabase_storage(self):
        file = make_upload_file("image/jpeg")
        mock_supabase, mock_bucket = make_supabase_mock()

        with patch("app.services.file_storage.supabase", mock_supabase):
            save_uploaded_image(file, "vehicles")

        mock_bucket.upload.assert_called_once()

    def test_deux_uploads_ont_des_chemins_differents(self):
        file1 = make_upload_file("image/jpeg")
        file2 = make_upload_file("image/jpeg")
        mock_supabase, mock_bucket = make_supabase_mock()

        paths = []

        def capture_upload(path, file, file_options):
            paths.append(path)

        mock_bucket.upload.side_effect = capture_upload

        with patch("app.services.file_storage.supabase", mock_supabase):
            save_uploaded_image(file1, "vehicles")
            save_uploaded_image(file2, "vehicles")

        assert paths[0] != paths[1]

    def test_chemin_contient_le_subfolder(self):
        file = make_upload_file("image/jpeg")
        mock_supabase, mock_bucket = make_supabase_mock()
        captured = {}

        def capture_upload(path, file, file_options):
            captured["path"] = path

        mock_bucket.upload.side_effect = capture_upload

        with patch("app.services.file_storage.supabase", mock_supabase):
            save_uploaded_image(file, "vehicles")

        assert captured["path"].startswith("vehicles/")


# ──────────────────────────────────────────
# Tests : delete_uploaded_file
# ──────────────────────────────────────────


class TestDeleteUploadedFile:
    def test_supprime_fichier_existant(self):
        mock_supabase, mock_bucket = make_supabase_mock()
        url = "https://supabase.co/storage/v1/object/public/GLF-images/vehicles/abc.jpg"

        with patch("app.services.file_storage.supabase", mock_supabase), patch(
            "app.services.file_storage.settings"
        ) as mock_settings:
            mock_settings.SUPABASE_BUCKET = "GLF-images"
            delete_uploaded_file(url)

        mock_bucket.remove.assert_called_once_with(["vehicles/abc.jpg"])

    def test_ne_plante_pas_si_url_invalide(self):
        """Une URL sans le marqueur Supabase ne doit pas lever d'exception."""
        mock_supabase, _ = make_supabase_mock()

        with patch("app.services.file_storage.supabase", mock_supabase), patch(
            "app.services.file_storage.settings"
        ) as mock_settings:
            mock_settings.SUPABASE_BUCKET = "GLF-images"
            delete_uploaded_file("https://autre-domaine.com/image.jpg")

    def test_ne_plante_pas_si_supabase_echoue(self):
        """Si Supabase lève une exception, la fonction doit l'avaler silencieusement."""
        mock_supabase, mock_bucket = make_supabase_mock()
        mock_bucket.remove.side_effect = Exception("Supabase error")
        url = "https://supabase.co/storage/v1/object/public/GLF-images/vehicles/abc.jpg"

        with patch("app.services.file_storage.supabase", mock_supabase), patch(
            "app.services.file_storage.settings"
        ) as mock_settings:
            mock_settings.SUPABASE_BUCKET = "GLF-images"
            delete_uploaded_file(url)  # ne doit pas lever d'exception
