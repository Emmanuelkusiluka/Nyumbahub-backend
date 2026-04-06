from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentListCreateView.as_view(), name='payment_list'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('summary/', views.MonthlyPaymentSummaryView.as_view(), name='payment_summary'),
    path('unpaid/', views.UnpaidTenantsView.as_view(), name='unpaid_tenants'),
    path('expenses/', views.ExpenseListCreateView.as_view(), name='expense_list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
]
