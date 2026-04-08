from django.utils import timezone
from .models import Reservation




def check_conflict(gpu_id, start_time, end_time, exclude_id=None):
    qs = Reservation.objects.filter(
        gpu_id=gpu_id,
        status__in=['pending', 'approved'],
        start_time__lt=end_time,
        end_time__gt=start_time,
    )
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    return qs.exists()




def auto_approve_reservation(reservation):
    # 并发检查：查询已批准且未结束的预约（不包括当前预约，因为还未批准）
    active_reservations = Reservation.objects.filter(
        user=reservation.user,
        status='approved',
        end_time__gt=timezone.now()
    ).count()
    if active_reservations >= reservation.user.max_concurrent_reservations:
        return False, "超出最大并发预约数量"

    # 冲突检查：排除当前预约自身（因为它的状态还是 pending）
    if check_conflict(reservation.gpu_id, reservation.start_time, reservation.end_time, exclude_id=reservation.id):
        return False, "时间段与现有预约冲突"

    # 自动批准
    reservation.status = 'approved'
    reservation.approver = None
    reservation.approved_at = timezone.now()
    reservation.save()
    return True, "自动批准成功"