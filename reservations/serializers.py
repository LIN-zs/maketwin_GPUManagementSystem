from rest_framework import serializers
from .models import Reservation, GPU
from accounts.models import User
from datetime import datetime, timedelta
class GPUListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = ['id', 'gpu_index', 'name', 'status']

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'gpu', 'start_time', 'end_time', 'remark', 'status']  # 加入 status
        read_only_fields = ['id', 'status']  # status 只读

    def to_internal_value(self, data):
        """打印原始请求数据"""
        print("\n" + "="*50)
        print("【序列化器接收到的原始数据】")
        print(data)
        internal_value = super().to_internal_value(data)
        print("\n【转换为Python对象后的数据（含外键对象）】")
        print(internal_value)
        return internal_value

    def validate(self, data):
        # 基础时间校验
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("结束时间必须晚于开始时间")
        # 其他校验（如冲突检测）将在视图中进行
        return data

    def create(self, validated_data):
        """打印即将存入数据库的数据"""
        print("\n【即将存入数据库的数据（validated_data）】")
        print(f"gpu: {validated_data['gpu']}")
        print(f"start_time: {validated_data['start_time']} (类型: {type(validated_data['start_time'])})")
        print(f"end_time: {validated_data['end_time']} (类型: {type(validated_data['end_time'])})")
        print(f"remark: {validated_data.get('remark', '')}")
        print("="*50 + "\n")
        return super().create(validated_data)

class ReservationListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    gpu = GPUListSerializer(read_only=True)   # 之前已改好
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
