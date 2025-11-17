from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
import json
from .models import User


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            errors = self._validate_registration_data(data)
            if errors:
                return JsonResponse({
                    "success": False, 
                    "errors": errors
                }, status=400)
            
        
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                phone=data.get('phone', ''),
                is_active=False  
            )
            
        
            confirm_code = user.generate_confirm_code()
            
            return JsonResponse({
                "success": True,
                "message": "Пользователь успешно создан. Подтвердите аккаунт с помощью кода.",
                "username": user.username,
                "confirm_code": confirm_code 
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "error": "Invalid JSON"
            }, status=400)
    
    def _validate_registration_data(self, data):
        errors = {}
        
        if not data.get('username'):
            errors['username'] = 'Username обязателен'
        elif User.objects.filter(username=data['username']).exists():
            errors['username'] = 'Пользователь с таким именем уже существует'
        
        if not data.get('email'):
            errors['email'] = 'Email обязателен'
        elif User.objects.filter(email=data['email']).exists():
            errors['email'] = 'Пользователь с таким email уже существует'
        
        if not data.get('password'):
            errors['password'] = 'Пароль обязателен'
        elif len(data['password']) < 6:
            errors['password'] = 'Пароль должен содержать минимум 6 символов'
        elif data.get('password') != data.get('password_confirm'):
            errors['password_confirm'] = 'Пароли не совпадают'
        
        return errors


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({
                    "success": False,
                    "error": "Необходимо указать username и password"
                }, status=400)
            
            user = authenticate(username=username, password=password)
            
            if user:
                if not user.is_active:
                    return JsonResponse({
                        "success": False,
                        "error": "Аккаунт не подтвержден. Подтвердите аккаунт с помощью кода."
                    }, status=400)
                
                login(request, user)
                
                return JsonResponse({
                    "success": True,
                    "message": "Успешный вход в систему",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                })
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Неверные учетные данные"
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "error": "Invalid JSON"
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ConfirmUserView(View):
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            confirm_code = data.get('confirm_code')
            
            if not username or not confirm_code:
                return JsonResponse({
                    "success": False,
                    "error": "Необходимо указать username и confirm_code"
                }, status=400)
            
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "error": "Пользователь не найден"
                }, status=400)
            
            if user.is_active:
                return JsonResponse({
                    "success": False,
                    "error": "Аккаунт уже подтвержден"
                }, status=400)
            
            if user.confirm_account(confirm_code):
                return JsonResponse({
                    "success": True,
                    "message": "Аккаунт успешно подтвержден! Теперь вы можете войти в систему."
                })
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Неверный код подтверждения"
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "error": "Invalid JSON"
            }, status=400)