from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True)
    instructor = models.CharField(max_length=150, blank=True)
    credit_hours = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=3.0
    )
    semester = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title