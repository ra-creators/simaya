from django.contrib import admin
from .models import Product,Cart

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','titel','selling_price','discounted_price','discription','category','product_image')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=('id','quantity','product','user')
    


    
