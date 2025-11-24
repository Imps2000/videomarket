from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Submission
from requests.models import Request
from .serializers import (
    SubmissionSerializer,
    SubmissionCreateSerializer,
    SubmissionListSerializer
)


class SubmissionListCreateView(APIView):
    """제출물 목록 조회 및 생성"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """본인이 제출한 제출물 목록"""
        submissions = Submission.objects.filter(creator=request.user)
        serializer = SubmissionListSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """영상 제출"""
        serializer = SubmissionCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            submission = serializer.save()
            response_serializer = SubmissionSerializer(submission)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmissionDetailView(APIView):
    """제출물 상세 조회"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """제출물 상세 (제작자 또는 의뢰자만)"""
        submission = get_object_or_404(Submission, pk=pk)

        # 권한 확인: 제작자 본인 또는 의뢰자
        if submission.creator != request.user and submission.request.requester != request.user:
            return Response(
                {"detail": "제작자 또는 의뢰자만 조회할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestSubmissionsView(APIView):
    """특정 의뢰의 제출물 목록"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, request_id):
        """
        제출물 조회 권한:
        1. 의뢰자 - 항상 모든 제출물 확인 가능
        2. 완료된 의뢰 - 모든 사람이 포트폴리오 확인 가능
        3. 진행 중 - 의뢰자만
        """
        request_obj = get_object_or_404(Request, pk=request_id)
        
        # 의뢰자는 항상 볼 수 있음
        if request_obj.requester == request.user:
            submissions = Submission.objects.filter(request=request_obj)
            serializer = SubmissionSerializer(submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 완료된 의뢰는 포트폴리오로 공개 (구매된 것 중 show_in_portfolio=True)
        if request_obj.status == 'completed':
            submissions = Submission.objects.filter(
                request=request_obj,
                show_in_portfolio=True,
                is_paid=True
            )
            serializer = SubmissionSerializer(submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 그 외는 권한 없음 (빈 배열 반환)
        return Response([], status=status.HTTP_200_OK)
