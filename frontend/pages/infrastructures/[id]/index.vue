<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail-infrastructure :data="infrastructure" @update="updateData()" />
  </NuxtLayout>
</template>

<script setup lang=ts>
import { centroid } from '@turf/centroid';
import { storeToRefs } from 'pinia';

import type { CablesFeature } from '~/types/cables'


useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - Infrastructure ${route.params.id}` : 'Infrastructure';
  }
})

const route = useRoute()

const authStore = useAuthStore()
const coordinateStore = useCoordinatesStore()

const { data: infrastructure } = await authStore.authedGet<CablesFeature>(`/api/v1/cables/infrastructures/${route.params.id}/`)

const { selectedFeature, center, zoom } = storeToRefs(coordinateStore)

const updateData = async () => {
  const { data: resp } = await authStore.authedGet<CablesFeature>(`/api/v1/cables/infrastructures/${route.params.id}/`)
  infrastructure.value = resp
  zoomTo()
  title.value = `aviCable - Infrastructure #${route.query.id}`
}

const zoomTo = () => {
  // const layer = geoJSON(info.value)
  // TODO: fix error on lines
  console.debug('zoomTo', infrastructure)
  center.value = centroid(infrastructure.value)?.geometry?.coordinates.reverse()
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
