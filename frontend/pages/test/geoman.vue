<template>
  <div>
    <l-map ref="map" :zoom="zoom" :center="center">
      <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
    </l-map>
  </div>
</template>

<script setup lang="ts">

// Import Geoman
import '@geoman-io/leaflet-geoman-free';
import leaflet from 'leaflet'

// Initialize Geoman
leaflet.Map.addInitHook('addHandler', 'geoman', leaflet.Control.Geoman);

const zoom = ref(13);
const center = ref({lat: 51.505, lng:-0.09});
const map : Ref<typeof LMap|null> = ref(null)

onMounted(() => {
  if ($refs.map) {
    // Add Geoman toolbar to the map
    map.value.pm.addControls();
  }
});
</script>
