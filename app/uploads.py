import uuid

from .storage import get_storage

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def _extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def save_image(file_storage, subdir: str) -> str:
    """Save an uploaded image via the active storage backend, return its URL.

    Local dev writes to disk under UPLOAD_FOLDER; in production (STORAGE_BACKEND=s3)
    this instead uploads to the configured bucket. Callers never need to care which.
    """
    ext = _extension(file_storage.filename or "")
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Unsupported image type.")

    filename = f"{uuid.uuid4().hex}.{ext}"
    return get_storage().save(file_storage, subdir, filename)


def delete_upload(url: str) -> None:
    """Remove a previously uploaded file, wherever the active backend put it.

    A no-op for any URL the current backend doesn't recognize as its own
    (e.g. an external path an admin typed into the URL field by hand).
    """
    if not url:
        return
    get_storage().delete(url)
