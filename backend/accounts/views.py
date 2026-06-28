from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def accounts_home(request):
    return Response({
        "status": "success",
        "message": "Accounts API is working",
        "endpoints": {
            "register": "/api/accounts/register/",
            "login": "/api/accounts/login/",
            "profile": "/api/accounts/profile/",
            "logout": "/api/accounts/logout/",
        }
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        return Response({
            "status": "success",
            "message": "User registered successfully",
            "user": UserProfileSerializer(user).data,
            "tokens": tokens,
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "error",
        "errors": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                "status": "error",
                "message": "Invalid username or password",
            }, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)

        return Response({
            "status": "success",
            "message": "Login successful",
            "user": UserProfileSerializer(user).data,
            "tokens": tokens,
        }, status=status.HTTP_200_OK)

    return Response({
        "status": "error",
        "errors": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if request.method == "GET":
        serializer = UserProfileSerializer(user)
        return Response({
            "status": "success",
            "user": serializer.data,
        })

    serializer = UserProfileSerializer(
        user,
        data=request.data,
        partial=request.method == "PATCH"
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "Profile updated successfully",
            "user": serializer.data,
        })

    return Response({
        "status": "error",
        "errors": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response({
            "status": "error",
            "message": "Refresh token is required",
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({
            "status": "success",
            "message": "Logout successful",
        }, status=status.HTTP_200_OK)

    except TokenError:
        return Response({
            "status": "error",
            "message": "Invalid or expired refresh token",
        }, status=status.HTTP_400_BAD_REQUEST)