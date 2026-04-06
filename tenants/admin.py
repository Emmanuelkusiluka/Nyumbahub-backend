from django.contrib import admin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'room', 'move_in_date', 'status']
    list_filter = ['status', 'room__house']
    search_fields = ['first_name', 'last_name', 'phone', 'national_id']
    readonly_fields = ['created_at', 'updated_at']
