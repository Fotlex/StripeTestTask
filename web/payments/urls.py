from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, item_detail, item_list


router = DefaultRouter()

router.register(r'buy', PaymentViewSet, basename='buy')

urlpatterns = [
    path('', item_list, name='item_list'),
    path('', include(router.urls)),
    path('item/<int:id>', item_detail, name='item_detail'),
]