from django.urls import path
from .views import (
    SubmissionListCreateView,
    SubmissionDetailView,
    RequestSubmissionsView
)

urlpatterns = [
    path('', SubmissionListCreateView.as_view(), name='submission-list-create'),
    path('<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('request/<int:request_id>/', RequestSubmissionsView.as_view(), name='request-submissions'),
]
