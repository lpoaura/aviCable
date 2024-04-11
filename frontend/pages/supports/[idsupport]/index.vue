<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map><map-search :edit-mode="false" /></template>
      <data-support-detail :data="info" />
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

const { data: info } = await useHttp(`/api/v1/cables/infrastructures/${route.params.idsupport}`)


watch(info, (value) =>{
  console.log('WATCH value', value)
  if(value) {
    coordinateStore.setCenter([...value.geometry.coordinates].reverse())
    coordinateStore.setZoom(14)
  }
})



// onMounted(() => {})

// // await useHttp(`/api/v1/cables/infrastructures/${route.params.idsupport}`).then(resp => {
// //   console.log('INFO DATA', resp.data)
// //   info.value = resp.data}).then(() => {
// //     console.log(info)
// //     zoomTo()
// //   }
// // )


// // const loadData = async () => {
// //   const {data} = await useHttp(`/api/v1/cables/infrastructures/${route.params.idsupport}`)
// //   info.value = data

// // }

// // watch(route, value => {
// //   loadData()
// //     console.log('watchRoute', value)
// //     idSupport.value=value.params.idsupport
// //     console.log('watchRoute idSupport',idSupport)
// //      console.log('watchRoute info',info.value)
// //   },
// //   {
// //     deep: true,
// //     immediate: true
// //   }
// // )


// // const { data: info } = await useAsyncData(
// //   'info',
// //   () => useHttp(`/api/v1/cables/infrastructures/${route.params.idsupport}`),
// //   {watch: [idSupport]}
// // )
</script>
