<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail-mortality :data="item" />
  </NuxtLayout>
</template>

<script setup>
const route = useRoute()
const authStore = useAuthStore()
const coordinateStore = useCoordinatesStore()


const zoomTo = () => {
  // const layer = geoJSON(info.value)
  coordinateStore.setCenter([...item.value.geometry.coordinates].reverse())
  coordinateStore.setZoom(14)
}

const { data: item } = await authStore.authedGet(`/api/v1/mortality/${route.params.idmortality}`)


onMounted(() => {zoomTo()})

</script>
