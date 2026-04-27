import stripe
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from config import config
from .models import Item, Order


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
    orders = Order.objects.all()
    
    context = {
        'items': items,
        'orders': orders
    }
    return render(request, 'index.html', context)


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    _, public_key = get_stripe_keys(item.currency)

    context = {
        'item': item,
        'stripe_public_key': public_key
    }
    return render(request, 'item.html', context)


class OrderPaymentViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, id=pk)
        
        if not order.items.exists():
            return Response({'error': 'Order is empty'}, status=status.HTTP_400_BAD_REQUEST)

        currency = order.get_currency
        secret_key, _ = get_stripe_keys(currency)
        stripe.api_key = secret_key

        try:
            line_items = []
            tax_rates = []

            if order.tax:
                tax_rate = stripe.TaxRate.create(
                    display_name=order.tax.name,
                    percentage=order.tax.percentage,
                    inclusive=False,
                )
                tax_rates.append(tax_rate.id)

            for item in order.items.all():
                line_items.append({
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': item.price * 100,
                    },
                    'quantity': 1,
                    'tax_rates': tax_rates if tax_rates else None,
                })

            checkout_kwargs = {
                'payment_method_types': ['card'],
                'line_items': line_items,
                'mode': 'payment',
                'success_url': f"http://{config.APP_URL}/?success=true",
                'cancel_url': f"http://{config.APP_URL}/?canceled=true",
            }

            if order.discount:
                coupon = stripe.Coupon.create(
                    percent_off=order.discount.percent_off, 
                    name=order.discount.name,
                    duration='once'
                )
                checkout_kwargs['discounts'] = [{'coupon': coupon.id}]

            session = stripe.checkout.Session.create(**checkout_kwargs)
            return Response({'session_id': session.id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntentViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        item = get_object_or_404(Item, id=pk)
        secret_key, _ = get_stripe_keys(item.currency)
        stripe.api_key = secret_key

        try:
            intent = stripe.PaymentIntent.create(
                amount=item.price * 100,
                currency=item.currency,
                payment_method_types=['card']
            )
            return Response({'client_secret': intent.client_secret}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    _, public_key = get_stripe_keys(order.get_currency)
    
    context = {
        'order': order,
        'stripe_public_key': public_key
    }
    return render(request, 'order.html', context)


def item_intent_detail(request, id):
    item = get_object_or_404(Item, id=id)
    _, public_key = get_stripe_keys(item.currency)

    context = {
        'item': item,
        'stripe_public_key': public_key
    }
    return render(request, 'intent.html', context)