from django.urls import path
from .views import POSChatView, AmazonSalesBasicChatView

urlpatterns = [
    path('', POSChatView.as_view(), name='index'),
    path('amazon_sales_basic/', AmazonSalesBasicChatView.as_view(), name='index')
]
