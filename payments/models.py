from django.db import models
from tenants.models import Tenant
from accounts.models import User


class Payment(models.Model):
    METHOD_CASH = 'cash'
    METHOD_MPESA = 'mpesa'
    METHOD_BANK = 'bank'
    METHOD_CHOICES = [
        (METHOD_CASH, 'Cash'),
        (METHOD_MPESA, 'M-Pesa'),
        (METHOD_BANK, 'Bank Transfer'),
    ]

    STATUS_PAID = 'paid'
    STATUS_PARTIAL = 'partial'
    STATUS_UNPAID = 'unpaid'
    STATUS_CHOICES = [
        (STATUS_PAID, 'Paid'),
        (STATUS_PARTIAL, 'Partial'),
        (STATUS_UNPAID, 'Unpaid'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_month = models.PositiveIntegerField()  # 1-12
    payment_year = models.PositiveIntegerField()
    payment_date = models.DateField(null=True, blank=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default=METHOD_CASH)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_UNPAID)
    mpesa_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='recorded_payments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        unique_together = ['tenant', 'payment_month', 'payment_year']
        ordering = ['-payment_year', '-payment_month']

    def __str__(self):
        return f"{self.tenant} - {self.payment_month}/{self.payment_year} ({self.status})"

    @property
    def balance(self):
        return self.amount_due - self.amount_paid

    def save(self, *args, **kwargs):
        # Auto-compute status
        if self.amount_paid >= self.amount_due:
            self.status = self.STATUS_PAID
        elif self.amount_paid > 0:
            self.status = self.STATUS_PARTIAL
        else:
            self.status = self.STATUS_UNPAID
        super().save(*args, **kwargs)


class Expense(models.Model):
    CATEGORY_MAINTENANCE = 'maintenance'
    CATEGORY_UTILITIES = 'utilities'
    CATEGORY_STAFF = 'staff'
    CATEGORY_TAXES = 'taxes'
    CATEGORY_OTHER = 'other'
    CATEGORY_CHOICES = [
        (CATEGORY_MAINTENANCE, 'Maintenance & Repairs'),
        (CATEGORY_UTILITIES, 'Utilities'),
        (CATEGORY_STAFF, 'Staff / Caretaker'),
        (CATEGORY_TAXES, 'Taxes & Fees'),
        (CATEGORY_OTHER, 'Other'),
    ]

    house = models.ForeignKey(
        'properties.House', on_delete=models.CASCADE,
        related_name='expenses', null=True, blank=True
    )
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='recorded_expenses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'expenses'
        ordering = ['-date']

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.date})"
