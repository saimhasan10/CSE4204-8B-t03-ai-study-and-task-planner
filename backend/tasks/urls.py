from django.urls import path

from .views import (
    task_list_create,
    task_detail,
    task_filter,
)


urlpatterns = [
    path("", task_list_create, name="task-list-create"),
    path("filter/", task_filter, name="task-filter"),
    path("<int:task_id>/", task_detail, name="task-detail"),
]