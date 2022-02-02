from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from cart.cart import Cart
from coupons.models import Coupon
from .models import Order, OrderItem
from product.models import Product
from razor_pay.models import RazorPayOrder

from razor_pay.razorpay_cred import razorpay_client, RAZOR_KEY_ID


# Create your views here.
class OrderCreate(View, LoginRequiredMixin):
    def get(self, request):
        cart = Cart(request)
        address = request.user.addresses.all()[0]
        context = {}
        context['cart'] = cart
        context['address'] = address
        if request.session.get('coupon_id'):
            context["discount"] = Coupon.objects.get(id=request.session['coupon_id']).discount
            context['discount_price'] = cart.get_total_price_after_discount()
        return render(request, 'orders/confirmation.html', context=context)
    
    def post(self, request):
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        id_ = request.POST.get('id')
        address_type = request.POST.get('address_type')
        # queryset = request.user.addresses.filter(first_name=fname, last_name=lname, address=address, city=city, country=country, postal_code=pincode)
        # print(queryset)
        # if queryset is None:
        #     return HttpResponse("Exists already")
        # else:
            
        #     return HttpResponse("Created")
        try:
            # Uncomment this to create a new address
            # request.user.addresses.create(
            #     first_name=fname,
            #     last_name=lname,
            #     address=address, 
            #     city=city,
            #     country=country,
            #     postal_code=pincode,
            #     address_type=address_type.title()
            #     )

            context = create_order(request, id_)
            if context is None:
                return HttpResponseBadRequest()
            # print(context)
            return JsonResponse({
                'status': '200',
                'context': context
            })
        except Exception as e:
            print(e)
            return JsonResponse({'status':400})

def create_order(request, address_id):
    cart = Cart(request)
    context = {}
    # cart.print_cart()

    order = Order.objects.create(
        user=request.user,
        address_id=1, # add address_id
    )

    try:
        for id, item in cart.cart.items():
            OrderItem.objects.create(
                order=order,
                product=Product.objects.get(id=id),
                size=item['size'],
                metal=item['metal'],
                diamond=item['diamond'],
                price=int(float(item['price'])),
                quantity=int(item['quantity']),
            )
    except Exception as e:
        print(e)
        print("ERROR OCCURED WHILE CREATING ORDER")
    
    order.save()

    try:
        order_data = {}
        order_data['amount'] = str(cart.get_total_price() * 100)
        if request.session.get('coupon_id'):
            order_data['amount'] = str(cart.get_total_price_after_discount() * 100)
        order_data['currency'] = 'INR'

        razorpay_order = razorpay_client.order.create(data=order_data)

        order.razorpay_order_id = razorpay_order['id']
        order.save()

        RazorPayOrder.objects.create(
            order=order,
            rp_id=razorpay_order['id'],
        )

        context = {}
        context['razorpay_order_id'] = razorpay_order['id']
        context['razorpay_merchant_key'] = RAZOR_KEY_ID
        context['razorpay_amount'] = str(cart.get_total_price() * 100)
        context['currency'] = 'INR'
        context['callback_url'] = '/razor_pay/rp_callback/'

        cart.clear()

        return context
    except Exception as e:
        print(e)
        # print("ERROR OCCURED WHILE CREATING RAZORPAY ORDER")
        return None

def success(request):
    return render(request, 'orders/success.html')