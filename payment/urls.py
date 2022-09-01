from django.urls import path
from payment.views import basketview

app_name = 'payment'

urlpatterns = [
    path('', basketview, name='basket'),
    # path('orderplaced/', order_placed, name='order_placed'),
    # path('webhook', stripe_webhook),
]
