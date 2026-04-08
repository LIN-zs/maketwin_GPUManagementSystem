from django.db import models

# Create your models here.
from django.db import models

class GPU(models.Model):
    STATUS_CHOICES = (
        ('idle', '空闲'),
        ('occupied', '占用中'),
        ('maintenance', '维护中'),
    )
    gpu_index = models.IntegerField(unique=True, help_text='显卡编号1-8')
    name = models.CharField(max_length=20, help_text='显卡名称')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idle')
    description = models.TextField(blank=True, help_text='描述信息')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gpus'
        verbose_name = '显卡'
        verbose_name_plural = '显卡'

    def __str__(self):
        return f"GPU-{self.gpu_index} ({self.name})"

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('expired', '已过期'),
        ('cancelled', '已取消'),
    )
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='申请人')
    gpu = models.ForeignKey(GPU, on_delete=models.CASCADE, verbose_name='显卡')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approver = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_reservations', verbose_name='审批人')
    remark = models.TextField(blank=True, verbose_name='备注/拒绝理由')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservations'
        verbose_name = '预约申请'
        verbose_name_plural = '预约申请'
        indexes = [
            models.Index(fields=['gpu', 'start_time', 'end_time']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'start_time']),
        ]

    def __str__(self):
        return f"{self.user.username} 预约 {self.gpu} ({self.start_time}~{self.end_time})"