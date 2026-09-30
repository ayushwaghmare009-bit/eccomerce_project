from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart_detail.html', context)

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # override_quantity=True sets the exact quantity from the box
    cart.add(product=product, quantity=quantity, override_quantity=True)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')