from django.shortcuts import get_object_or_404, redirect
import json 
from django.shortcuts import render
from django.core import serializers
from django.http import Http404, HttpResponse
from .models import Category, Product

# Create your views here.
def index(request):
    context = {}
    categories = Category.objects.all()
    products = Product.objects.all()[:3]
    context['categories'] = categories
    context['products'] = products
    return render(request,"others/index.html", context=context)

def shop(request):
    context = {}
    categories = Category.objects.all()
    products = Product.objects.all()[:3]
    context['categories'] = categories
    context['products'] = products
    return render(request,"product/shop.html", context=context)

def categories(request, cat_slug=None):
    context = {}
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    context['page_heading'] = 'Categories'
    context['page_type'] = 'list'
    context['single_url'] = 'list_by_category'

    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        context['page_heading'] = category.name
        context['page_type'] = 'single'
        categories = [category]
        products = products.filter(category=category)

    context.update({
        'property': category,
        'properties': categories,
        'products': products,
    })
    # print(context)
    return render(request, 'product/product_list.html', context=context)

def categories_api(request, category=None):
    if category == None:
        products = Product.objects.filter(available=True)
        products_json = serializers.serialize('json', products)
        return HttpResponse(add_img_url(products_json), content_type='application/json')

    cat_obj = get_object_or_404(Category, name=category.title())
    cat = Product.objects.filter(category=cat_obj, available=True)
    cat_json = serializers.serialize('json', cat)
    cat_json = add_img_url(cat_json)
    return HttpResponse(cat_json, content_type='application/json')

def add_img_url(cat_json):
    cat_json = json.loads(cat_json)
    for line in cat_json:
        line['fields']['img_url'] = str(Product.objects.get(id=line['pk']).get_primary_image)
    return json.dumps(cat_json)

def single_product_view(request, pk=None):
    if not pk:
        redirect('index')
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'product/single_product.html', context=context)

def categories_api_by_count(request, count, category=None):
    if category == None:
        products = Product.objects.filter(available=True)[:count]
        products_json = serializers.serialize('json', products)
        return HttpResponse(add_img_url(products_json), content_type='application/json')

    cat_obj = get_object_or_404(Category, name=category.title())
    cat = Product.objects.filter(category=cat_obj, available=True)[:count]
    cat_json = serializers.serialize('json', cat)
    cat_json = add_img_url(cat_json)
    return HttpResponse(cat_json, content_type='application/json')