from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from courses.models import Course


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00
    )

    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["status", "deadline", "-created_at"]

    def save(self, *args, **kwargs):
        if self.status == "completed" and self.completed_at is None:
            self.completed_at = timezone.now()

        if self.status != "completed":
            self.completed_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title