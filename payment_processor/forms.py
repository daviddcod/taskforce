from django import forms
from .models import BillingDetail

class BillingDetailForm(forms.ModelForm):
    class Meta:
        model = BillingDetail
        fields = ['address', 'city', 'postal_code', 'country']
