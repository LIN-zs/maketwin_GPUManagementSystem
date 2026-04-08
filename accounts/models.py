from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', '普通用户'),
        ('admin', '管理员'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    max_concurrent_reservations = models.IntegerField(default=2, help_text='最大同时预约数量')
    sudo_enabled = models.BooleanField(default=False, help_text='当前是否拥有sudo权限')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username