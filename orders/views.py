from django.shortcuts import render
from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import OrderItem, Order
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart_detail')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        # Create the Order
        order = Order.objects.create(
            first_name=first_name, last_name=last_name, email=email,
            phone=phone, address=address, city=city, postal_code=postal_code
        )

        # Create Order Items from Cart
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Clear the cart session
        session_key = 'session_key'
        if session_key in request.session:
            del request.session[session_key]
            request.session.modified = True

        context = {'order': order}
        return render(request, 'orders/order_success.html', context)

    return render(request, 'orders/checkout.html', {'cart': cart})
# Create your views here.
