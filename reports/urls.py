from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardSummaryView.as_view(), name='dashboard'),
    path('monthly/', views.MonthlyReportView.as_view(), name='monthly_report'),
    path('yearly/', views.YearlyReportView.as_view(), name='yearly_report'),
    path('by-house/', views.HouseReportView.as_view(), name='house_report'),
    path('expenses/by-category/', views.ExpenseByCategoryView.as_view(), name='expense_by_category'),
    path('room/<int:room_id>/history/', views.RentalHistoryView.as_view(), name='room_history'),
]
