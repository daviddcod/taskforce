# payment_processor/admin.py

from django.contrib import admin
from .models import BillingDetail, Payment

admin.site.register(BillingDetail)
admin.site.register(Payment)
