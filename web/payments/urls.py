from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()

router.register(r'buy', PaymentViewSet, basename='buy')
router.register(r'buy_order', OrderPaymentViewSet, basename='buy_order')
router.register(r'intent', PaymentIntentViewSet, basename='intent')


urlpatterns = [
    path('', item_list, name='item_list'),
    path('', include(router.urls)),
    
    path('item/<int:id>/', item_detail, name='item_detail'),
    path('item/<int:id>/intent/', item_intent_detail, name='item_intent_detail'),
    
    path('order/<int:id>/', order_detail, name='order_detail'),
]
