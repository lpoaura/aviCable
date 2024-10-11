<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail-infrastructure :data="infrastructure" @update="updateData()" />
  </NuxtLayout>
</template>

<script setup>
import {centroid} from '@turf/centroid';
import {storeToRefs} from 'pinia';
const route = useRoute()

const coordinateStore = useCoordinatesStore()

const { data: infrastructure } = await useHttp(`/api/v1/cables/infrastructures/${route.params.id}/`)

const {selectedFeature,center,zoom} = storeToRefs(coordinateStore)

const updateData = async () => {
  zoomTo()
}

const zoomTo = () => {
  // const layer = geoJSON(info.value)
  // TODO: fix error on lines
  center.value = centroid(infrastructure.value)?.geometry?.coordinates.reverse()
  selectedFeature.value = infrastructure.value
  zoom.value = 14
}

onMounted(() => {zoomTo()})

</script>
