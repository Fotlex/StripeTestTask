import stripe
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from config import config
from .models import Item


def get_stripe_keys(currency):
    if currency == 'usd':
        return config.STRIPE_SECRET_KEY_USD, config.STRIPE_PUBLIC_KEY_USD

    return config.STRIPE_SECRET_KEY_EUR, config.STRIPE_PUBLIC_KEY_EUR


class PaymentViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        item = get_object_or_404(Item, id=pk)
        
        secret_key, _ = get_stripe_keys(item.currency)
        stripe.api_key = secret_key

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': item.price * 100,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"http://{config.APP_URL}/item/{item.id}/?success=true",
                cancel_url=f"http://{config.APP_URL}/item/{item.id}/?canceled=true",
            )
            return Response({'session_id': session.id}, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def item_list(request):
    items = Item.objects.all()
    return render(request, 'index.html', {'items': items})


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    _, public_key = get_stripe_keys(item.currency)

    context = {
        'item': item,
        'stripe_public_key': public_key
    }
    return render(request, 'item.html', context)