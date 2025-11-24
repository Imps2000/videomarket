from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer, PurchaseSerializer
from submissions.serializers import SubmissionSerializer


class PurchaseView(APIView):
    """원본 구매 (재화 결제)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """원본 영상 구매"""
        serializer = PurchaseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            submission = serializer.save()
            # 구매 완료 후 제출물 정보 반환
            response_serializer = SubmissionSerializer(submission)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListView(APIView):
    """내 거래 내역 목록"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """거래 내역 조회 (최신순)"""
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserBalanceView(APIView):
    """내 재화 잔액 조회"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """사용자 재화 잔액 및 통계"""
        user = request.user
        balance_data = {
            'coins': user.coins,
            'completed_requests': user.completed_requests,
            'total_earnings': user.total_earnings,
        }
        return Response(balance_data, status=status.HTTP_200_OK)
