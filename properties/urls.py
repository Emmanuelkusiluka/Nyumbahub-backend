from django.urls import path
from . import views

urlpatterns = [
    # Houses
    path('houses/', views.HouseListCreateView.as_view(), name='house_list'),
    path('houses/<int:pk>/', views.HouseDetailView.as_view(), name='house_detail'),

    # Rooms (all or per-house)
    path('rooms/', views.RoomListCreateView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('rooms/<int:pk>/status/', views.RoomStatusUpdateView.as_view(), name='room_status'),

    # Rooms nested under house
    path('houses/<int:house_pk>/rooms/', views.RoomListCreateView.as_view(), name='house_room_list'),

    # Dashboard overview
    path('occupancy/', views.OccupancyOverviewView.as_view(), name='occupancy_overview'),
]
