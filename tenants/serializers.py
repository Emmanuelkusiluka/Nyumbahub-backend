from rest_framework import serializers
from .models import Tenant
from properties.models import Room


class TenantSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    house_name = serializers.CharField(source='room.house.name', read_only=True)
    house_id = serializers.IntegerField(source='room.house.id', read_only=True)
    monthly_rent = serializers.DecimalField(
        source='room.monthly_rent', max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Tenant
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'phone', 'email',
            'national_id', 'emergency_contact_name', 'emergency_contact_phone',
            'room', 'room_number', 'house_name', 'house_id', 'monthly_rent',
            'move_in_date', 'move_out_date', 'status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        room = attrs.get('room')
        status = attrs.get('status', 'active')
        # If assigning a room, ensure it's not already occupied by another active tenant
        if room and status == Tenant.STATUS_ACTIVE:
            active_in_room = Tenant.objects.filter(
                room=room, status=Tenant.STATUS_ACTIVE
            )
            if self.instance:
                active_in_room = active_in_room.exclude(pk=self.instance.pk)
            if active_in_room.exists():
                raise serializers.ValidationError(
                    {'room': 'This room already has an active tenant.'}
                )
        return attrs

    def update(self, instance, validated_data):
        # If tenant moves out, update room status to vacant
        new_status = validated_data.get('status')
        if new_status == Tenant.STATUS_FORMER and instance.status == Tenant.STATUS_ACTIVE:
            if instance.room:
                instance.room.status = 'vacant'
                instance.room.save(update_fields=['status', 'updated_at'])

        # If tenant is assigned a new active room, mark it occupied
        new_room = validated_data.get('room')
        if new_room and new_status != Tenant.STATUS_FORMER:
            new_room.status = 'occupied'
            new_room.save(update_fields=['status', 'updated_at'])

        return super().update(instance, validated_data)

    def create(self, validated_data):
        tenant = super().create(validated_data)
        # Auto-set room to occupied when tenant is created
        if tenant.room and tenant.status == Tenant.STATUS_ACTIVE:
            tenant.room.status = 'occupied'
            tenant.room.save(update_fields=['status', 'updated_at'])
        return tenant


class TenantListSerializer(serializers.ModelSerializer):
    """Lightweight for list views."""
    full_name = serializers.ReadOnlyField()
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    house_name = serializers.CharField(source='room.house.name', read_only=True)

    class Meta:
        model = Tenant
        fields = [
            'id', 'full_name', 'phone', 'room_number', 'house_name',
            'move_in_date', 'status'
        ]
