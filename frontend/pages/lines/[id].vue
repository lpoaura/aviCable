<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail :data="info" @update="updateData()" />
  </NuxtLayout>
</template>

<script setup>
const route = useRoute()

const coordinateStore = useCoordinatesStore()

const { data: info } = await useHttp(`/api/v1/cables/infrastructures/${route.params.id}/`)

const updateData = async () => {
  const { data: info } = await useHttp(`/api/v1/cables/infrastructures/${route.params.id}/`)
}

const zoomTo = () => {
  // const layer = geoJSON(info.value)
  coordinateStore.setCenter([...info.value.geometry.coordinates].reverse())
  coordinateStore.setSelectedFeature(info.value)
  coordinateStore.setZoom(14)
}

onMounted(() => {zoomTo()})

// await useHttp(`/api/v1/cables/infrastructures/${route.params.idsupport}`).then(resp => {
//   console.log('INFO DATA', resp.data)
//   info.value = resp.data}).then(() => {
//     console.log(info)
//     zoomTo()
//   }
// )


// const loadData = async () => {
//   const {data} = await useHttp(`/api/v1/cables/infrastructures/${route.params.idsupport}`)
//   info.value = data

// }

// watch(route, value => {
//   loadData()
//     console.log('watchRoute', value)
//     idSupport.value=value.params.idsupport
//     console.log('watchRoute idSupport',idSupport)
//      console.log('watchRoute info',info.value)
//   },
//   {
//     deep: true,
//     immediate: true
//   }
// )


// const { data: info } = await useAsyncData(
//   'info',
//   () => useHttp(`/api/v1/cables/infrastructures/${route.params.idsupport}`),
//   {watch: [idSupport]}
// )
</script>
