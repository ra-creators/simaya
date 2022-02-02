from django.contrib import admin
from .models import Transaction, RazorPayOrder

# Register your models here.
admin.site.register(RazorPayOrder)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'timestamp', 'order']
    exclude = ['razor_pay_order', 'payment_sig']
    readonly_fields = ['payment_id', 'payment_sig', 'order', 'timestamp']