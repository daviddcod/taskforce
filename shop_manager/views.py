from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django import forms
from .models import Product, Cart, CartItem
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from .forms import ProductForm, CartForm, CartItemForm

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# Product Views
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # Updated to handle files
        if form.is_valid():
            form.save()
            return redirect('shop:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

# Similar changes for the product_update view

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('shop:product_list')
    return render(request, 'products/product_confirm_delete.html', {'object': product})

# Similar CRUD views for Cart and CartItem...
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Add or update the cart
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('shop:product_list')


from django.shortcuts import render
from .models import Product
from decimal import Decimal
def cart_view(request):
    cart = request.session.get('cart', {})
    
    cart_items = []
    total_price = Decimal('0.00')  # Ensure total_price is a decimal
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = int(quantity)  # Ensure quantity is an integer
            subtotal = product.price * quantity
            total_price += subtotal
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            # Handle cases where the product might not be found
            pass
        except TypeError:
            # Handle cases where quantity is not a number
            print(f"Invalid quantity type for product {product_id}: {type(quantity)}")

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Cart, CartItem, Order, Product
from django.contrib.auth.decorators import login_required
# Import other necessary models or utilities

@login_required
def checkout(request):
    try:
        # Retrieve the user's cart
        cart = Cart.objects.get(user=request.user)
        
        # Ensure the cart exists and has items
        if not cart or cart.items.count() == 0:
            return HttpResponse("Your cart is empty.")

        # Create a new order
        order = Order.objects.create(user=request.user)

        # Process each cart item
        for item in cart.items.all():
            # Deduct the quantity of the product from the stock and add to order
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()

                # Assuming an OrderItem model with a foreign key to Order and Product
                order.items.create(product=product, quantity=item.quantity, price=item.product.price)
            else:
                # Not enough stock to fulfill the order
                return HttpResponse(f"Not enough {product.name} in stock to complete your order.")

        # Clear the cart
        cart.items.all().delete()

        # Redirect to a success page with the order's id
        return redirect(reverse('shop:succes', args=[order.id]))  # Make sure you have a URL named 'order_success'

    except Cart.DoesNotExist:
        return HttpResponse("You do not have an active cart.")
    except Exception as e:
        # If anything goes wrong, render an error page
        return render(request, 'shop/error.html', {'message': str(e)})

def success(request):
    # Initialize Stripe with your secret key
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session_id = request.GET.get('session_id')
    if session_id is None:
        # If there's no session ID, redirect to an error page or back to cart
        return redirect('error')  # Make sure you have an error view and URL

    try:
        # Retrieve the checkout session to ensure it's paid
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            # Payment was successful

            # Here, you'd typically look up the order using session.client_reference_id
            # and update its status to paid or similar. This is highly dependent on your
            # order model and how you've structured your checkout process.

            # Clear the cart from the session after successful checkout
            request.session['cart'] = {}

            # Render a success template with relevant order details
            return render(request, 'success.html', {
                'order_id': session.client_reference_id,
                'amount_paid': session.amount_total / 100,  # Dividing by 100 to convert to dollars/pounds/etc.
            })
        else:
            # Payment was unsuccessful
            return redirect('error')  # Handle payment failure appropriately
    except stripe.error.StripeError as e:
        # Handle Stripe exceptions
        return render(request, 'error.html', {'message': str(e)})

    return redirect('error')  # Generic redirect if all else fails

def cancel(request):
    # Logic for handling a cancellation
    # You might want to send a message to the user explaining the cancellation or log the event.

    # Render a cancellation page to inform the user
    return render(request, 'cancel.html', {
        'message': 'Your transaction has been canceled.'
    })