from django.db import models

# Create your models here.
from django.db import models



class SudoRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('expired', '已过期'),
    )
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='申请人')
    reason = models.TextField(verbose_name='申请理由')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    valid_from = models.DateTimeField(null=True, blank=True, verbose_name='生效时间')
    valid_until = models.DateTimeField(null=True, blank=True, verbose_name='失效时间')
    approver = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_sudo_requests', verbose_name='审批人')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        db_table = 'sudo_requests'
        verbose_name = 'Sudo权限申请'
        verbose_name_plural = 'Sudo权限申请'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'valid_until']),
        ]

    def __str__(self):
        return f"{self.user.username} 申请 sudo 权限 ({self.status})"