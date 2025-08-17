from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone  # <-- Importante para manejar fechas y horas
from datetime import timedelta  # <-- Importa timedelta
from django.core.exceptions import ValidationError  # <-- Importa ValidationError
from .models import MeetingRoom, Reservation
from .forms import MeetingRoomForm, ReservationForm  # <-- Importa el nuevo formulario

def room_list(request):
    # 1. Obtenemos todos los objetos del modelo MeetingRoom de la base de datos.
    rooms = MeetingRoom.objects.all()
    # 2. Creamos un "contexto", que es un diccionario para pasar datos a la plantilla.
    context = {
        'rooms': rooms,
    }
    # 3. Renderizamos (dibujamos) la plantilla HTML pasándole los datos del contexto.
    return render(request, 'management/room_list.html', context)

# Esta es la nueva vista para crear salas
def create_room(request):
    if request.method == 'POST':
        # Si el método es POST, significa que el usuario ha enviado el formulario
        form = MeetingRoomForm(request.POST)
        if form.is_valid():
            form.save() # Guarda el nuevo objeto en la base de datos
            return redirect('room_list') # Redirige al usuario a la lista de salas
    else:
        # Si el método es GET, se muestra un formulario vacío
        form = MeetingRoomForm()

    # Renderiza la plantilla con el formulario
    return render(request, 'management/create_room.html', {'form': form})

# AÑADE ESTA NUEVA VISTA
def room_detail(request, room_id):
    room = get_object_or_404(MeetingRoom, pk=room_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.room = room

            try:
                # LAS LÍNEAS DE PYTZ HAN SIDO ELIMINADAS.
                # AHORA TRABAJAMOS DIRECTAMENTE CON LAS FECHAS DEL FORMULARIO.

                if reservation.start_time >= reservation.end_time:
                    raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

                duration = reservation.end_time - reservation.start_time
                if duration > timedelta(hours=2):
                    raise ValidationError("La reservación no puede exceder las 2 horas.")

                overlapping_reservations = Reservation.objects.filter(
                    room=room,
                    start_time__lt=reservation.end_time,
                    end_time__gt=reservation.start_time
                ).exists()

                if overlapping_reservations:
                    raise ValidationError("La sala ya está ocupada en este horario. Por favor, elige otro.")

                reservation.save()
                return redirect('room_detail', room_id=room.id)

            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ReservationForm()

    reservations = Reservation.objects.filter(room=room, end_time__gte=timezone.now()).order_by('start_time')

    context = {
        'room': room,
        'reservations': reservations,
        'form': form,
    }
    return render(request, 'management/room_detail.html', context)


def delete_reservation(request, reservation_id):
    # Busca la reservación o muestra un error 404 si no existe
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    # Guarda el ID de la sala antes de borrar la reservación para saber a dónde volver
    room_id = reservation.room.id

    # Por seguridad, es una buena práctica que las eliminaciones se hagan vía POST
    if request.method == 'POST':
        reservation.delete()
        # Redirige de vuelta a la página de detalles de la sala
        return redirect('room_detail', room_id=room_id)

    # Si alguien intenta acceder a la URL vía GET, simplemente lo redirigimos
    return redirect('room_detail', room_id=room_id)