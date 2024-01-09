from django import forms
from .models import Product, Cart, CartItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'is_audio_file', 'is_python_file', 'is_image_file', 'image']  # Include 'image' field
        
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']

from django import forms

class OrderConfirmForm(forms.Form):
    confirm = forms.BooleanField(label="I confirm my order")
