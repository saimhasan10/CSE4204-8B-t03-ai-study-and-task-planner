from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        "status": "success",
        "message": "AI Study and Task Planner backend is running"
    })


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/health/", health_check, name="health-check"),

    path("api/accounts/", include("accounts.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/tasks/", include("tasks.urls")),
    path("api/progress/", include("progress.urls")),
    path("api/ai/", include("ai_assistant.urls")),
]