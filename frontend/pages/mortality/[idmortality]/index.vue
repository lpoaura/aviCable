<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail-mortality :data="item" />
  </NuxtLayout>
</template>

<script setup lang="ts">
import type { MortalityFeature } from '~/types/mortality'

const route = useRoute()
const coordinateStore = useCoordinatesStore()


const zoomTo = () => {
  // const layer = geoJSON(info.value)
  coordinateStore.setCenter([...item.geometry.coordinates].reverse())
  coordinateStore.setZoom(14)
}

const item = await api.get<MortalityFeature>(`/api/v1/mortality/${route.params.idmortality}`)


onMounted(() => {zoomTo()})

</script>
