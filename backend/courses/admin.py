from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "code",
        "user",
        "instructor",
        "credit_hours",
        "semester",
        "created_at",
    )
    list_filter = ("semester", "created_at")
    search_fields = ("title", "code", "instructor", "user__username")
    ordering = ("-created_at",)