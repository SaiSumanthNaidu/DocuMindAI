from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document

        fields = [
            "id",
            "title",
            "file",
            "extracted_text",
            "structured_data",
            "uploaded_at"
        ]

        read_only_fields = [
            "extracted_text",
            "structured_data",
            "uploaded_at"
        ]