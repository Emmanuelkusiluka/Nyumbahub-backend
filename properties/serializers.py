from rest_framework import serializers
from .models import House, Room


class RoomSerializer(serializers.ModelSerializer):
    house_name = serializers.CharField(source='house.name', read_only=True)

    class Meta:
        model = Room
        fields = [
            'id', 'house', 'house_name', 'room_number', 'monthly_rent',
            'status', 'description', 'floor', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoomInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'monthly_rent', 'status', 'floor']


class HouseSerializer(serializers.ModelSerializer):
    rooms = RoomInlineSerializer(many=True, read_only=True)
    total_rooms = serializers.ReadOnlyField()
    occupied_rooms = serializers.ReadOnlyField()
    vacant_rooms = serializers.ReadOnlyField()
    maintenance_rooms = serializers.ReadOnlyField()
    occupancy_rate = serializers.ReadOnlyField()

    class Meta:
        model = House
        fields = [
            'id', 'name', 'address', 'description',
            'total_rooms', 'occupied_rooms', 'vacant_rooms', 'maintenance_rooms',
            'occupancy_rate', 'rooms', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class HouseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views (no rooms inline)."""
    total_rooms = serializers.ReadOnlyField()
    occupied_rooms = serializers.ReadOnlyField()
    vacant_rooms = serializers.ReadOnlyField()
    occupancy_rate = serializers.ReadOnlyField()

    class Meta:
        model = House
        fields = [
            'id', 'name', 'address',
            'total_rooms', 'occupied_rooms', 'vacant_rooms', 'occupancy_rate',
            'created_at'
        ]
