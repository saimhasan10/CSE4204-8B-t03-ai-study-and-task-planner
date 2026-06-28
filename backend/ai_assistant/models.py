from django.db import models
from django.contrib.auth.models import User


class SavedAIPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ("study_plan", "Study Plan"),
        ("priority", "Priority Suggestion"),
        ("task_breakdown", "Task Breakdown"),
        ("chat", "AI Chat"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_ai_plans"
    )
    title = models.CharField(max_length=200)
    plan_type = models.CharField(
        max_length=50,
        choices=PLAN_TYPE_CHOICES,
        default="study_plan"
    )
    prompt = models.TextField(blank=True)
    content = models.JSONField(default=dict)
    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title