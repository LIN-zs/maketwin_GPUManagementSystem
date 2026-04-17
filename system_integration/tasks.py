# system_integration/tasks.py
from django.utils import timezone
from reservations.models import Reservation
from sudo_requests.models import SudoRequest
from . import remove_user_from_gpu_group, revoke_sudo_permission
from system_integration.utils import notify_gpu_update


def expire_reservations():
    expired = Reservation.objects.filter(status='approved', end_time__lt=timezone.now())
    gpu_ids = set()
    for r in expired:
        r.status = 'expired'
        r.save()
        remove_user_from_gpu_group(r.user.username)
        gpu_ids.add(r.gpu_id)

    # 对涉及的每个 GPU 发送更新通知
    for gpu_id in gpu_ids:
        notify_gpu_update(action='expired', gpu_id=gpu_id)




def expire_sudo_requests():
    """将过期的sudo申请标记为expired，并回收sudo权限"""
    expired = SudoRequest.objects.filter(status='approved', valid_until__lt=timezone.now())
    for s in expired:
        s.status = 'expired'
        s.save()
        revoke_sudo_permission(s.user.username)
        s.user.sudo_enabled = False
        s.user.save()