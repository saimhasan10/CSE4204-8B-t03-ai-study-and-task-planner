from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "user",
            "title",
            "code",
            "instructor",
            "credit_hours",
            "semester",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Course title is required.")

        return value