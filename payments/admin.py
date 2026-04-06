from django.contrib import admin
from .models import Payment, Expense


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'payment_month', 'payment_year', 'amount_due', 'amount_paid', 'status', 'method']
    list_filter = ['status', 'method', 'payment_year', 'payment_month']
    search_fields = ['tenant__first_name', 'tenant__last_name', 'mpesa_reference']
    readonly_fields = ['status', 'created_at', 'updated_at']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'category', 'house', 'amount', 'date']
    list_filter = ['category', 'house']
    search_fields = ['description']
