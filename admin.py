from django.contrib import admin
from .models import User, Order


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ('email', 'full_name', 'phone')
    search_fields = ('email', 'full_name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('order_id', 'user', 'grand_total', 'status', 'placed_at')
    list_filter   = ('status',)
    search_fields = ('order_id', 'user__email')
    readonly_fields = ('placed_at',)
