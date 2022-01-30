from django.contrib import admin
from .models import Coupon
# Register your models here.

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to',
     'discount', 'percentage', 'active')
    list_filter = ('active', 'valid_from', 'valid_to', 'percentage')
    search_fields = ('code', 'discount')