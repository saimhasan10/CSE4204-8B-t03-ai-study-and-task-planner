from django.urls import path

from .views import (
    ai_home,
    generate_study_plan,
    suggest_priority,
    breakdown_task,
    ai_chat,
    saved_plans,
    saved_plan_detail,
)


urlpatterns = [
    path("", ai_home, name="ai-home"),
    path("study-plan/", generate_study_plan, name="generate-study-plan"),
    path("priority/", suggest_priority, name="suggest-priority"),
    path("task-breakdown/", breakdown_task, name="task-breakdown"),
    path("chat/", ai_chat, name="ai-chat"),
    path("plans/", saved_plans, name="saved-plans"),
    path("plans/<int:plan_id>/", saved_plan_detail, name="saved-plan-detail"),
]