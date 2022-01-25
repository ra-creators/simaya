from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('cd/', views.cart_detail, name='cart_detail'),
    path('total/', views.get_total_price, name='total_cart_price'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove,
        name='cart_remove'),
    path('increase/<int:product_id>/', views.cart_increase, name='cart_increase'),
    path('decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
]
