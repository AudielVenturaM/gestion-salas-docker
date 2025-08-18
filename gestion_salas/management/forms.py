from django import forms
from .models import MeetingRoom, Reservation

class MeetingRoomForm(forms.ModelForm):
    class Meta:
        model = MeetingRoom
        fields = ['name', 'capacity']
        labels = {
            'name': 'Nombre de la Sala',
            'capacity': 'Capacidad (personas)',
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        # Excluimos 'room' porque lo asignaremos automáticamente en la vista
        fields = ['organizer_name', 'start_time', 'end_time']
        labels = {
            'organizer_name': 'Tu Nombre',
            'start_time': 'Hora de Inicio (ej: 2025-08-16 14:00)',
            'end_time': 'Hora de Fin (ej: 2025-08-16 16:00)',
        }
        # Opcional: widgets para mejorar la experiencia de usuario
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
