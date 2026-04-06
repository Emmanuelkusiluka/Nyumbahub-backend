from django.urls import path
from . import views

urlpatterns = [
    path('', views.TenantListCreateView.as_view(), name='tenant_list'),
    path('<int:pk>/', views.TenantDetailView.as_view(), name='tenant_detail'),
]
