from datetime import timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


def get_user_tasks(user):
    return Task.objects.filter(user=user).select_related("course")


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def task_list_create(request):
    if request.method == "GET":
        tasks = get_user_tasks(request.user)
        serializer = TaskSerializer(tasks, many=True)

        return Response({
            "status": "success",
            "count": tasks.count(),
            "tasks": serializer.data,
        })

    serializer = TaskSerializer(
        data=request.data,
        context={"request": request}
    )

    if serializer.is_valid():
        task = serializer.save()

        return Response({
            "status": "success",
            "message": "Task created successfully",
            "task": TaskSerializer(task).data,
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "error",
        "errors": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "GET":
        serializer = TaskSerializer(task)

        return Response({
            "status": "success",
            "task": serializer.data,
        })

    if request.method in ["PUT", "PATCH"]:
        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=request.method == "PATCH",
            context={"request": request}
        )

        if serializer.is_valid():
            updated_task = serializer.save()

            return Response({
                "status": "success",
                "message": "Task updated successfully",
                "task": TaskSerializer(updated_task).data,
            })

        return Response({
            "status": "error",
            "errors": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    task.delete()

    return Response({
        "status": "success",
        "message": "Task deleted successfully",
    }, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_filter(request):
    tasks = get_user_tasks(request.user)

    status_filter = request.query_params.get("status")
    priority = request.query_params.get("priority")
    course_id = request.query_params.get("course_id")
    search = request.query_params.get("search")
    overdue = request.query_params.get("overdue")
    upcoming_days = request.query_params.get("upcoming_days")

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    if priority:
        tasks = tasks.filter(priority=priority)

    if course_id:
        tasks = tasks.filter(course_id=course_id)

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(course__title__icontains=search)
        )

    if overdue == "true":
        tasks = tasks.filter(
            deadline__lt=timezone.now()
        ).exclude(status="completed")

    if upcoming_days:
        try:
            days = int(upcoming_days)
            now = timezone.now()
            tasks = tasks.filter(
                deadline__gte=now,
                deadline__lte=now + timedelta(days=days)
            )
        except ValueError:
            pass

    serializer = TaskSerializer(tasks, many=True)

    return Response({
        "status": "success",
        "count": tasks.count(),
        "tasks": serializer.data,
    })