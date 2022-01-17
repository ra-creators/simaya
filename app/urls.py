from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home_page,name="home"),
    path('about/',views.about_page,name="aboutpage"),
    path('contact/',views.contact_page,name="contactpage"),
    path('blog/',views.blog_page,name="blogpage"),
    path('profile/',views.profile_page,name="profile"),

    path('ring/',views.ring_page,name="ring_name"),
    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.cart_page,name="cartpage"),

    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    
    path('signin/',views.signin_page,name="signin"),
    path('login/',views.login_page,name="login"),
    path('logout/',views.logout_page,name="logout")

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)