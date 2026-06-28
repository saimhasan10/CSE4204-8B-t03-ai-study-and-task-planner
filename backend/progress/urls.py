from django.urls import path
from .views import progress_overview


urlpatterns = [
    path("", progress_overview, name="progress-overview"),
]