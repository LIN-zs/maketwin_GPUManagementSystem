# sudo_requests/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.SudoRequestCreateView.as_view(), name='sudo-create'),
    path('my/', views.MySudoRequestListView.as_view(), name='sudo-my'),
    path('admin/pending/', views.PendingSudoRequestListView.as_view(), name='sudo-admin-pending'),
    path('admin/approve/<int:pk>/', views.ApproveSudoRequestView.as_view(), name='sudo-admin-approve'),
    path('admin/reject/<int:pk>/', views.RejectSudoRequestView.as_view(), name='sudo-admin-reject'),
]