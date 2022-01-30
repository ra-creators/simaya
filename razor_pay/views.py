from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import RazorPayOrder, Transaction
from orders.models import Order

from .razorpay_cred import razorpay_client

@csrf_exempt
def rp_callback(request):
    if(request.method != 'POST'):
        return HttpResponse(400)
    # print("MADE TO RP_CALLBACK")
    data = request.POST
    # print(data)
    try:
        res = razorpay_client.utility.verify_payment_signature(data)
    except:
        return HttpResponse('payment failure')
    
    try:
        order = Order.objects.get(razorpay_order_id=data['razorpay_order_id'])
        rp_order = RazorPayOrder.objects.get(order=order)
        transaction = Transaction.objects.create(
            order=order,
            razor_pay_order=rp_order,
            payment_id=data['razorpay_payment_id'],
            payment_sig=data['razorpay_signature']
        )
        order.paid = True
        order.save()
        return redirect('success')
    except:
        return HttpResponse('error occured')
