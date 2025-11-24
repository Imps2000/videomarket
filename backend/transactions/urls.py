from django.urls import path
from .views import PurchaseView, TransactionListView, UserBalanceView

urlpatterns = [
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('balance/', UserBalanceView.as_view(), name='user-balance'),
]
