<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map><map-search :edit-mode="false" :mortalityItem="info" /></template>
      <data-mortality-detail :data="info" />
    </NuxtLayout>
  </v-container>
</template>

<script setup>
import {useCoordinatesStore} from '../../../store/coordinatesStore';
import {geoJSON} from 'leaflet'

definePageMeta({
  middleware: 'auth',
  layout: false
})

const route = useRoute()

const coordinateStore = useCoordinatesStore()


const zoomTo = () => {
  console.log('coordinateStore',coordinateStore)
  // const layer = geoJSON(info.value)
  coordinateStore.setCenter([...info.value.geometry.coordinates].reverse())
  coordinateStore.setZoom(14)
}

const { data: info } = await useHttp(`/api/v1/mortality/${route.params.idmortality}`)



onMounted(() => {zoomTo()})
// watch(info, _value => zoomTo())

</script>
