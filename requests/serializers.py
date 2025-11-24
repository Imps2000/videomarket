from rest_framework import serializers
from .models import Request
from users.serializers import UserSerializer

class RequestSerializer(serializers.ModelSerializer):
    """의뢰 기본 정보"""
    requester = UserSerializer(read_only=True)
    requester_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Request
        fields = [
            'id',
            'requester',
            'requester_id',
            'title',
            'concept',
            'style',
            'duration',
            'purpose',
            'request_type',
            'target_user',
            'reward',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'requester', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """의뢰 생성 시 requester는 현재 로그인 유저"""
        validated_data['requester'] = self.context['request'].user
        return super().create(validated_data)


class RequestCreateSerializer(serializers.ModelSerializer):
    """의뢰 생성용 (간단)"""
    
    class Meta:
        model = Request
        fields = [
            'title',
            'concept',
            'style',
            'duration',
            'purpose',
            'request_type',
            'target_user',
            'reward',
        ]
    
    def validate_reward(self, value):
        """보상 최소값 검증"""
        if value < 100:
            raise serializers.ValidationError("보상은 최소 100 코인 이상이어야 합니다.")
        return value
    
    def validate(self, data):
        """특정 사용자 지정 시 검증"""
        if data.get('request_type') == 'specific' and not data.get('target_user'):
            raise serializers.ValidationError("특정 사용자 의뢰는 target_user를 지정해야 합니다.")
        return data