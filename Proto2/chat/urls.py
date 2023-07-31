from django.urls import path
from .views import POSChatView, AmazonSalesBasicChatView, TaskStatus

urlpatterns = [
    path('', POSChatView.as_view(), name='index'),
    path('amazon_sales_basic/', AmazonSalesBasicChatView.as_view()),
    path('task-status/<str:task_id>/', TaskStatus.as_view(), name='task-status'),
]
