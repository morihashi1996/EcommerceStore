import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from basket.basket import Basket


@login_required
def basketview(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    print('total')
    stripe.api_key = 'sk_test_51LaXfIAf88l3syRF8mQwSXF54TWRkSglYxOamF9YGRge54F2lr14MOuEioJk7O4cmzjvJHMj2hgAXVWWRiZVSdkZ00dzD4rvcB'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )
    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})
