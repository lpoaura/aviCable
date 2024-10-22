<template>
  <v-container fill-height fluid>
    <l-map :zoom="zoom" :center="center" style="height: 500px; width: 100%">
      <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" :attribution="attribution" />
      <l-geo-json ref="layer0" :geojson="geoJsonLayers[0]" :options="geoJsonOptions" @add="bringToFront()" />
      <l-geo-json ref="layer1" :geojson="geoJsonLayers[1]" :options="geoJsonOptions" @add="bringToFront()" />
      <l-geo-json ref="layer2" :geojson="geoJsonLayers[2]" :options="geoJsonOptions" @add="bringToFront()" />
    </l-map>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { LMap, LTileLayer, LGeoJson } from "@vue-leaflet/vue-leaflet";
import 'leaflet/dist/leaflet.css';

// Map center and zoom level
const layer1 = ref()
const center = ref([51.505, -0.09]); // Common location
const zoom = ref(13);
const attribution = ref('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')

// GeoJSON data for three layers
const geoJsonLayers = ref([
  {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        properties: { name: 'Point A 1', color: 'red', size:3},
        geometry: {
          type: 'Point',
          coordinates: [-0.09, 51.505], // Point 1
        },
      },
    ],
  },
  {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        properties: { name: 'Point B 2', color: 'green', size:5 },
        geometry: {
          type: 'Point',
          coordinates: [-0.08, 51.506], // Point 2
        },
      },
      {
        type: 'Feature',
        properties: { name: 'Point B 1', color: 'green', size:5  },
        geometry: {
          type: 'Point',
          coordinates: [-0.09, 51.505], // Point 1
        },
      },
    ],
  },
  {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        properties: { name: 'Point C 3', color: 'blue', size:10  },
        geometry: {
          type: 'Point',
          coordinates: [-0.07, 51.507], // Point 3
        },
      },
      {
        type: 'Feature',
        properties: { name: 'Point C 2', color: 'blue', size:10 },
        geometry: {
          type: 'Point',
          coordinates: [-0.08, 51.506], // Point 2
        },
      },
    ],
  },
]);

const bringToFront = () => {
  layer1.value?.leafletObject?.bringToFront()
  console.log(layer1.value?.leafletObject?.bringToFront())
}

// CircleMarker options
const geoJsonOptions = {
  pointToLayer: (feature, latlng) => {
    console.log('feature', feature )
    return L.circleMarker(latlng, {
      radius: feature.properties.size,
      fillColor: feature.properties.color,
      color: '#000',
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8,
    });
  },
};
</script>

<style scoped>
/* Add any additional styles here */
</style>
