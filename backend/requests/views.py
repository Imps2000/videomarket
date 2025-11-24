from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Request
from .serializers import RequestSerializer, RequestCreateSerializer


class RequestListCreateView(APIView):
    """의뢰 목록 조회 및 생성"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """의뢰 목록 조회 (모든 open 의뢰)"""
        requests_list = Request.objects.filter(
            Q(status__in=['open', 'in_progress']) &
            (Q(request_type='global') | Q(target_user=request.user) | Q(requester=request.user))
        ).order_by('-created_at')
        
        serializer = RequestSerializer(requests_list, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """의뢰 생성"""
        serializer = RequestCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestDetailView(APIView):
    """의뢰 상세 조회, 수정, 삭제"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """의뢰 상세 조회"""
        request_obj = get_object_or_404(Request, pk=pk)
        serializer = RequestSerializer(request_obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """의뢰 수정 (본인만)"""
        request_obj = get_object_or_404(Request, pk=pk)

        # 본인 확인
        if request_obj.requester != request.user:
            return Response(
                {"detail": "본인의 의뢰만 수정할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RequestCreateSerializer(request_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = RequestSerializer(request_obj)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """의뢰 삭제 (본인만)"""
        request_obj = get_object_or_404(Request, pk=pk)

        # 본인 확인
        if request_obj.requester != request.user:
            return Response(
                {"detail": "본인의 의뢰만 삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        request_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyRequestsView(APIView):
    """내가 올린 의뢰 목록"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """내가 올린 의뢰 목록 조회"""
        my_requests = Request.objects.filter(requester=request.user)
        serializer = RequestSerializer(my_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
