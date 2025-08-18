from django.contrib import admin
from .models import MeetingRoom, Reservation # Importamos nuestros modelos

# Registramos los modelos para que aparezcan en el panel de admin
admin.site.register(MeetingRoom)
admin.site.register(Reservation)
