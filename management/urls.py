from django.urls import path
from . import views # Importamos las vistas

urlpatterns = [
    # Cuando alguien visite la URL raíz, se llamará a la función 'room_list' de views.py
    path('', views.room_list, name='room_list'),
    # Añadimos la nueva URL para crear una sala
    path('rooms/new/', views.create_room, name='create_room'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    # AÑADE ESTA LÍNEA PARA ELIMINAR RESERVACIONES
    path('reservations/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
]