from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    """평가 정보"""
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id',
            'submission',
            'reviewer',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """평가 작성"""
    
    class Meta:
        model = Review
        fields = ['submission', 'comment']
    
    def validate_submission(self, value):
        """제출물 검증"""
        user = self.context['request'].user
        
        # 의뢰자만 평가 가능
        if value.request.requester != user:
            raise serializers.ValidationError("본인이 올린 의뢰의 제출물만 평가할 수 있습니다.")
        
        # 결제 완료된 것만 평가 가능
        if not value.is_paid:
            raise serializers.ValidationError("결제 완료 후 평가할 수 있습니다.")
        
        # 이미 평가가 있는지 확인
        if hasattr(value, 'review'):
            raise serializers.ValidationError("이미 평가를 작성했습니다.")
        
        return value
    
    def create(self, validated_data):
        """평가 생성"""
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)