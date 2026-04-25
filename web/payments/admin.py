from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'currency')
    list_filter = ('currency',)
    search_fields = ('name',)
    