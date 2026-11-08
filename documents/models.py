from django.db import models

class Document(models.Model):
    """
    Represent a document uploaded by a user.
    Store the original filename, file location, upload timestamp and processing  status.
    """

    class Status(models.TextChoices):
        """Track the document's processing status."""
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        INDEXED = "indexed", "Indexed"
        FAILED = "failed", "Failed"

    original_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPLOADED,
    )

    # Store the uploaded file.
    file = models.FileField(
        upload_to="documents/%Y/%m/%d/",
    )

    # Record the document upload date and time.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the original filename."""
        return self.original_name