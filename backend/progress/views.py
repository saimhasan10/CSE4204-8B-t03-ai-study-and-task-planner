from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course
from tasks.models import Task


def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "course": {
            "id": task.course.id,
            "title": task.course.title,
            "code": task.course.code,
        },
        "priority": task.priority,
        "status": task.status,
        "deadline": task.deadline,
        "estimated_hours": task.estimated_hours,
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def progress_overview(request):
    user = request.user
    now = timezone.now()

    courses = Course.objects.filter(user=user)
    tasks = Task.objects.filter(user=user).select_related("course")

    total_courses = courses.count()
    total_tasks = tasks.count()

    completed_tasks = tasks.filter(status="completed").count()
    pending_tasks = tasks.filter(status="pending").count()
    in_progress_tasks = tasks.filter(status="in_progress").count()

    overdue_tasks = tasks.filter(
        deadline__lt=now
    ).exclude(status="completed").count()

    upcoming_tasks = tasks.filter(
        deadline__gte=now,
        deadline__lte=now + timedelta(days=7)
    ).exclude(status="completed").count()

    completion_rate = 0

    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 2)

    status_summary = {
        "pending": pending_tasks,
        "in_progress": in_progress_tasks,
        "completed": completed_tasks,
    }

    priority_summary = {
        "low": tasks.filter(priority="low").count(),
        "medium": tasks.filter(priority="medium").count(),
        "high": tasks.filter(priority="high").count(),
        "urgent": tasks.filter(priority="urgent").count(),
    }

    course_progress = []

    for course in courses:
        course_tasks = tasks.filter(course=course)

        course_total = course_tasks.count()
        course_completed = course_tasks.filter(status="completed").count()
        course_pending = course_tasks.filter(status="pending").count()
        course_in_progress = course_tasks.filter(status="in_progress").count()

        course_completion_rate = 0

        if course_total > 0:
            course_completion_rate = round((course_completed / course_total) * 100, 2)

        course_progress.append({
            "course_id": course.id,
            "course_title": course.title,
            "course_code": course.code,
            "total_tasks": course_total,
            "completed_tasks": course_completed,
            "pending_tasks": course_pending,
            "in_progress_tasks": course_in_progress,
            "completion_rate": course_completion_rate,
        })

    weekly_completion = []

    for i in range(6, -1, -1):
        day = (now - timedelta(days=i)).date()

        completed_count = tasks.filter(
            status="completed",
            completed_at__date=day
        ).count()

        weekly_completion.append({
            "date": str(day),
            "completed_tasks": completed_count,
        })

    upcoming_deadlines = tasks.filter(
        deadline__gte=now
    ).exclude(status="completed").order_by("deadline")[:5]

    recent_tasks = tasks.order_by("-updated_at")[:5]

    return Response({
        "status": "success",
        "summary": {
            "total_courses": total_courses,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "overdue_tasks": overdue_tasks,
            "upcoming_tasks_next_7_days": upcoming_tasks,
            "completion_rate": completion_rate,
        },
        "status_summary": status_summary,
        "priority_summary": priority_summary,
        "course_progress": course_progress,
        "weekly_completion": weekly_completion,
        "upcoming_deadlines": [
            serialize_task(task) for task in upcoming_deadlines
        ],
        "recent_tasks": [
            serialize_task(task) for task in recent_tasks
        ],
    })