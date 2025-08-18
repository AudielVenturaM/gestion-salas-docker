# --- Importaciones Necesarias ---
from django.test import TestCase  # La clase base para todas las pruebas en Django.
from django.urls import reverse  # Permite buscar URLs por su nombre, en lugar de escribirlas a mano.
from django.utils import timezone  # Para manejar fechas y horas "conscientes" de su zona horaria.
from django.conf import settings  # Para acceder a la configuración del proyecto, como TIME_ZONE.
from datetime import timedelta, datetime  # Para manipular fechas y horas.
import pytz  # Librería para un manejo robusto de zonas horarias.

# Importamos los modelos que vamos a probar.
from .models import MeetingRoom, Reservation


# --- Grupo de Pruebas para el Modelo MeetingRoom ---
class MeetingRoomModelTest(TestCase):

    def test_meeting_room_creation(self):
        """Prueba que se puede crear una sala y que su representación en texto es correcta."""
        # Creamos una instancia de MeetingRoom en la base de datos de prueba.
        room = MeetingRoom.objects.create(name="Sala de Pruebas", capacity=15)

        # Verificamos que los atributos se guardaron correctamente.
        self.assertEqual(room.name, "Sala de Pruebas")
        self.assertEqual(room.capacity, 15)
        # Verificamos que el método __str__ devuelve el formato esperado.
        self.assertEqual(str(room), "Sala de Pruebas (Capacidad: 15)")


# --- Grupo de Pruebas para la Vista de Lista de Salas ---
class RoomListViewTest(TestCase):

    def test_view_url_exists_at_proper_location(self):
        """Prueba que la URL raíz ('/') carga exitosamente."""
        # self.client es un navegador web simulado. Hacemos una petición GET a la página principal.
        response = self.client.get('/')
        # Verificamos que la página respondió con un código 200 (OK).
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Prueba que la vista usa la plantilla HTML correcta."""
        # Usamos reverse() para obtener la URL a partir de su nombre ('room_list'). Es más robusto que usar '/'.
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code, 200)
        # Verificamos que Django usó este archivo HTML para generar la respuesta.
        self.assertTemplateUsed(response, 'management/room_list.html')


# --- Grupo de Pruebas para la Lógica de Negocio de las Reservaciones ---
class ReservationLogicTest(TestCase):

    def setUp(self):
        """
        Este método especial se ejecuta ANTES de cada 'test_' en esta clase.
        Es ideal para configurar un estado inicial consistente para las pruebas.
        """
        self.room = MeetingRoom.objects.create(name="Sala para Lógica", capacity=5)

        # Obtenemos la zona horaria definida en settings.py para asegurar consistencia.
        local_tz = pytz.timezone(settings.TIME_ZONE)
        # Creamos fechas "ingenuas" (sin zona horaria) para tener control total.
        start_naive = datetime(2025, 8, 17, 15, 0)  # 3:00 PM
        end_naive = datetime(2025, 8, 17, 16, 0)  # 4:00 PM
        # Las convertimos en fechas "conscientes" usando nuestra zona horaria.
        start_aware = local_tz.localize(start_naive)
        end_aware = local_tz.localize(end_naive)

        # Creamos una reservación base que existirá en la BD para cada prueba.
        self.existing_reservation = Reservation.objects.create(
            room=self.room,
            organizer_name="Juan Perez",
            start_time=start_aware,
            end_time=end_aware
        )

    def test_prevent_overlapping_reservation(self):
        """
        Prueba la regla de negocio más importante: que no se pueda crear una
        reservación si su horario se solapa con una ya existente.
        """
        # ARRANGE (Preparar): Calculamos un horario que sabemos que entra en conflicto.
        # Este nuevo horario empieza 30 mins ANTES de que termine la reservación existente.
        overlapping_start_time = self.existing_reservation.end_time - timedelta(minutes=30)
        overlapping_end_time = overlapping_start_time + timedelta(hours=1)

        # Convertimos las fechas a formato de string, tal como lo haría un formulario HTML.
        start_str = overlapping_start_time.strftime('%Y-%m-%dT%H:%M')
        end_str = overlapping_end_time.strftime('%Y-%m-%dT%H:%M')

        # ACT (Actuar): Simulamos que un usuario envía el formulario con los datos conflictivos.
        response = self.client.post(reverse('room_detail', kwargs={'room_id': self.room.id}), {
            'organizer_name': 'Ana Lopez',
            'start_time': start_str,
            'end_time': end_str,
        })

        # ASSERT (Verificar): Comprobamos que el sistema se comportó como esperábamos.
        # 1. El código de estado debe ser 200, no 302. Esto significa que la página
        #    se volvió a mostrar con un error, en lugar de redirigir por un éxito.
        self.assertEqual(response.status_code, 200)

        # 2. El mensaje de error específico debe estar presente en el HTML de la respuesta.
        self.assertContains(response, "La sala ya está ocupada en este horario.")

        # 3. La cantidad de reservaciones en la BD debe seguir siendo 1. Esto confirma
        #    que la reservación inválida no se guardó.
        self.assertEqual(self.room.reservation_set.count(), 1)