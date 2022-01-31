import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from .cart import Cart
from coupons.models import Coupon
from .helpers import *
# from .forms import CartAddProductForm

# Create your views here.
def cart(request):
    cart = Cart(request)
    discount = None
    if request.session.get('coupon_id'):
        discount = Coupon.objects.get(id=request.session['coupon_id']).discount
    # print(request.session.get('coupon_id'))
    # cart.print_cart()
    return render(request, 'cart/cart.html', {'cart': cart, 'discount': discount})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form_data = request.POST.copy()
    size = form_data.get('sizes')
    metal = form_data.get('metal')
    diamond = form_data.get('diamond')
    price = get_price(product, size, metal, diamond)
    if size and metal and diamond and price:
        cart.add(product=product,
                 price=price,
                 size=size,
                 metal=metal, 
                 diamond=diamond)
    if 'buy_now' in form_data:
        # Redirect to Buy Now
        return redirect('order_create')
    
    # print(request.POST)
    # print(product)
    return redirect('cart')

@csrf_exempt
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return HttpResponse(200)

def get_total_price(request):
    cart = Cart(request)
    total = cart.get_total_price()
    discount_price = 0
    if request.session.get('coupon_id'):
        discount_price = cart.get_total_price_after_discount()
    content = json.dumps({'total': str(total), 'discount_price': str(discount_price)})
    return HttpResponse(content, content_type='application/json')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/details.html', {'cart': cart})

@csrf_exempt
@require_POST
def cart_increase(request, product_id):
    cart = Cart(request)
    product_id = str(product_id)
    is_ok = cart.increase_count(product_id)
    # cart.print_cart()
    if is_ok:
        return HttpResponse(200)
    return HttpResponse(400)        

@csrf_exempt
@require_POST
def cart_decrease(request, product_id):
    cart = Cart(request)
    # print(product_id)
    product_id = str(product_id)
    is_ok = cart.decrease_count(product_id)
    # cart.print_cart()
    if is_ok:
        return HttpResponse(200)
    return HttpResponse(400)        