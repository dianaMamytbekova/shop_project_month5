from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string


class User(AbstractUser):
    is_active = models.BooleanField(default=False)  # Неактивен до подтверждения
    confirm_code = models.CharField(
        max_length=6, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name="Код подтверждения"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def generate_confirm_code(self):
        """Генерация 6-значного рандомного кода"""
        while True:
            code = ''.join(random.choices(string.digits, k=6))
            if not User.objects.filter(confirm_code=code).exists():
                self.confirm_code = code
                self.save()
                return code
    
    def confirm_account(self, code):
        """Подтверждение аккаунта по коду"""
        if self.confirm_code == code:
            self.is_active = True
            self.confirm_code = None  # Удаляем код после подтверждения
            self.save()
            return True
        return False
    
    def save(self, *args, **kwargs):
        """Суперпользователи создаются активными"""
        if self.is_superuser or self.is_staff:
            self.is_active = True
            self.confirm_code = None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        db_table = 'product_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'