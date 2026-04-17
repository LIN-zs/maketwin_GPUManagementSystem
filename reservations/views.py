from django.shortcuts import render
# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Reservation, GPU
from .serializers import ReservationCreateSerializer, ReservationListSerializer, GPUListSerializer
from .services import check_conflict, auto_approve_reservation
from system_integration.utils import notify_gpu_update
class GPUListView(generics.ListAPIView):
    queryset = GPU.objects.all()
    serializer_class = GPUListSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReservationCreateView(generics.CreateAPIView):
    serializer_class = ReservationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        reservation = serializer.save(user=self.request.user, status='pending')
        success, msg = auto_approve_reservation(reservation)   # 内部会修改状态并保存
        # 可以打印日志记录 success 和 msg，便于调试

class MyReservationListView(generics.ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by('-created_at')

class AllReservationListView(generics.ListAPIView):
    """公共日历视图：展示所有已批准的预约"""
    serializer_class = ReservationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(status='approved').order_by('start_time')

# reservations/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Reservation
from .serializers import ReservationListSerializer
from .permissions import IsAdmin
from .services import check_conflict

class PendingReservationListView(generics.ListAPIView):
    """管理员查看所有待审批的预约"""
    serializer_class = ReservationListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    def get_queryset(self):
        return Reservation.objects.filter(status='pending').order_by('start_time')

class ApproveReservationView(generics.UpdateAPIView):
    """管理员批准预约"""
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = ReservationListSerializer

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.status != 'pending':
            return Response({'error': '只能审批待审批的预约'}, status=status.HTTP_400_BAD_REQUEST)
        # 再次检查冲突（避免在等待期间被其他预约占用）
        if check_conflict(reservation.gpu_id, reservation.start_time, reservation.end_time, exclude_id=reservation.id):
            return Response({'error': '时间段已被其他预约占用'}, status=status.HTTP_400_BAD_REQUEST)
        reservation.status = 'approved'
        reservation.approver = request.user
        reservation.approved_at = timezone.now()
        reservation.save()
        notify_gpu_update(action='approved', gpu_id=reservation.gpu_id)
        # TODO: 调用系统权限修改函数，将用户加入GPU组
        return Response({'status': 'approved'})

class RejectReservationView(generics.UpdateAPIView):
    """管理员拒绝预约"""
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = ReservationListSerializer

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.status != 'pending':
            return Response({'error': '只能拒绝待审批的预约'}, status=status.HTTP_400_BAD_REQUEST)
        reservation.status = 'rejected'
        reservation.approver = request.user
        reservation.remark = request.data.get('remark', '')
        reservation.save()
        notify_gpu_update(action='rejected', gpu_id=reservation.gpu_id)
        return Response({'status': 'rejected'})

