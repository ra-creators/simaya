from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Shop
    path('shop/', views.shop, name='shop'),

    # Shop category api
    path('shop/api/', views.categories_api, name='categories_api'),
    path('shop/api/<slug:category>', views.categories_api, name='categories_api_'),
    
    # Shop category api by count
    path('shop/api/count/<int:count>', views.categories_api_by_count, name='categories_api_by_count'),
    path('shop/api/count/<int:count>/<slug:category>', views.categories_api_by_count, name='categories_api_by_count_'),

    # Shop collection
    path('shop/collection/<slug:category>', views.collection, name='collection'),
    path('shop/product/collection/<slug:category>/<slug:gender>', views.collection_by_gender, name='collection_by_gender'),
    path('shop/name/collection/<slug:category>', views.get_collection_names, name='get_collection_names'),

    # products_by_categories
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:cat_slug>/', views.categories, name='list_by_category'),

    # single product
    path('product/<int:pk>/', views.single_product_view, name='single_product'),
]
