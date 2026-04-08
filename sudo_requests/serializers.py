# sudo_requests/serializers.py
from rest_framework import serializers
from .models import SudoRequest

class SudoRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SudoRequest
        fields = ['id', 'reason', 'valid_until']
        read_only_fields = ['id', 'status']

class SudoRequestListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    approver = serializers.StringRelatedField()
    class Meta:
        model = SudoRequest
        fields = '__all__'