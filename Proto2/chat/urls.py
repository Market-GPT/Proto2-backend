from django.urls import path
from .views import POSChatView

urlpatterns = [
    path('', POSChatView.as_view(), name='index'),
    path('amazon_sales_basic/', POSChatView.as_view(), name='index')
]
