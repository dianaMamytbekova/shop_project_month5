from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        min_length=6,
        style={'input_type': 'password'},
        label="Пароль"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}, 
        label="Подтверждение пароля"
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'phone')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }
    
    def validate(self, attrs):
        # Проверка совпадения паролей
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password_confirm": "Пароли не совпадают"
            })
        
        # Проверка уникальности email
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({
                "email": "Пользователь с таким email уже существует"
            })
        
        # Проверка уникальности username
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError({
                "username": "Пользователь с таким именем уже существует"
            })
        
        return attrs
    
    def create(self, validated_data):
        # Удаляем подтверждение пароля
        validated_data.pop('password_confirm')
        
        # Создаем пользователя с is_active=False
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            is_active=False  # Пользователь неактивен до подтверждения
        )
        
        # Генерируем и привязываем 6-значный код подтверждения
        confirm_code = user.generate_confirm_code()
        
        # В реальном приложении здесь отправляем код по email/SMS
        print(f"Код подтверждения для {user.username}: {confirm_code}")
        
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Имя пользователя")
    password = serializers.CharField(
        label="Пароль",
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            # Пытаемся найти пользователя
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError("Неверные учетные данные")
            
            # Проверяем пароль
            if not user.check_password(password):
                raise serializers.ValidationError("Неверные учетные данные")
            
            # Проверяем подтвержден ли аккаунт
            if not user.is_active:
                raise serializers.ValidationError(
                    "Аккаунт не подтвержден. Проверьте вашу почту для кода подтверждения."
                )
            
            # Аутентифицируем пользователя
            user = authenticate(username=username, password=password)
            if user:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError("Неверные учетные данные")
        else:
            raise serializers.ValidationError("Необходимо указать имя пользователя и пароль")


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(label="Имя пользователя")
    confirm_code = serializers.CharField(
        min_length=6, 
        max_length=6,
        label="Код подтверждения"
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        confirm_code = attrs.get('confirm_code')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "username": "Пользователь не найден"
            })
        
        # Проверяем, не подтвержден ли уже аккаунт
        if user.is_active:
            raise serializers.ValidationError("Аккаунт уже подтвержден")
        
        # Проверяем код подтверждения (один к одному)
        if user.confirm_code != confirm_code:
            raise serializers.ValidationError({
                "confirm_code": "Неверный код подтверждения"
            })
        
        attrs['user'] = user
        return attrs
    
    def save(self):
        user = self.validated_data['user']
        confirm_code = self.validated_data['confirm_code']
        return user.confirm_account(confirm_code)