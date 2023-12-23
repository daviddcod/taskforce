# payment_processor/views.py

from mollie.api.client import Client
from django.shortcuts import redirect, render
from .models import Payment, BillingDetail
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import BillingDetailForm

# payment_processor/mollie_helper.py
from mollie.api.client import Client
from django.conf import settings

def get_mollie_client():
    client = Client()
    client.set_api_key(settings.MOLLIE_API_KEY)
    return client


def start_payment(request, billing_detail_id):
    mollie_client = Client()
    mollie_client.set_api_key(settings.MOLLIE_API_KEY)

    billing_detail = BillingDetail.objects.get(id=billing_detail_id)
    amount = billing_detail.plan.price  # Assuming you have a price field in Plan model

    payment = mollie_client.payments.create({
        'amount': {'currency': 'EUR', 'value': str(amount)},
        'description': f'Payment for {billing_detail.plan.name}',
        'redirectUrl': request.build_absolute_uri('/payment/complete/'),
        'webhookUrl': request.build_absolute_uri('/payment/webhook/'),
        'method': 'ideal'
    })

    # Save the payment info
    Payment.objects.create(
        billing_detail=billing_detail,
        amount=amount,
        payment_id=payment['id']
    )

    return redirect(payment['_links']['checkout']['href'])

# Include other views to handle payment completion and webhook

# In your views.py or wherever you handle payments

def create_payment(request):
    mollie_client = get_mollie_client()
    payment = mollie_client.payments.create({
        'amount': {
            'currency': 'EUR',
            'value': '10.00'  # 10 Euro
        },
        'description': 'Payment description',
        'redirectUrl': request.build_absolute_uri('/payment/success/'),
        'webhookUrl': request.build_absolute_uri('/payment/webhook/')
    })

    # Redirect the user to Mollie to complete the payment.
    return redirect(payment.checkout_url)

# payment_processor/views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        payment_id = request.POST.get('id')
        mollie_client = Client()
        mollie_client.set_api_key('settings.MOLLIE_API_KEY')

        payment = mollie_client.payments.get(payment_id)
        if payment['status'] == 'paid':
            # Update your payment model
            payment_record = Payment.objects.get(payment_id=payment_id)
            payment_record.is_paid = True
            payment_record.save()

        return HttpResponse('Received!')
    else:
        return HttpResponse('Only POST requests are allowed', status=405)

# payment_processor/views.py

def payment_complete(request):
    user = request.user
    # Logic to check user's last payment status or use session data to identify the payment
    # Show a success message or payment status to the user
    return render(request, 'payment_complete.html', {'user': user})


from django.contrib.auth.decorators import login_required
from .forms import BillingDetailForm
from plan_selection.models import Plan

@login_required
def create_billing_detail(request):
    selected_plan_id = request.GET.get('selected_plan')
    selected_plan = Plan.objects.get(id=selected_plan_id) if selected_plan_id else None
    
    if request.method == 'POST':
        form = BillingDetailForm(request.POST)
        if form.is_valid():
            billing_detail = form.save(commit=False)
            billing_detail.user = request.user
            billing_detail.plan = selected_plan
            billing_detail.save()
            return redirect('payment_processor:start_payment', billing_detail_id=billing_detail.id)
    else:
        form = BillingDetailForm(initial={'plan': selected_plan})
    
    return render(request, 'create_billing_detail.html', {'form': form, 'selected_plan': selected_plan})
