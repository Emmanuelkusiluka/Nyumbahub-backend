from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsAdminOrReadOnly
from .models import Tenant
from .serializers import TenantSerializer, TenantListSerializer


class TenantListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'room', 'room__house']
    search_fields = ['first_name', 'last_name', 'phone', 'email', 'national_id']
    ordering_fields = ['last_name', 'move_in_date', 'created_at']

    def get_queryset(self):
        return Tenant.objects.select_related('room', 'room__house').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TenantListSerializer
        return TenantSerializer


class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.select_related('room', 'room__house').all()
    serializer_class = TenantSerializer
    permission_classes = [IsAdminOrReadOnly]
