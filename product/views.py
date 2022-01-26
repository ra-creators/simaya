from email.mime import application
from django.shortcuts import get_object_or_404, redirect
import json 
from django.shortcuts import render
from django.core import serializers
from django.http import Http404, HttpResponse

from cart.cart import Cart
from .models import Category, Product, Collection

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
    # cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        # 'cart_product_form': cart_product_form
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

def collection(request, category=None):
    if category == None:
        return Http404
    context = {}
    category_ = Category.objects.get(slug=category)
    # if not collection_:
    #     return Http404
    products = Product.objects.filter(category=category_, available=True)
    male = products.filter(gender='Man')
    female = products.filter(gender='Woman')
    if len(male) >= 1:
        context['male_collection'] = male[0]
    if len(female) >= 1:
        context['female_collection'] = female[0]
    collections = Collection.objects.filter(category=category_)
    context.update({
        'category_title': category_,
        'collections': collections,
        'products': products
    })
    # print(context)
    return render(request, 'product/product_collection_list.html', context=context)

def get_collection_names(request, category=None):
    if category == None:
        return Http404
    cat = get_object_or_404(Category, slug=category)
    col = Collection.objects.filter(category=cat)
    collections = serializers.serialize('json', col)
    # print(collections)
    return HttpResponse(collections, content_type='application/json')

def category_by_gender(request, category=None, gender="Woman"):
    if category == None:
        return Http404
    cat = get_object_or_404(Category, slug=category)
    p = Product.objects.filter(category=cat, available=True, gender=gender)
    products = serializers.serialize('json', p)
    return HttpResponse(products, content_type='application/json')

def collection_products(request, collection=None):
    if collection == None:      
        return Http404
    collection_ = Collection.objects.get(slug=collection)
    products = Product.objects.filter(collection=collection_, available=True)
    products_json = serializers.serialize('json', products)
    # print(products_json)
    return HttpResponse(add_img_url(products_json), content_type='application/json')