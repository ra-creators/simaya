from importlib.metadata import requires
from itertools import product
from math import prod
from webbrowser import get
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.views.decorators.http import require_POST
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.
def cart(request):
    return render(request, 'cart/cart.html')

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
            override=cd['override'])
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/details.html', {'cart': cart})