from distutils.command import upload

from django.db import models

class Document(models.Model):

    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        INDEXED = "indexed", "Indexed"
        FAILED = "failed", "Failed"

    original_name = models.Charfield(max_length=225)

    file = models.FileField(
        upload_to="documents/%Y/%m/%d",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPLOADED,
    )

    def __str__(self):
        return self.original_name