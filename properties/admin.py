from django.contrib import admin
from .models import House, Room


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    fields = ['room_number', 'monthly_rent', 'status', 'floor']


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'total_rooms', 'occupied_rooms', 'occupancy_rate']
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'house', 'monthly_rent', 'status', 'floor']
    list_filter = ['status', 'house']
    search_fields = ['room_number', 'house__name']
