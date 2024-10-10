<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail-infrastructure :data="infrastructure" @update="updateData()" />
  </NuxtLayout>
</template>

<script setup>

const route = useRoute()

const coordinateStore = useCoordinatesStore()

const { data: infrastructure } = await useHttp(`/api/v1/cables/infrastructures/${route.params.id}/`)

const updateData = async () => {
  zoomTo()
}

const zoomTo = () => {

  console.log('zoomTo', infrastructure.value)
  // const layer = geoJSON(info.value)
  // TODO: fix error on lines
  // coordinateStore.setCenter([...infrastructure.value.geometry.coordinates].reverse())
  coordinateStore.setSelectedFeature(infrastructure.value)
  coordinateStore.setZoom(14)
}

onMounted(() => {zoomTo()})

</script>
