from rest_framework import serializers
from .models import Submission
from users.serializers import UserSerializer
from requests.serializers import RequestSerializer

class SubmissionSerializer(serializers.ModelSerializer):
    """제출물 기본 정보"""
    creator = UserSerializer(read_only=True)
    request = RequestSerializer(read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id',
            'request',
            'creator',
            'original_video',
            'preview_video',
            'thumbnail',
            'description',
            'is_paid',
            'show_in_portfolio',  # 추가!
            'submitted_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'creator', 'is_paid', 'preview_video', 'thumbnail', 'submitted_at', 'updated_at']


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """제출물 생성 (영상 업로드)"""
    
    class Meta:
        model = Submission
        fields = [
            'request',
            'original_video',
            'description',
            'show_in_portfolio',  # 추가!
        ]
    
    def validate_request(self, value):
        """의뢰 상태 검증 - open OR in_progress 가능"""
        if value.status not in ['open', 'in_progress']:  # 수정!
            raise serializers.ValidationError("완료된 의뢰에는 제출할 수 없습니다.")
        return value
    
    def validate(self, data):
        """본인 의뢰에는 제출 불가"""
        request_obj = data.get('request')
        user = self.context['request'].user
        
        if request_obj.requester == user:
            raise serializers.ValidationError("본인이 올린 의뢰에는 제출할 수 없습니다.")
        
        # 특정 사용자 의뢰인 경우 검증
        if request_obj.request_type == 'specific':
            if request_obj.target_user != user:
                raise serializers.ValidationError("이 의뢰는 특정 사용자만 제출할 수 있습니다.")
        
        return data
    
    def create(self, validated_data):
        """제출물 생성"""
        validated_data['creator'] = self.context['request'].user
        submission = super().create(validated_data)
        
        # 의뢰 상태를 '진행중'으로 변경 (open일 경우에만)
        if submission.request.status == 'open':
            submission.request.status = 'in_progress'
            submission.request.save()
        
        return submission


class SubmissionListSerializer(serializers.ModelSerializer):
    """제출물 목록용 (간단)"""
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    request_title = serializers.CharField(source='request.title', read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id',
            'request',
            'request_title',
            'creator_username',
            'thumbnail',
            'is_paid',
            'show_in_portfolio',
            'submitted_at',
        ]