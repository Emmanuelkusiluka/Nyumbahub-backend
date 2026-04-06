from rest_framework import serializers
from .models import Payment, Expense


class PaymentSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.full_name', read_only=True)
    room_number = serializers.CharField(source='tenant.room.room_number', read_only=True)
    house_name = serializers.CharField(source='tenant.room.house.name', read_only=True)
    balance = serializers.ReadOnlyField()
    recorded_by_username = serializers.CharField(source='recorded_by.username', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'tenant', 'tenant_name', 'room_number', 'house_name',
            'amount_due', 'amount_paid', 'balance',
            'payment_month', 'payment_year', 'payment_date',
            'method', 'status', 'mpesa_reference', 'notes',
            'recorded_by', 'recorded_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'recorded_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['recorded_by'] = self.context['request'].user
        return super().create(validated_data)


class ExpenseSerializer(serializers.ModelSerializer):
    house_name = serializers.CharField(source='house.name', read_only=True)
    recorded_by_username = serializers.CharField(source='recorded_by.username', read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'house', 'house_name', 'category', 'description',
            'amount', 'date', 'recorded_by', 'recorded_by_username', 'created_at'
        ]
        read_only_fields = ['id', 'recorded_by', 'created_at']

    def create(self, validated_data):
        validated_data['recorded_by'] = self.context['request'].user
        return super().create(validated_data)
