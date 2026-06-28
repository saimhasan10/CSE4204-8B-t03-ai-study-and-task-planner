from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def course_list_create(request):
    if request.method == "GET":
        courses = Course.objects.filter(user=request.user)
        serializer = CourseSerializer(courses, many=True)

        return Response({
            "status": "success",
            "count": courses.count(),
            "courses": serializer.data,
        })

    serializer = CourseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)

        return Response({
            "status": "success",
            "message": "Course created successfully",
            "course": serializer.data,
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "error",
        "errors": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def course_detail(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        user=request.user
    )

    if request.method == "GET":
        serializer = CourseSerializer(course)

        return Response({
            "status": "success",
            "course": serializer.data,
        })

    if request.method in ["PUT", "PATCH"]:
        serializer = CourseSerializer(
            course,
            data=request.data,
            partial=request.method == "PATCH"
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "Course updated successfully",
                "course": serializer.data,
            })

        return Response({
            "status": "error",
            "errors": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    course.delete()

    return Response({
        "status": "success",
        "message": "Course deleted successfully",
    }, status=status.HTTP_200_OK)