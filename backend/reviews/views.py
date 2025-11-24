from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Review
from submissions.models import Submission
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewListCreateView(APIView):
    """평가 목록 조회 및 작성"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """내가 작성한 평가 목록"""
        reviews = Review.objects.filter(reviewer=request.user)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """평가 작성"""
        serializer = ReviewCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            review = serializer.save()
            response_serializer = ReviewSerializer(review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmissionReviewView(APIView):
    """특정 제출물의 평가 조회"""
    permission_classes = [IsAuthenticated]

    def get(self, request, submission_id):
        """특정 제출물의 평가 조회 (공개)"""
        submission = get_object_or_404(Submission, pk=submission_id)

        # 평가가 있는지 확인
        if not hasattr(submission, 'review'):
            return Response(
                {"detail": "아직 평가가 작성되지 않았습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewSerializer(submission.review)
        return Response(serializer.data, status=status.HTTP_200_OK)
