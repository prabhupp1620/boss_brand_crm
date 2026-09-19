"""Pluggable file storage — local disk in development, an S3-compatible
bucket in production. Selected by the STORAGE_BACKEND config value; both
backends expose the same save()/delete()/owns() so app/uploads.py (and
everything above it) never needs to know which one is active.
"""
import os

from flask import current_app


class LocalStorage:
    """Saves under UPLOAD_FOLDER, served back out by the /uploads/<subdir>/<file> route."""

    def save(self, file_storage, subdir: str, filename: str) -> str:
        folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subdir)
        os.makedirs(folder, exist_ok=True)
        file_storage.save(os.path.join(folder, filename))
        return f"/uploads/{subdir}/{filename}"

    def owns(self, url: str) -> bool:
        return bool(url) and url.startswith("/uploads/")

    def delete(self, url: str) -> None:
        if not self.owns(url):
            return
        subdir, _, filename = url.split("/uploads/", 1)[-1].rpartition("/")
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], subdir, filename)
        try:
            os.remove(path)
        except OSError:
            pass


class S3Storage:
    """Saves to an S3-compatible bucket — AWS S3, DigitalOcean Spaces, MinIO, etc.

    Configure via S3_BUCKET, S3_REGION, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY.
    S3_ENDPOINT_URL is only needed for non-AWS S3-compatible services.
    S3_PUBLIC_BASE_URL overrides the returned URL's domain (e.g. a CDN in
    front of the bucket) — leave blank to use the bucket's own URL.
    """

    def _client(self):
        import boto3  # lazy: local dev never needs boto3 installed

        return boto3.client(
            "s3",
            region_name=current_app.config.get("S3_REGION") or None,
            endpoint_url=current_app.config.get("S3_ENDPOINT_URL") or None,
            aws_access_key_id=current_app.config.get("S3_ACCESS_KEY_ID") or None,
            aws_secret_access_key=current_app.config.get("S3_SECRET_ACCESS_KEY") or None,
        )

    def _base_url(self) -> str:
        base = current_app.config.get("S3_PUBLIC_BASE_URL")
        if base:
            return base.rstrip("/")
        bucket = current_app.config["S3_BUCKET"]
        endpoint = current_app.config.get("S3_ENDPOINT_URL")
        if endpoint:
            return f"{endpoint.rstrip('/')}/{bucket}"
        return f"https://{bucket}.s3.{current_app.config.get('S3_REGION')}.amazonaws.com"

    def save(self, file_storage, subdir: str, filename: str) -> str:
        bucket = current_app.config["S3_BUCKET"]
        key = f"{subdir}/{filename}"
        self._client().upload_fileobj(
            file_storage.stream,
            bucket,
            key,
            ExtraArgs={
                "ContentType": file_storage.mimetype or "application/octet-stream",
                "ACL": "public-read",
            },
        )
        return f"{self._base_url()}/{key}"

    def owns(self, url: str) -> bool:
        return bool(url) and url.startswith(self._base_url() + "/")

    def delete(self, url: str) -> None:
        if not self.owns(url):
            return
        key = url[len(self._base_url()) + 1:]
        try:
            self._client().delete_object(Bucket=current_app.config["S3_BUCKET"], Key=key)
        except Exception:
            pass


def get_storage():
    backend = current_app.config.get("STORAGE_BACKEND", "local")
    return S3Storage() if backend == "s3" else LocalStorage()
