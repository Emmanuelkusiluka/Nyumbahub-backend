from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count, Q
from accounts.permissions import IsAdminOrReadOnly
from .models import Payment, Expense
from .serializers import PaymentSerializer, ExpenseSerializer
import datetime


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'method', 'payment_month', 'payment_year', 'tenant']
    search_fields = ['tenant__first_name', 'tenant__last_name', 'mpesa_reference']
    ordering_fields = ['payment_year', 'payment_month', 'amount_due', 'created_at']

    def get_queryset(self):
        return Payment.objects.select_related(
            'tenant', 'tenant__room', 'tenant__room__house', 'recorded_by'
        ).all()


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.select_related(
        'tenant', 'tenant__room', 'tenant__room__house', 'recorded_by'
    ).all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrReadOnly]


class MonthlyPaymentSummaryView(APIView):
    """
    Returns payment summary for a given month/year.
    GET /api/payments/summary/?month=6&year=2025
    """
    def get(self, request):
        month = request.query_params.get('month', datetime.date.today().month)
        year = request.query_params.get('year', datetime.date.today().year)

        payments = Payment.objects.filter(
            payment_month=month, payment_year=year
        ).select_related('tenant', 'tenant__room', 'tenant__room__house')

        total_expected = payments.aggregate(s=Sum('amount_due'))['s'] or 0
        total_collected = payments.aggregate(s=Sum('amount_paid'))['s'] or 0

        summary = {
            'month': int(month),
            'year': int(year),
            'total_expected': total_expected,
            'total_collected': total_collected,
            'total_outstanding': float(total_expected) - float(total_collected),
            'paid_count': payments.filter(status='paid').count(),
            'partial_count': payments.filter(status='partial').count(),
            'unpaid_count': payments.filter(status='unpaid').count(),
            'payments': PaymentSerializer(payments, many=True).data,
        }
        return Response(summary)


class UnpaidTenantsView(APIView):
    """List all tenants with unpaid or partial rent for a given month/year."""
    def get(self, request):
        month = request.query_params.get('month', datetime.date.today().month)
        year = request.query_params.get('year', datetime.date.today().year)

        unpaid = Payment.objects.filter(
            payment_month=month,
            payment_year=year,
            status__in=['unpaid', 'partial']
        ).select_related('tenant', 'tenant__room', 'tenant__room__house')

        return Response(PaymentSerializer(unpaid, many=True).data)


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'house']
    search_fields = ['description', 'house__name']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        qs = Expense.objects.select_related('house', 'recorded_by').all()
        # Filter by year/month if provided
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year:
            qs = qs.filter(date__year=year)
        if month:
            qs = qs.filter(date__month=month)
        return qs


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.select_related('house', 'recorded_by').all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOrReadOnly]
