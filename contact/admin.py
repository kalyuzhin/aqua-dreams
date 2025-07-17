from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'created_at', 'get_pool_name')
    search_fields = ('full_name', 'phone_number', 'pool_name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def get_pool_name(self, obj):
        return obj.pool_name
    get_pool_name.short_description = 'Наименование запроса'

    # Запретить добавление через админку
    def has_add_permission(self, request):
        return False