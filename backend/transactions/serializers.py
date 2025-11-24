from rest_framework import serializers
from .models import Transaction
from submissions.models import Submission
from django.db import transaction as db_transaction

class TransactionSerializer(serializers.ModelSerializer):
    """거래 내역 조회"""
    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'amount',
            'transaction_type',
            'submission',
            'description',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']


class PurchaseSerializer(serializers.Serializer):
    """원본 구매"""
    submission_id = serializers.IntegerField()
    
    def validate_submission_id(self, value):
        """제출물 검증"""
        try:
            submission = Submission.objects.get(id=value)
        except Submission.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 제출물입니다.")
        
        user = self.context['request'].user
        
        # 본인 의뢰인지 확인
        if submission.request.requester != user:
            raise serializers.ValidationError("본인이 올린 의뢰의 제출물만 구매할 수 있습니다.")
        
        # 이미 구매했는지 확인
        if submission.is_paid:
            raise serializers.ValidationError("이미 구매한 제출물입니다.")
        
        # 잔액 확인
        reward = submission.request.reward
        if user.coins < reward:
            raise serializers.ValidationError(f"재화가 부족합니다. (필요: {reward}, 보유: {user.coins})")
        
        return value
    
    def create(self, validated_data):
        """구매 처리 (재화 거래)"""
        submission_id = validated_data['submission_id']
        submission = Submission.objects.get(id=submission_id)
        
        buyer = self.context['request'].user
        seller = submission.creator
        reward = submission.request.reward
        
        # DB 트랜잭션으로 묶기 (원자성 보장)
        with db_transaction.atomic():
            # 구매자 재화 차감
            buyer.coins -= reward
            buyer.save()
            
            # 판매자 재화 증가
            seller.coins += reward
            seller.total_earnings += reward
            seller.save()
            
            # 제출물 결제 완료 처리
            submission.is_paid = True
            submission.save()
            
            # 의뢰 상태 완료로 변경
            submission.request.status = 'completed'
            submission.request.save()
            
            # 구매자 통계 업데이트
            buyer.completed_requests += 1
            buyer.save()
            
            # 판매자 통계 업데이트
            seller.completed_requests += 1
            seller.save()
            
            # 거래 내역 저장 (구매자)
            Transaction.objects.create(
                user=buyer,
                amount=-reward,
                transaction_type='payment',
                submission=submission,
                description=f"원본 구매: {submission.request.title}"
            )
            
            # 거래 내역 저장 (판매자)
            Transaction.objects.create(
                user=seller,
                amount=reward,
                transaction_type='earning',
                submission=submission,
                description=f"제작 완료: {submission.request.title}"
            )
        
        return submission