from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'sudo_enabled': user.sudo_enabled,
                'max_concurrent_reservations': user.max_concurrent_reservations,
            })
        return Response({'error': '用户名或密码错误'}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': '已登出'})

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'sudo_enabled': user.sudo_enabled,
            'max_concurrent_reservations': user.max_concurrent_reservations,
        })