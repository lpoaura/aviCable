<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail-infrastructure :data="infrastructure" @update="updateData()" />
  </NuxtLayout>
</template>

<script setup lang=ts>
import {centroid} from '@turf/centroid';
import { storeToRefs } from 'pinia';


useHead({
  titleTemplate : (titleChunk) => {
    return titleChunk ? `${titleChunk} - Infrastructure ${route.params.id}` : 'Infrastructure';
  }
})

const route = useRoute()
const coordinateStore = useCoordinatesStore()

const { data: infrastructure } = await useApi(`/api/v1/cables/infrastructures/${route.params.id}/`)

const {selectedFeature,center,zoom} = storeToRefs(coordinateStore)

const updateData = async () => {
  const { data: resp } = await useApi(`/api/v1/cables/infrastructures/${route.params.id}/`)
  infrastructure.value = resp
  zoomTo()
  title.value = `aviCable - Infrastructure #${route.query.id}`
}

const zoomTo = () => {
  // const layer = geoJSON(info.value)
  // TODO: fix error on lines
  center.value = centroid(infrastructure.value)?.geometry?.coordinates.reverse()
  selectedFeature.value = infrastructure.value
  zoom.value = 14
}

onMounted(() => {
  zoomTo()
})

</script>
