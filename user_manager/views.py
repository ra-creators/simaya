from email import message
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()

# Create your views here.

def login_page(request):
    if request.method=="POST":
        email= request.POST.get('email')
        password=request.POST.get('password')
        if email and password:
            user=authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
           
    else:
        return render(request, 'userform/login.html')

def logout_page(request):
    logout(request)
    return redirect('/')

def signup_page(request):
    if request.method=="POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        password = request.POST.get("password")
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        if email and password:
            try:
                fname = request.POST.get("first_name")
                lname = request.POST.get("last_name")
                dob = request.POST.get("date_of_birth")
                phone = request.POST.get("phone")
                profile_pic = request.FILES.get('profile_pic')
                if profile_pic:
                    user = User.objects.create_user(email=email,
                                                    fname=fname,
                                                    lname=lname,
                                                    dob=dob,
                                                    phone_number=phone,
                                                    password=password,
                                                    profile_pic=profile_pic)
                else:
                    user = User.objects.create_user(email=email,
                                                    fname=fname,
                                                    lname=lname,
                                                    dob=dob,
                                                    phone_number=phone,
                                                    password=password)
                user.save()
                messages.success(request,'Congratulations Your Account Has Been Created')
                return redirect('signup')
            except Exception as e:
                print(e)
                messages.error(request, 'Invalid signup1')
                return redirect('signup')
        else:
            messages.error(request, 'Invalid signup2')
            return redirect('signup')
    else:
        return render(request,"userform/signup.html")




