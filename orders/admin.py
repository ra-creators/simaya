from django.contrib import admin
from .models import Order, OrderItem, OrderTrackingStatus

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # readonly_fields = ['product', 'sub_total']
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

# class OrderTrackingInline(admin.StackedInline):
#     model = OrderTracking

class OrderTrackingStatusInline(admin.TabularInline):
    model = OrderTrackingStatus

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline, OrderTrackingStatusInline]
    readonly_fields = ('created', 'updated', 'address', 'total', 'user')