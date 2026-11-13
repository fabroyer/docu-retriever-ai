from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ["id", "original_name", "status", "file", "uploaded_at"]
        read_only_fields = ["id", "original_name", "status", "file", "uploaded_at"]

    def validate_file(selfself, value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("File must be PDF.")
        max_size = 20 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError("File too large.")
        return value

    def create(self, validated_data):
        uploaded_file = validated_data["file"]
        validated_data["original_name"] = uploaded_file.name
        return super().create(validated_data)