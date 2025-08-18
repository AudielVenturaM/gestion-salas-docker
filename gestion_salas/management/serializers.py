from rest_framework import serializers
from .models import MeetingRoom, Reservation

class MeetingRoomSerializer(serializers.ModelSerializer):
    """Serializer para el modelo MeetingRoom."""
    class Meta:
        model = MeetingRoom
        fields = ['id', 'name', 'capacity']


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Reservation."""
    class Meta:
        model = Reservation
        fields = ['id', 'room', 'organizer_name', 'start_time', 'end_time']
        read_only_fields = ['room']