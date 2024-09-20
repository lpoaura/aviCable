<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" :mortality-item="info" /></template>
    <data-detail-mortality :data="item" />
  </NuxtLayout>
</template>

<script setup>
const route = useRoute()
const coordinateStore = useCoordinatesStore()


const zoomTo = () => {
  console.log('coordinateStore',coordinateStore)
  // const layer = geoJSON(info.value)
  coordinateStore.setCenter([...item.value.geometry.coordinates].reverse())
  coordinateStore.setZoom(14)
}

const { data: item } = await useHttp(`/api/v1/mortality/${route.params.idmortality}`)



onMounted(() => {zoomTo()})
// watch(info, _value => zoomTo())

</script>
