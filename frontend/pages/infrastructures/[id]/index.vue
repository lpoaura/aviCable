<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail-infrastructure :data="infrastructure" @update="updateData()" />
  </NuxtLayout>
</template>

<script setup lang=ts>
import { centroid } from "@turf/centroid";
import { storeToRefs } from 'pinia';

import type { CablesFeature } from '~/types/cables'


useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - Infrastructure ${route.params.id}` : 'Infrastructure';
  },
  // title: computed(() => `aviCable - Infrastructure #${route.query.id}`)
})


const route = useRoute()

const coordinateStore = useCoordinatesStore()

const infrastructure = await api.get<CablesFeature>(`/api/v1/cables/infrastructures/${route.params.id}/`)

const { selectedFeature, center, zoom } = storeToRefs(coordinateStore)

const updateData = async () => {
  const resp = await api.get<CablesFeature>(`/api/v1/cables/infrastructures/${route.params.id}/`)
  infrastructure.value = resp
  zoomTo()
}

const zoomTo = () => {
  const infraCentroid = centroid(infrastructure)
  center.value = infraCentroid?.geometry.coordinates.reverse()
  selectedFeature.value = infrastructure.value
  zoom.value = 14
}

watch(infrastructure.value, () => {
  zoomTo()
})

onMounted(() => {
  zoomTo()
})

</script>
