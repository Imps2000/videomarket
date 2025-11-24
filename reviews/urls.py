from django.urls import path
from .views import ReviewListCreateView, SubmissionReviewView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review-list-create'),
    path('submission/<int:submission_id>/', SubmissionReviewView.as_view(), name='submission-review'),
]
