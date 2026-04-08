from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import GPU, Reservation

User = get_user_model()

class ReservationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.login(username='test', password='test123')
        self.gpu = GPU.objects.create(gpu_index=1, name='A100')

    def test_create_reservation(self):
        data = {
            'gpu': self.gpu.id,
            'start_time': '2025-05-10T10:00:00Z',
            'end_time': '2025-05-10T12:00:00Z'
        }
        response = self.client.post('/api/reservations/reservations/create/', data, format='json')
        self.assertEqual(response.status_code, 201)  # 确保创建成功
        self.assertIn('status', response.data)  # 确保有 status 字段
        self.assertEqual(response.data['status'], 'approved')