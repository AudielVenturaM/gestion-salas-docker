from django.db import models

class MeetingRoom(models.Model):
    """Respresenta una sal de juntas física en la oficina."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Sala")
    capacity = models.PositiveIntegerField(verbose_name="Capacidad")

    def __str__(self):
        """Devuelve una representación en texto del modelo, útil para el admin."""
        return f"{self.name} (Capacidad: {self.capacity})"

class Reservation(models.Model):
    """Representa la reservación de una sala para un rango de tiempo específico."""
    room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, verbose_name="Sala")
    organizer_name = models.CharField(max_length=100, verbose_name="Nombre del Organizador")
    start_time = models.DateTimeField(verbose_name="Hora de Inicio")
    end_time = models.DateTimeField(verbose_name="Hora de Fin")

    def __str__(self):
        """Devuelve una representación legible de la reservación."""
        # Formateamos la fecha para que sea más legible
        start = self.start_time.strftime("%d/%m/%Y %H:%M")
        end = self.end_time.strftime("%H:%M")
        return f"Reserva en '{self.room.name}' por '{self.organizer_name}' de {start} a {end}"