from rest_framework import serializers
from .models import Request
from users.serializers import UserSerializer

class RequestSerializer(serializers.ModelSerializer):
    """의뢰 기본 정보"""
    requester = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()
    
    class Meta:
        model = Request
        fields = [
            'id',
            'requester',
            'is_mine',
            'title',
            'concept',
            'style',
            'duration',
            'purpose',
            'request_type',
            'target_user',
            'reward',
            'status',
            'is_anonymous',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'requester', 'status', 'created_at', 'updated_at']
    
    def get_requester(self, obj):
        """익명이면 의뢰자 정보 숨기기"""
        if getattr(obj, 'is_anonymous', False):
            return {
                'id': None,
                'username': '익명',
                'email': '',
            }
        return UserSerializer(obj.requester).data
    
    def get_is_mine(self, obj):
        """본인의 의뢰인지 확인"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.requester == request.user
        return False


class RequestCreateSerializer(serializers.ModelSerializer):
    """의뢰 생성용"""
    
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
            'is_anonymous',
        ]
    
    def validate_reward(self, value):
        """보상은 최소 100 코인 이상"""
        if value < 100:
            raise serializers.ValidationError("보상은 최소 100 코인 이상이어야 합니다.")
        return value
    
    def validate(self, attrs):
        """특정 사용자 지정 시 target_user 필수"""
        if attrs.get('request_type') == 'specific' and not attrs.get('target_user'):
            raise serializers.ValidationError({
                'target_user': '특정 사용자 타입일 경우 대상 사용자를 지정해야 합니다.'
            })
        return attrs
    
    def create(self, validated_data):
        """의뢰 생성 시 requester는 현재 로그인 유저"""
        validated_data['requester'] = self.context['request'].user
        return super().create(validated_data)