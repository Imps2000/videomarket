from django.urls import path
from .views import RequestListCreateView, RequestDetailView, MyRequestsView

urlpatterns = [
    path('', RequestListCreateView.as_view(), name='request-list-create'),
    path('my/', MyRequestsView.as_view(), name='my-requests'),
    path('<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
]
