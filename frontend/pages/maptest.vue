<template>
  <l-map id="map" ref="map" class="d-flex" :center="center" :zoom="zoom" @ready="hookUpDraw" />
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { LMap, LTileLayer, LGeoJson, LControlLayers, LControl, LControlScale, LWmsTileLayer } from "@vue-leaflet/vue-leaflet";
await import("@geoman-io/leaflet-geoman-free");
// import { useMapLayersStore } from "store/mapLayersStore";

// Reactive property to hold a unique layer
const uniqueLayer = ref(null);

const map = ref(null)
const mapObject = ref(null)
const center = ref([51.505, -0.09])
const zoom = ref(8)
const hookUpDraw = async () => {
  console.log('hookUpDraw', map.value)
  mapObject.value = map.value?.leafletObject
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
  }).addTo(mapObject.value);
  console.log('mapObject.value',mapObject.value)

  // Initialize a marker and add it to the map
  uniqueLayer.value = L.marker(center.value).addTo(mapObject.value );

  // Enable Geoman with only markers and polylines
  mapObject.value.pm.addControls({
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
  mapObject.value.on('pm:create', (e) => {
    // If a layer already exists, remove it before adding a new one
    if (uniqueLayer.value) {
      mapObject.value.valueremoveLayer(uniqueLayer.value);
    }
    uniqueLayer.value = e.layer; // Set the unique layer to the newly created layer
    mapObject.value.valueaddLayer(uniqueLayer.value); // Add the new layer to the map
    console.log('Layer created:', uniqueLayer.value);
  });

  mapObject.value.on('pm:remove', (e) => {
    if (uniqueLayer.value === e.layer) {
      uniqueLayer.value = null; // Clear the unique layer reference
      console.log('Layer removed:', e.layer);
    }
  });

  // Listen for the edit event
  mapObject.value.on('pm:edit', (e) => {
    console.log('Layer edited:', e);
    // You can perform additional actions here based on the edit
  });

  // Listen for the update event
  mapObject.value.on('pm:update', (e) => {
    console.log('Layer updated:', e);
    // You can perform additional actions here based on the update
  });
  if (uniqueLayer.value) {
    uniqueLayer.value.pm.enable();
    uniqueLayer.value.on('pm:edit', (e) => {
      console.log('layer edit', e)
    }) // Enable Geoman controls for the unique layer
  }
}

onMounted(() => {
  // Initialize the map
  // const map = L.map('map').setView([51.505, -0.09], 13);

  // // Add a tile layer
  // L.tileLayer('https://{s}.tile.openstreetmapObject.valueorg/{z}/{x}/{y}.png', {
  //   maxZoom: 19,
  // }).addTo(map);

  // // Initialize a marker and add it to the map
  // uniqueLayer.value = L.marker([51.505, -0.09]).addTo(map);

  // // Enable Geoman with only markers and polylines

});

</script>

<style></style>
