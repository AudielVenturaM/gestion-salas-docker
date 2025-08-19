from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import MeetingRoom, Reservation
from .serializers import MeetingRoomSerializer, ReservationSerializer
from rest_framework.permissions import AllowAny

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def room_list_api(request):
    """
    Endpoint de API para listar todas las salas o crear una nueva.
    """
    if request.method == 'GET':
        # Obtiene todos los objetos de sala.
        rooms = MeetingRoom.objects.all()
        # Los traduce a JSON usando el serializer. 'many=True' es necesario para listas de objetos.
        serializer = MeetingRoomSerializer(rooms, many=True)
        # Devuelve los datos en una respuesta de API.
        return Response(serializer.data)

    elif request.method == 'POST':
        # Procesa los datos JSON enviados para crear una nueva sala.
        serializer = MeetingRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def room_detail_api(request, room_id):
    """
    Endpoint de API para ver, actualizar o eliminar una sala específica.
    """
    try:
        room = MeetingRoom.objects.get(pk=room_id)
    except MeetingRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MeetingRoomSerializer(room)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # El 'PUT' actualiza un objeto existente con nuevos datos.
        serializer = MeetingRoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def reservation_list_api(request, room_id):
    """
    Endpoint para listar las reservaciones de una sala o crear una nueva.
    """
    # Verificamos que la sala exista.
    try:
        room = MeetingRoom.objects.get(pk=room_id)
    except MeetingRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Filtramos las reservaciones futuras para esta sala.
        reservations = Reservation.objects.filter(room=room, end_time__gte=timezone.now()).order_by('start_time')
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Al crear una reservación, le asignamos la sala automáticamente.
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            # Aquí replicamos la lógica de validación que teníamos antes.
            # (Esta es una versión simplificada, podrías mover la lógica a un método del serializer)
            validated_data = serializer.validated_data
            start_time = validated_data['start_time']
            end_time = validated_data['end_time']

            # Validar que no se solape
            overlapping = Reservation.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()
            if overlapping:
                return Response({'error': 'La sala ya está ocupada en este horario.'}, status=status.HTTP_400_BAD_REQUEST)

            # Validar duración máxima de 2 horas
            if end_time - start_time > timedelta(hours=2):
                return Response({'error': 'La reservación no puede exceder las 2 horas.'}, status=status.HTTP_400_BAD_REQUEST)

            # Si todo está bien, guardamos la reservación asociada a la sala.
            serializer.save(room=room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def reservation_delete_api(request, reservation_id):
    """
    Endpoint para eliminar una reservación.
    """
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    reservation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)