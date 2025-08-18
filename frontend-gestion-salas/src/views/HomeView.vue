<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
const rooms = ref([]);
onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/rooms/');
    rooms.value = response.data;
  } catch (error) {
    console.error("Hubo un error al obtener las salas:", error);
  }
});
</script>

<template>
  <main>
    <h1 class="mb-4">Salas de Juntas Disponibles</h1>
    <div class="row">
      <div v-for="room in rooms" :key="room.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ room.name }}</h5>
            <p class="card-text">Capacidad: {{ room.capacity }} personas</p>
            <router-link :to="{ name: 'RoomDetail', params: { id: room.id } }" class="btn btn-primary mt-auto">
              Ver detalles y reservar
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
