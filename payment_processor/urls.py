# payment_processor/urls.py

from django.urls import path
from .views import start_payment, payment_webhook, payment_complete, create_billing_detail

app_name = 'payment_processor'  # This defines the namespace for this URLs module


urlpatterns = [
    path('start-payment/<int:billing_detail_id>/', start_payment, name='start_payment'),
    path('payment/webhook/', payment_webhook, name='payment_webhook'),
    path('payment/complete/', payment_complete, name='payment_complete'),
    path('create-billing/', create_billing_detail, name='create_billing_detail'),

]