from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import Product,Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.db.models import Q
from django.http import JsonResponse 


# Create your views here.

def home_page(request):
    return render(request,"app/index.html",)

def about_page(request):
    return render(request,"app/AboutUs.html" )

def contact_page(request):
    return render(request,"app/ContactUs.html")



def blog_page(request):
    return render(request,"app/blog.html" )

def ring_page(request):
    ring=Product.objects.filter(category="Ring")
    ear=Product.objects.filter(category="Earring")
    brac=Product.objects.filter(category="Bracelet")
    neck=Product.objects.filter(category="Necklace")
    return render(request, "app/ring.html", {'rings':ring,'ears':ear,'bracs':brac,'necks':neck})

def product_detail(request,pk):
    pro=Product.objects.get(pk=pk)
    return render(request, 'app/product.html',{'pro':pro})

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def cart_page(request):
    if request.user.is_authenticated:
        user=request.user
        carts=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=0.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                print(amount)
                totalamount=amount+shipping_amount
            return render(request,"app/cart.html" ,{'cart':carts,'amount':amount,'totalamount':totalamount})
        else:
            return render(request,"app/emptycart.html" )
            

def plus_cart(request):
     if request.method=='GET':
          prod_id = request.GET['prod_id']
          c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
          c.quantity+=1
          c.save()
          amount=0.0
          shipping_amount=70.0
          cart_product=[p for p in Cart.objects.all() if p.user==request.user]
          for p in cart_product:
               tempamount=(p.quantity*p.product.discounted_price)
               amount+=tempamount
             
          data={
               'quantity':c.quantity,
               'amount':amount,
               'totalamount':amount+shipping_amount
               }
          return JsonResponse(data)


def minus_cart(request):
     if request.method=='GET':
          prod_id = request.GET['prod_id']
          c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
          c.quantity-=1
          c.save()
          amount=0.0
          shipping_amount=70.0
          cart_product=[p for p in Cart.objects.all() if p.user==request.user]
          for p in cart_product:
               tempamount=(p.quantity*p.product.discounted_price)
               amount+=tempamount
     
             
          data={
               'quantity':c.quantity,
               'amount':amount,
               'totalamount':amount+shipping_amount
               }
          return JsonResponse(data)



def remove_cart(request):
     if request.method=='GET':
          prod_id = request.GET['prod_id']
          c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
          c.delete()
          amount=0.0
          shipping_amount=70.0
          cart_product=[p for p in Cart.objects.all() if p.user==request.user]
          for p in cart_product:
               tempamount=(p.quantity*p.product.discounted_price)
               amount+=tempamount
          data={
               'amount':amount,
               'totalamount':amount+shipping_amount
               }
          return JsonResponse(data)
          
def profile_page(request):
    return render(request,"app/profile.html")
    


def signin_page(request):
    return render(request,"app/signIn.html")


def login_page(request):
    return render(request,"app/logIn.html")



def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


