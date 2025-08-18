<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const room = ref(null);
const reservations = ref([]);
const newReservation = ref({ organizer_name: '', start_time: '', end_time: '' });
const errorMessage = ref('');

const fetchData = async () => {
  try {
    const roomId = route.params.id;
    const [roomRes, reservationsRes] = await Promise.all([
      axios.get(`http://localhost:8000/api/rooms/${roomId}/`),
      axios.get(`http://localhost:8000/api/rooms/${roomId}/reservations/`)
    ]);
    room.value = roomRes.data;
    reservations.value = reservationsRes.data;
  } catch (error) {
    console.error("Error al obtener los datos:", error);
    errorMessage.value = "No se pudieron cargar los datos de la sala.";
  }
};

const handleReservationSubmit = async () => {
  errorMessage.value = '';
  try {
    const roomId = route.params.id;
    await axios.post(`http://localhost:8000/api/rooms/${roomId}/reservations/`, newReservation.value);
    newReservation.value = { organizer_name: '', start_time: '', end_time: '' };
    await fetchData();
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Ocurrió un error inesperado al reservar.';
  }
};

const deleteReservation = async (reservationId) => {
  if (confirm('¿Estás seguro de que quieres liberar esta sala?')) {
    try {
      await axios.delete(`http://localhost:8000/api/reservations/${reservationId}/delete/`);
      await fetchData();
    } catch (error) {
      errorMessage.value = 'No se pudo eliminar la reservación.';
    }
  }
};

onMounted(fetchData);
</script>

<template>
  <div v-if="room">
    <button @click="router.push('/')" class="btn btn-sm btn-outline-secondary mb-3">&larr; Volver a la lista</button>
    <h1 class="mt-2">{{ room.name }}</h1>
    <p class="lead">Capacidad: {{ room.capacity }} personas</p>
    <hr />

    <div class="row">
      <div class="col-md-6 mb-4">
        <h2>Próximas Reservaciones</h2>
        <ul class="list-group">
          <li v-for="res in reservations" :key="res.id" class="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <strong>{{ res.organizer_name }}</strong><br>
              <small>{{ new Date(res.start_time).toLocaleString() }} - {{ new Date(res.end_time).toLocaleString() }}</small>
            </div>
            <button @click="deleteReservation(res.id)" class="btn btn-sm btn-outline-danger">Liberar</button>
          </li>
          <p v-if="!reservations.length" class="text-muted mt-3">No hay reservaciones próximas.</p>
        </ul>
      </div>
      <div class="col-md-6">
        <h2>Hacer una Nueva Reservación</h2>
        <div class="card">
          <div class="card-body">
            <form @submit.prevent="handleReservationSubmit">
              <div class="mb-3">
                <label class="form-label">Tu Nombre</label>
                <input type="text" v-model="newReservation.organizer_name" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Hora de Inicio</label>
                <input type="datetime-local" v-model="newReservation.start_time" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Hora de Fin</label>
                <input type="datetime-local" v-model="newReservation.end_time" class="form-control" required />
              </div>
              <button type="submit" class="btn btn-success w-100">Reservar</button>
            </form>
            <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else><p>Cargando sala...</p></div>
</template>
