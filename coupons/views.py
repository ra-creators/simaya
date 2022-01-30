from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Coupon
from cart.cart import Cart

# Create your views here.
@require_POST
@csrf_exempt
def coupon_apply(request):
    code = request.POST.get("code")
    if code:
        try:
            coupon = Coupon.objects.get(
                code__iexect=code,
                active=True
            )
            if not coupon.is_valid:
                # Raise error that coupon is not valid
                raise Exception("Coupon is not valid")
            request.session['coupon_id'] = coupon.id
        except:
            request.session['coupon_id'] = None
        return JsonResponse({"success": True})
