
from django.shortcuts import render
from .models import Blog

# Create your views here.

def blog_page(request):
    fm= Blog.objects.all()
    data = Blog.objects.filter(id=1)
    return render(request,"blog/blog.html",{'form':fm ,'dt':data})

def blog_detail(request,pk):
    fm= Blog.objects.all()
    data = Blog.objects.filter(pk=pk)
    return render(request,"blog/blogdetail.html",{'dt':data,'form':fm})
