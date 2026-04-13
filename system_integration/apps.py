from django.apps import AppConfig


class SystemIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'system_integration'


    def ready(self):
        # ✅ 在 ready() 方法内部导入模型
        from django_q.models import Schedule
        # 避免重复创建（可选，但建议保留）
        if not Schedule.objects.filter(name='expire_reservations').exists():
            Schedule.objects.create(
                name='expire_reservations',
                func='system_integration.tasks.expire_reservations',
                schedule_type=Schedule.MINUTES,
                minutes=5,
                repeats=-1
            )
        if not Schedule.objects.filter(name='expire_sudo_requests').exists():
            Schedule.objects.create(
                name='expire_sudo_requests',
                func='system_integration.tasks.expire_sudo_requests',
                schedule_type=Schedule.MINUTES,
                minutes=5,
                repeats=-1
            )