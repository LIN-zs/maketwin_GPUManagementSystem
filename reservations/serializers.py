from rest_framework import serializers
from .models import Reservation, GPU
from accounts.models import User

class GPUListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = ['id', 'gpu_index', 'name', 'status']

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'gpu', 'start_time', 'end_time', 'remark', 'status']  # 加入 status
        read_only_fields = ['id', 'status']  # status 只读

    def validate(self, data):
        # 基础时间校验
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("结束时间必须晚于开始时间")
        # 其他校验（如冲突检测）将在视图中进行
        return data

class ReservationListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    gpu = serializers.StringRelatedField()
    class Meta:
        model = Reservation
        fields = '__all__'