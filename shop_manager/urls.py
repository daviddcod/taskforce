from django.urls import path, include
from . import views

app_name = 'shop'  # This defines the namespace for this URLs module

urlpatterns = [
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),    # Similar URL patterns for Cart and CartItem...
    path('checkout/', views.checkout, name='checkout'),

    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
