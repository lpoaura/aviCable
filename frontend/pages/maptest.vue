<template>
  <div id="map" style="height: 500px;" />
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
await import("@geoman-io/leaflet-geoman-free");

// Reactive property to hold a unique layer
const uniqueLayer = ref(null);

onMounted(() => {
  // Initialize the map
  const map = L.map('map').setView([51.505, -0.09], 13);

  // Add a tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
  }).addTo(map);

  // Initialize a marker and add it to the map
  uniqueLayer.value = L.marker([51.505, -0.09]).addTo(map);

  // Enable Geoman with only markers and polylines
  map.pm.addControls({
    position: 'topleft',
    drawMarker: true,
    drawPolyline: true,
    drawText: false,
    drawCircleMarker: false,
    drawPolygon: false,
    drawRectangle: false,
    drawCircle: false,
    editMode: true,
    removalMode: true,
  });

  // Add event listeners for Geoman
  map.on('pm:create', (e) => {
    // If a layer already exists, remove it before adding a new one
    if (uniqueLayer.value) {
      map.removeLayer(uniqueLayer.value);
    }
    uniqueLayer.value = e.layer; // Set the unique layer to the newly created layer
    map.addLayer(uniqueLayer.value); // Add the new layer to the map
    console.log('Layer created:', uniqueLayer.value);
  });

  map.on('pm:remove', (e) => {
    if (uniqueLayer.value === e.layer) {
      uniqueLayer.value = null; // Clear the unique layer reference
      console.log('Layer removed:', e.layer);
    }
  });

  // Listen for the edit event
  map.on('pm:edit', (e) => {
    console.log('Layer edited:', e);
    // You can perform additional actions here based on the edit
  });

  // Listen for the update event
  map.on('pm:update', (e) => {
    console.log('Layer updated:', e);
    // You can perform additional actions here based on the update
  });
  if (uniqueLayer.value) {
    uniqueLayer.value.pm.enable();
    uniqueLayer.value.on('pm:edit', (e) => {
      console.log('layer edit', e)
    }) // Enable Geoman controls for the unique layer
  }
});

// Watcher to react to changes in the unique layer
watch(uniqueLayer, (newLayer, oldLayer) => {
  if (newLayer) {
    console.log('Unique layer changed:', newLayer);
    uniqueLayer.value.pm.enable();
    uniqueLayer.value.on("pm:edit", (e) => {
  console.log(e);
}); // Enable Geoman controls for the unique layer
    // You can perform additional actions here based on the unique layer's changes
  } else {
    console.log('Unique layer removed');
  }
});
</script>

<style>
#map {
  height: 100vh;
}
</style>
