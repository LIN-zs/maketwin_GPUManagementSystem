"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginView, LogoutView, UserInfoView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/reservations/', include('reservations.urls')),
    path('api/sudo/', include('sudo_requests.urls')),
    path('api/auth/login/', LoginView.as_view()),
    path('api/auth/logout/', LogoutView.as_view()),
    path('api/auth/me/', UserInfoView.as_view()),
    path('', lambda request: redirect('/static/index.html')),   # 根路径重定向
]
from rest_framework.urls import path as drf_path
urlpatterns += [
    drf_path('api-auth/', include('rest_framework.urls')),  # 提供登录/登出
]

