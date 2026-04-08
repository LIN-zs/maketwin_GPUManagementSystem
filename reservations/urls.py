from django.urls import path
from . import views

urlpatterns = [
    path('gpus/', views.GPUListView.as_view(), name='gpu-list'),
    path('reservations/create/', views.ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/my/', views.MyReservationListView.as_view(), name='my-reservations'),
    path('reservations/all/', views.AllReservationListView.as_view(), name='all-reservations'),
    path('admin/pending/', views.PendingReservationListView.as_view(), name='admin-pending'),
    path('admin/approve/<int:pk>/', views.ApproveReservationView.as_view(), name='admin-approve'),
    path('admin/reject/<int:pk>/', views.RejectReservationView.as_view(), name='admin-reject'),
]
