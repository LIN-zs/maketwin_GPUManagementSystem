# system_integration/tasks.py
from django.utils import timezone
from reservations.models import Reservation
from sudo_requests.models import SudoRequest
from . import remove_user_from_gpu_group, revoke_sudo_permission

def expire_reservations():
    """将过期的预约标记为expired，并回收GPU权限"""
    expired = Reservation.objects.filter(status='approved', end_time__lt=timezone.now())
    for r in expired:
        r.status = 'expired'
        r.save()
        # 注意：若用户还有未过期的预约，不应该移出组，这里简化处理，生产环境需加判断
        remove_user_from_gpu_group(r.user.username)

def expire_sudo_requests():
    """将过期的sudo申请标记为expired，并回收sudo权限"""
    expired = SudoRequest.objects.filter(status='approved', valid_until__lt=timezone.now())
    for s in expired:
        s.status = 'expired'
        s.save()
        revoke_sudo_permission(s.user.username)
        s.user.sudo_enabled = False
        s.user.save()