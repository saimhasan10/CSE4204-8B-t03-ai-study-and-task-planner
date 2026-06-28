from datetime import timedelta
from math import ceil

from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.models import Task
from .models import SavedAIPlan
from .serializers import SavedAIPlanSerializer
from .gemini_service import call_gemini, extract_json_from_text


def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "course": {
            "id": task.course.id,
            "title": task.course.title,
            "code": task.course.code,
        },
        "description": task.description,
        "deadline": task.deadline.isoformat() if task.deadline else None,
        "priority": task.priority,
        "status": task.status,
        "estimated_hours": float(task.estimated_hours),
    }


def get_task_context(user):
    tasks = Task.objects.filter(
        user=user
    ).exclude(
        status="completed"
    ).select_related("course")

    return [serialize_task(task) for task in tasks]


def fallback_study_plan(duration_days, daily_hours, task_context):
    schedule = []

    for day_index in range(duration_days):
        date = timezone.now().date() + timedelta(days=day_index)
        selected_tasks = task_context[day_index:day_index + 2]

        if not selected_tasks and task_context:
            selected_tasks = task_context[:2]

        schedule.append({
            "day": day_index + 1,
            "date": str(date),
            "target_study_hours": daily_hours,
            "tasks": selected_tasks,
        })

    return {
        "duration_days": duration_days,
        "daily_hours": daily_hours,
        "strategy": [
            "Start with urgent and high priority tasks.",
            "Break large tasks into small study sessions.",
            "Review completed work at the end of each day.",
        ],
        "schedule": schedule,
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ai_home(request):
    return Response({
        "status": "success",
        "message": "AI Assistant API is working",
        "endpoints": {
            "study_plan": "/api/ai/study-plan/",
            "priority": "/api/ai/priority/",
            "task_breakdown": "/api/ai/task-breakdown/",
            "chat": "/api/ai/chat/",
            "saved_plans": "/api/ai/plans/",
        }
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_study_plan(request):
    duration_days = int(request.data.get("duration_days", 7))
    daily_hours = float(request.data.get("daily_hours", 2))
    focus_course_ids = request.data.get("focus_course_ids", [])
    save_plan = request.data.get("save", False)

    duration_days = max(1, min(duration_days, 30))
    daily_hours = max(0.5, min(daily_hours, 12))

    tasks = Task.objects.filter(
        user=request.user
    ).exclude(
        status="completed"
    ).select_related("course")

    if focus_course_ids:
        tasks = tasks.filter(course_id__in=focus_course_ids)

    task_context = [serialize_task(task) for task in tasks]

    prompt = f"""
You are an academic study planner assistant.

Create a realistic study plan for a university student.

Student task data:
{task_context}

Rules:
- Duration: {duration_days} days
- Daily study hours: {daily_hours}
- Prioritize urgent deadlines and high priority tasks
- Keep the plan practical
- Return ONLY valid JSON
- Do not add markdown

JSON format:
{{
  "duration_days": {duration_days},
  "daily_hours": {daily_hours},
  "strategy": ["string"],
  "schedule": [
    {{
      "day": 1,
      "date": "YYYY-MM-DD",
      "target_study_hours": {daily_hours},
      "tasks": [
        {{
          "task_id": 1,
          "task_title": "string",
          "course": "string",
          "priority": "string",
          "suggested_time_hours": 1.5,
          "focus_note": "string"
        }}
      ]
    }}
  ]
}}
"""

    gemini_response = call_gemini(prompt)
    plan = None
    ai_source = "fallback"

    if gemini_response["success"]:
        plan = extract_json_from_text(gemini_response["text"])
        ai_source = "gemini"

    if plan is None:
        plan = fallback_study_plan(duration_days, daily_hours, task_context)

    saved_plan = None

    if save_plan:
        saved_plan = SavedAIPlan.objects.create(
            user=request.user,
            title=f"{duration_days}-Day Study Plan",
            plan_type="study_plan",
            prompt=prompt,
            content=plan,
        )

    return Response({
        "status": "success",
        "message": "Study plan generated successfully",
        "ai_source": ai_source,
        "gemini_error": gemini_response["error"],
        "plan": plan,
        "saved_plan_id": saved_plan.id if saved_plan else None,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suggest_priority(request):
    task_context = get_task_context(request.user)

    prompt = f"""
You are an academic task priority assistant.

Analyze these student tasks:
{task_context}

Return ONLY valid JSON.
Do not add markdown.

JSON format:
{{
  "suggestions": [
    {{
      "task_id": 1,
      "task_title": "string",
      "priority_score": 8.5,
      "suggested_action": "string",
      "reason": "string"
    }}
  ]
}}
"""

    gemini_response = call_gemini(prompt)
    result = None
    ai_source = "fallback"

    if gemini_response["success"]:
        result = extract_json_from_text(gemini_response["text"])
        ai_source = "gemini"

    if result is None:
        suggestions = []

        priority_weight = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "urgent": 4,
        }

        now = timezone.now()

        for task in Task.objects.filter(user=request.user).exclude(status="completed"):
            score = priority_weight.get(task.priority, 2)

            if task.deadline:
                hours_left = (task.deadline - now).total_seconds() / 3600

                if hours_left < 0:
                    score += 4
                elif hours_left <= 24:
                    score += 3
                elif hours_left <= 72:
                    score += 2
                elif hours_left <= 168:
                    score += 1

            suggestions.append({
                "task_id": task.id,
                "task_title": task.title,
                "priority_score": round(score, 2),
                "suggested_action": "Do this task earlier" if score >= 5 else "Schedule normally",
                "reason": "Based on deadline, priority, and current status."
            })

        result = {
            "suggestions": sorted(
                suggestions,
                key=lambda item: item["priority_score"],
                reverse=True
            )
        }

    return Response({
        "status": "success",
        "message": "Priority suggestion generated successfully",
        "ai_source": ai_source,
        "gemini_error": gemini_response["error"],
        "suggestions": result.get("suggestions", []),
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def breakdown_task(request):
    task_id = request.data.get("task_id")

    if not task_id:
        return Response({
            "status": "error",
            "message": "task_id is required",
        }, status=status.HTTP_400_BAD_REQUEST)

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task_data = serialize_task(task)

    prompt = f"""
You are an academic task breakdown assistant.

Break this task into smaller practical steps:
{task_data}

Return ONLY valid JSON.
Do not add markdown.

JSON format:
{{
  "task": {{
    "id": {task.id},
    "title": "{task.title}"
  }},
  "total_steps": 5,
  "steps": [
    {{
      "step_no": 1,
      "title": "string",
      "estimated_time_hours": 1.0,
      "instruction": "string"
    }}
  ],
  "final_tip": "string"
}}
"""

    gemini_response = call_gemini(prompt)
    breakdown = None
    ai_source = "fallback"

    if gemini_response["success"]:
        breakdown = extract_json_from_text(gemini_response["text"])
        ai_source = "gemini"

    if breakdown is None:
        estimated_hours = float(task.estimated_hours)
        step_count = max(3, min(6, ceil(estimated_hours)))

        steps = []

        for index in range(step_count):
            steps.append({
                "step_no": index + 1,
                "title": f"Step {index + 1} for {task.title}",
                "estimated_time_hours": round(estimated_hours / step_count, 2),
                "instruction": "Complete this part before moving to the next step."
            })

        breakdown = {
            "task": {
                "id": task.id,
                "title": task.title,
            },
            "total_steps": step_count,
            "steps": steps,
            "final_tip": "Finish the hardest step first and keep the last step for review."
        }

    return Response({
        "status": "success",
        "message": "Task breakdown generated successfully",
        "ai_source": ai_source,
        "gemini_error": gemini_response["error"],
        "breakdown": breakdown,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ai_chat(request):
    message = request.data.get("message", "").strip()

    if not message:
        return Response({
            "status": "error",
            "message": "Message is required",
        }, status=status.HTTP_400_BAD_REQUEST)

    task_context = get_task_context(request.user)

    prompt = f"""
You are an academic AI assistant for a student.

Student message:
{message}

Current pending task data:
{task_context}

Give a helpful, short, practical answer.
Do not mention that you are an AI model.
"""

    gemini_response = call_gemini(prompt)
    ai_source = "fallback"

    if gemini_response["success"] and gemini_response["text"]:
        reply = gemini_response["text"]
        ai_source = "gemini"
    else:
        total_tasks = Task.objects.filter(user=request.user).count()
        pending_tasks = Task.objects.filter(user=request.user, status="pending").count()
        completed_tasks = Task.objects.filter(user=request.user, status="completed").count()

        reply = (
            f"You asked: {message}. "
            f"You currently have {total_tasks} total tasks, "
            f"{pending_tasks} pending tasks, and {completed_tasks} completed tasks. "
            f"Focus on urgent deadlines first and keep your daily study plan realistic."
        )

    return Response({
        "status": "success",
        "message": "AI chat response generated successfully",
        "ai_source": ai_source,
        "gemini_error": gemini_response["error"],
        "reply": reply,
    })


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def saved_plans(request):
    if request.method == "GET":
        plans = SavedAIPlan.objects.filter(user=request.user)
        serializer = SavedAIPlanSerializer(plans, many=True)

        return Response({
            "status": "success",
            "count": plans.count(),
            "plans": serializer.data,
        })

    serializer = SavedAIPlanSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)

        return Response({
            "status": "success",
            "message": "AI plan saved successfully",
            "plan": serializer.data,
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "error",
        "errors": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def saved_plan_detail(request, plan_id):
    plan = get_object_or_404(
        SavedAIPlan,
        id=plan_id,
        user=request.user
    )

    if request.method == "GET":
        serializer = SavedAIPlanSerializer(plan)

        return Response({
            "status": "success",
            "plan": serializer.data,
        })

    if request.method == "PATCH":
        serializer = SavedAIPlanSerializer(
            plan,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "message": "AI plan updated successfully",
                "plan": serializer.data,
            })

        return Response({
            "status": "error",
            "errors": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    plan.delete()

    return Response({
        "status": "success",
        "message": "AI plan deleted successfully",
    })