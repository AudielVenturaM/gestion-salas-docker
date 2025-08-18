from django.urls import path
from . import views # Importamos las vistas

urlpatterns = [
    # URL para la lista de salas: /api/rooms/
    path('rooms/', views.room_list_api, name='room_list_api'),
    # URL para los detalles de una sala: /api/rooms/1/
    path('rooms/<int:room_id>/', views.room_detail_api, name='room_detail_api'),
    path('rooms/<int:room_id>/reservations/', views.reservation_list_api, name='reservation_list_api'),
    path('reservations/<int:reservation_id>/delete/', views.reservation_delete_api, name='reservation_delete_api'),
]