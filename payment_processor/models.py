
from django.db import models

class BillingDetail(models.Model):
    user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE)
    plan = models.ForeignKey('plan_selection.Plan', on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    # Add more fields as necessary

    def __str__(self):
        return f'Billing Detail for {self.user.username}'

# payment_processor/models.py

class Payment(models.Model):
    billing_detail = models.ForeignKey(BillingDetail, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True)  # ID from the payment gateway
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment of ${self.amount} for {self.billing_detail.user.username}'

