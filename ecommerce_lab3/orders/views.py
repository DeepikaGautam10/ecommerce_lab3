from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from products.models import Cart, CartItem

@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('products:cart')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            shipping_address=request.POST.get('shipping_address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code', ''),
            payment_method=request.POST.get('payment_method'),
            total_amount=cart.total_price,
            notes=request.POST.get('notes', '')
        )
        
        # Create order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders:order_detail', order.id)
    
    context = {
        'cart': cart
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'orders/order_list.html', context)

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order
    }
    return render(request, 'orders/order_detail.html', context)
