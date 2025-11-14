from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserConfirmSerializer
)


class RegisterView(APIView):
    """
    Регистрация нового пользователя
    """
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": True,
                "message": "Пользователь успешно создан. Подтвердите аккаунт с помощью кода.",
                "username": user.username,
                "confirm_code": user.confirm_code  # В продакшене убрать!
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Авторизация пользователя
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                "success": True,
                "message": "Успешный вход в систему",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            })
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ConfirmUserView(APIView):
    """
    Подтверждение пользователя по коду
    """
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.save():
                return Response({
                    "success": True,
                    "message": "Аккаунт успешно подтвержден! Теперь вы можете войти в систему."
                })
            else:
                return Response({
                    "success": False,
                    "error": "Ошибка подтверждения аккаунта"
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)