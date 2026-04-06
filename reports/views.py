from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from properties.models import House, Room
from tenants.models import Tenant
from payments.models import Payment, Expense
import datetime


class DashboardSummaryView(APIView):
    """
    Main dashboard stats — single endpoint the React app loads on home screen.
    GET /api/reports/dashboard/
    """
    def get(self, request):
        today = datetime.date.today()
        month = today.month
        year = today.year

        # Property overview
        total_rooms = Room.objects.count()
        occupied = Room.objects.filter(status='occupied').count()
        vacant = Room.objects.filter(status='vacant').count()
        maintenance = Room.objects.filter(status='maintenance').count()

        # Tenants
        active_tenants = Tenant.objects.filter(status='active').count()

        # This month payments
        month_payments = Payment.objects.filter(payment_month=month, payment_year=year)
        collected = month_payments.aggregate(s=Sum('amount_paid'))['s'] or 0
        expected = month_payments.aggregate(s=Sum('amount_due'))['s'] or 0
        paid_count = month_payments.filter(status='paid').count()
        unpaid_count = month_payments.filter(status__in=['unpaid', 'partial']).count()

        # This month expenses
        month_expenses = Expense.objects.filter(
            date__month=month, date__year=year
        ).aggregate(s=Sum('amount'))['s'] or 0

        return Response({
            'today': today.isoformat(),
            'properties': {
                'total_rooms': total_rooms,
                'occupied': occupied,
                'vacant': vacant,
                'maintenance': maintenance,
                'occupancy_rate': round((occupied / total_rooms * 100), 1) if total_rooms else 0,
                'total_houses': House.objects.count(),
            },
            'tenants': {
                'active': active_tenants,
            },
            'this_month': {
                'month': month,
                'year': year,
                'rent_expected': float(expected),
                'rent_collected': float(collected),
                'rent_outstanding': float(expected) - float(collected),
                'paid_tenants': paid_count,
                'unpaid_tenants': unpaid_count,
                'expenses': float(month_expenses),
                'net_income': float(collected) - float(month_expenses),
            },
        })


class MonthlyReportView(APIView):
    """
    Income vs expenses per month for a given year.
    GET /api/reports/monthly/?year=2025
    """
    def get(self, request):
        year = int(request.query_params.get('year', datetime.date.today().year))

        monthly_data = []
        for month in range(1, 13):
            income = Payment.objects.filter(
                payment_year=year, payment_month=month
            ).aggregate(s=Sum('amount_paid'))['s'] or 0

            expenses = Expense.objects.filter(
                date__year=year, date__month=month
            ).aggregate(s=Sum('amount'))['s'] or 0

            monthly_data.append({
                'month': month,
                'income': float(income),
                'expenses': float(expenses),
                'net': float(income) - float(expenses),
            })

        total_income = sum(m['income'] for m in monthly_data)
        total_expenses = sum(m['expenses'] for m in monthly_data)

        return Response({
            'year': year,
            'months': monthly_data,
            'totals': {
                'income': total_income,
                'expenses': total_expenses,
                'net': total_income - total_expenses,
            }
        })


class YearlyReportView(APIView):
    """
    Year-by-year summary.
    GET /api/reports/yearly/
    """
    def get(self, request):
        years = Payment.objects.values_list('payment_year', flat=True).distinct().order_by('payment_year')

        data = []
        for year in years:
            income = Payment.objects.filter(payment_year=year).aggregate(
                s=Sum('amount_paid')
            )['s'] or 0
            expenses = Expense.objects.filter(date__year=year).aggregate(
                s=Sum('amount')
            )['s'] or 0
            data.append({
                'year': year,
                'income': float(income),
                'expenses': float(expenses),
                'net': float(income) - float(expenses),
            })

        return Response(data)


class HouseReportView(APIView):
    """
    Per-house income, expenses and occupancy for a year.
    GET /api/reports/by-house/?year=2025
    """
    def get(self, request):
        year = int(request.query_params.get('year', datetime.date.today().year))
        houses = House.objects.all()
        data = []

        for house in houses:
            # Income: payments from tenants in this house
            income = Payment.objects.filter(
                payment_year=year,
                tenant__room__house=house
            ).aggregate(s=Sum('amount_paid'))['s'] or 0

            expenses = Expense.objects.filter(
                date__year=year, house=house
            ).aggregate(s=Sum('amount'))['s'] or 0

            data.append({
                'house_id': house.id,
                'house_name': house.name,
                'total_rooms': house.total_rooms,
                'occupied_rooms': house.occupied_rooms,
                'occupancy_rate': house.occupancy_rate,
                'income': float(income),
                'expenses': float(expenses),
                'net': float(income) - float(expenses),
            })

        return Response({'year': year, 'houses': data})


class ExpenseByCategoryView(APIView):
    """
    Expense breakdown by category for a given period.
    GET /api/reports/expenses/by-category/?year=2025&month=6
    """
    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        qs = Expense.objects.all()
        if year:
            qs = qs.filter(date__year=year)
        if month:
            qs = qs.filter(date__month=month)

        breakdown = qs.values('category').annotate(
            total=Sum('amount'), count=Count('id')
        ).order_by('-total')

        return Response(list(breakdown))


class RentalHistoryView(APIView):
    """
    Full rental history for a specific room.
    GET /api/reports/room/<room_id>/history/
    """
    def get(self, request, room_id):
        from tenants.serializers import TenantSerializer
        tenants = Tenant.objects.filter(room_id=room_id).select_related(
            'room', 'room__house'
        ).order_by('-move_in_date')
        return Response(TenantSerializer(tenants, many=True).data)
