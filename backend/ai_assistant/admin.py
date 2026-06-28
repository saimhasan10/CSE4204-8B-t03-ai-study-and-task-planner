from django.contrib import admin
from .models import SavedAIPlan


@admin.register(SavedAIPlan)
class SavedAIPlanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "plan_type",
        "user",
        "is_archived",
        "created_at",
    )
    list_filter = ("plan_type", "is_archived", "created_at")
    search_fields = ("title", "prompt", "user__username")
    ordering = ("-created_at",)