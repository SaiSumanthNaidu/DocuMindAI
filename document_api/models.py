from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)

    file = models.FileField(
        upload_to="uploads/"
    )

    extracted_text = models.TextField(
        blank=True
    )

    structured_data = models.JSONField(
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title