from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import OTP, UserAddress
User = get_user_model()


class UserAddressInline(admin.StackedInline):
    model = UserAddress
    can_delete = False
    extra = 0
    verbose_name_plural = 'UserAddress'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserAddressInline,)


admin.site.register(OTP)
