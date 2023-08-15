from django.contrib import admin
from payments.models import (
    Order,
)


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'product', 'payment_done', 'status', 'sub_status',
        'created_at', 'updated_at']
    list_filter = (
        'status', 'status', 'sub_status', 'created_at', 'updated_at'
    )
    search_fields = ('user__email', 'user__phone_number', 'product__title')
    autocomplete_fields = ('user', 'product')
    readonly_fields = ('slug', )


admin.site.register(Order, OrderAdmin)
