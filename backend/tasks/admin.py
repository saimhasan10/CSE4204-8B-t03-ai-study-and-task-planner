from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "course",
        "user",
        "priority",
        "status",
        "deadline",
        "estimated_hours",
        "completed_at",
        "created_at",
    )
    list_filter = ("priority", "status", "course", "created_at")
    search_fields = ("title", "description", "course__title", "user__username")
    ordering = ("status", "deadline", "-created_at")