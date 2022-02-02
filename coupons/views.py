from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Coupon
from cart.cart import Cart

# Create your views here.
@require_POST
@csrf_exempt
def coupon_apply(request, promo):
    code = promo
    if code:
        now = timezone.now()
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
            print('found')
            cart = Cart(request)

            check_dis = cart.check_discount(coupon)
            if cart.get_total_price() - check_dis < 1:
                print('less than 1')
                request.session['coupon_id'] = None
                return JsonResponse({'status': 'error'})
            
            dic = {
                'status': 'success',
                'discount': int(coupon.discount),
                'total': str(cart.get_total_price_after_discount())
            }
            print(dic)
            return JsonResponse(dic)
        except Exception as e:
            print(e)
            request.session['coupon_id'] = None
            return JsonResponse({"status": 'error'})
