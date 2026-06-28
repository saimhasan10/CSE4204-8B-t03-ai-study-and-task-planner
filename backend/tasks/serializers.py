from rest_framework import serializers

from courses.models import Course
from .models import Task


class CourseBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "code"]


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    course = CourseBriefSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "course",
            "course_id",
            "title",
            "description",
            "deadline",
            "priority",
            "status",
            "estimated_hours",
            "completed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "course",
            "completed_at",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Task title is required.")

        return value

    def validate_estimated_hours(self, value):
        if value < 0:
            raise serializers.ValidationError("Estimated hours cannot be negative.")

        return value

    def validate(self, data):
        request = self.context.get("request")

        if self.instance is None and "course_id" not in data:
            raise serializers.ValidationError({
                "course_id": "Course ID is required."
            })

        course_id = data.get("course_id")

        if course_id:
            course_exists = Course.objects.filter(
                id=course_id,
                user=request.user
            ).exists()

            if not course_exists:
                raise serializers.ValidationError({
                    "course_id": "Invalid course ID."
                })

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        course_id = validated_data.pop("course_id")

        course = Course.objects.get(
            id=course_id,
            user=request.user
        )

        task = Task.objects.create(
            user=request.user,
            course=course,
            **validated_data
        )

        return task

    def update(self, instance, validated_data):
        request = self.context.get("request")
        course_id = validated_data.pop("course_id", None)

        if course_id:
            instance.course = Course.objects.get(
                id=course_id,
                user=request.user
            )

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance