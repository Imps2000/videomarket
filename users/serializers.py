from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """사용자 기본 정보"""
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'coins',
            'completed_requests',
            'total_earnings',
            'profile_image',
            'bio',
        ]
        read_only_fields = ['id', 'coins', 'completed_requests', 'total_earnings']


class RegisterSerializer(serializers.ModelSerializer):
    """회원가입"""
    password = serializers.CharField(write_only=True, min_length=4)
    password2 = serializers.CharField(write_only=True, min_length=4)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, data):
        """비밀번호 확인"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data
    
    def create(self, validated_data):
        """사용자 생성"""
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """로그인"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """로그인 검증"""
        from django.contrib.auth import authenticate
        
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        
        if user is None:
            raise serializers.ValidationError("아이디 또는 비밀번호가 잘못되었습니다.")
        
        if not user.is_active:
            raise serializers.ValidationError("비활성화된 계정입니다.")
        
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }