<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <display-component />
  </NuxtLayout>
</template>

<script setup lang="ts">
import type { Feature, FeatureCollection } from 'geojson';
import {useDisplay} from 'vuetify'

definePageMeta({
  auth: true
})

const {mobile} = useDisplay()

const coordinatesStore = useCoordinatesStore()
const cableStore = useCablesStore()
const mortalityStore = useMortalityStore()




onMounted (() => {
  console.debug(`the component is now mounted. mobile`, mobile)
})

</script>
