from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Category, Product

# Create your views here.
def index(request):
    context = {}
    categories = Category.objects.all()
    products = Product.objects.all()[:3]
    context['categories'] = categories
    context['products'] = products
    return render(request,"others/index.html", context=context)


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