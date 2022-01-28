from django.shortcuts import render
from django.views.generic import View
from cart.cart import Cart

# Create your views here.
class OrderCreate(View):
    def get(self, request):
        cart = Cart(request)
        address = request.user.user_address.all()[0]
        context = {}
        context['cart'] = cart
        

        return render(request, 'orders/confirmation.html')
    
    def post(self, request):
        pass