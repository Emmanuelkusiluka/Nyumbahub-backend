from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from accounts.permissions import IsAdminOrReadOnly
from .models import House, Room
from .serializers import (
    HouseSerializer, HouseListSerializer, RoomSerializer
)


class HouseListCreateView(generics.ListCreateAPIView):
    queryset = House.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return HouseListSerializer
        return HouseSerializer


class HouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['house', 'status', 'floor']
    search_fields = ['room_number', 'house__name']
    ordering_fields = ['room_number', 'monthly_rent', 'status']

    def get_queryset(self):
        qs = Room.objects.select_related('house').all()
        house_id = self.kwargs.get('house_pk')
        if house_id:
            qs = qs.filter(house_id=house_id)
        return qs

    def perform_create(self, serializer):
        house_id = self.kwargs.get('house_pk')
        if house_id:
            serializer.save(house_id=house_id)
        else:
            serializer.save()


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.select_related('house').all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomStatusUpdateView(APIView):
    """Quick endpoint to update only room status."""
    permission_classes = [IsAdminOrReadOnly]

    def patch(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in dict(Room.STATUS_CHOICES):
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        room.status = new_status
        room.save(update_fields=['status', 'updated_at'])
        return Response(RoomSerializer(room).data)


class OccupancyOverviewView(APIView):
    """Summary of all houses occupancy for the dashboard."""
    def get(self, request):
        houses = House.objects.all()
        data = []
        totals = {'total_rooms': 0, 'occupied': 0, 'vacant': 0, 'maintenance': 0}

        for house in houses:
            entry = {
                'id': house.id,
                'name': house.name,
                'total_rooms': house.total_rooms,
                'occupied': house.occupied_rooms,
                'vacant': house.vacant_rooms,
                'maintenance': house.maintenance_rooms,
                'occupancy_rate': house.occupancy_rate,
            }
            data.append(entry)
            totals['total_rooms'] += house.total_rooms
            totals['occupied'] += house.occupied_rooms
            totals['vacant'] += house.vacant_rooms
            totals['maintenance'] += house.maintenance_rooms

        if totals['total_rooms'] > 0:
            totals['occupancy_rate'] = round(
                (totals['occupied'] / totals['total_rooms']) * 100, 1
            )
        else:
            totals['occupancy_rate'] = 0

        return Response({'houses': data, 'totals': totals})
