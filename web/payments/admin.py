from django.contrib import admin
from .models import Item, Discount, Tax, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'currency')
    list_filter = ('currency',)
    search_fields = ('name',)
    
    
admin.site.register(Discount)
admin.site.register(Tax)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_total_price', 'discount', 'tax')
    filter_horizontal = ('items',)

    def get_total_price(self, obj):
        return f"{obj.total_price}"
    get_total_price.short_description = "Сумма"