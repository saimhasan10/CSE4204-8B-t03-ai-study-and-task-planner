from rest_framework import serializers
from .models import SavedAIPlan


class SavedAIPlanSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SavedAIPlan
        fields = [
            "id",
            "user",
            "title",
            "plan_type",
            "prompt",
            "content",
            "is_archived",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Title is required.")

        return value