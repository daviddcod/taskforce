from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from wdmmorpg.models import UserProfile

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_audio_file = models.BooleanField(default=False)
    is_python_file = models.BooleanField(default=False)
    is_image_file = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', default='product_images/shopimage.jpg')
    stock = models.IntegerField()

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # You might want to add a price field to lock the price at the time of adding to the cart

from django.db import models
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
