from rest_framework import serializers
from .models import Document
from django.contrib.auth.models import User
from rest_framework import serializers


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "extracted_text",
            "uploaded_at"
        ]
        read_only_fields = [
            "extracted_text",
            "uploaded_at"
        ]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user