from django.shortcuts import render

# Create your views here.
# sudo_requests/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import SudoRequest
from .serializers import SudoRequestCreateSerializer, SudoRequestListSerializer
from reservations.permissions import IsAdmin

class SudoRequestCreateView(generics.CreateAPIView):
    serializer_class = SudoRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')

class MySudoRequestListView(generics.ListAPIView):
    serializer_class = SudoRequestListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SudoRequest.objects.filter(user=self.request.user).order_by('-created_at')

class PendingSudoRequestListView(generics.ListAPIView):
    serializer_class = SudoRequestListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return SudoRequest.objects.filter(status='pending').order_by('created_at')

class ApproveSudoRequestView(generics.UpdateAPIView):
    queryset = SudoRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = SudoRequestListSerializer

    def update(self, request, *args, **kwargs):
        sudo_req = self.get_object()
        if sudo_req.status != 'pending':
            return Response({'error': '只能审批待审批的申请'}, status=status.HTTP_400_BAD_REQUEST)
        sudo_req.status = 'approved'
        sudo_req.approver = request.user
        sudo_req.approved_at = timezone.now()
        # 设置有效期（默认7天，前端可传）
        valid_days = request.data.get('valid_days', 7)
        sudo_req.valid_until = timezone.now() + timezone.timedelta(days=valid_days)
        sudo_req.save()
        # 更新用户的 sudo_enabled 字段
        sudo_req.user.sudo_enabled = True
        sudo_req.user.save()
        # TODO: 调用系统命令实际赋予sudo权限
        return Response({'status': 'approved', 'valid_until': sudo_req.valid_until})

class RejectSudoRequestView(generics.UpdateAPIView):
    queryset = SudoRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = SudoRequestListSerializer

    def update(self, request, *args, **kwargs):
        sudo_req = self.get_object()
        if sudo_req.status != 'pending':
            return Response({'error': '只能拒绝待审批的申请'}, status=status.HTTP_400_BAD_REQUEST)
        sudo_req.status = 'rejected'
        sudo_req.approver = request.user
        sudo_req.save()
        return Response({'status': 'rejected'})