from django.db import models


class House(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'houses'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total_rooms(self):
        return self.rooms.count()

    @property
    def occupied_rooms(self):
        return self.rooms.filter(status=Room.STATUS_OCCUPIED).count()

    @property
    def vacant_rooms(self):
        return self.rooms.filter(status=Room.STATUS_VACANT).count()

    @property
    def maintenance_rooms(self):
        return self.rooms.filter(status=Room.STATUS_MAINTENANCE).count()

    @property
    def occupancy_rate(self):
        total = self.total_rooms
        if total == 0:
            return 0
        return round((self.occupied_rooms / total) * 100, 1)


class Room(models.Model):
    STATUS_VACANT = 'vacant'
    STATUS_OCCUPIED = 'occupied'
    STATUS_MAINTENANCE = 'maintenance'
    STATUS_CHOICES = [
        (STATUS_VACANT, 'Vacant'),
        (STATUS_OCCUPIED, 'Occupied'),
        (STATUS_MAINTENANCE, 'Under Maintenance'),
    ]

    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_VACANT)
    description = models.TextField(blank=True)
    floor = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rooms'
        unique_together = ['house', 'room_number']
        ordering = ['house', 'room_number']

    def __str__(self):
        return f"{self.house.name} - Room {self.room_number}"
