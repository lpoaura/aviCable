<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <data-detail-infrastructure :data="infrastructure" @update="onUpdate()" />
  </NuxtLayout>
</template>

<script setup lang=ts>
import { centroid } from "@turf/centroid";
import { storeToRefs } from 'pinia';

import type { CablesFeature } from '~/types/cables'

definePageMeta({
  middleware: 'auth',
})


useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - Infrastructure ${route.params.id}` : 'Infrastructure';
  },
  // title: computed(() => `aviCable - Infrastructure #${route.query.id}`)
})


const route = useRoute()

const coordinateStore = useCoordinatesStore()


const {
  data: infrastructure,
  refresh
} = await useAsyncData(
  `infrastructure-${route.params.id}`,
  () => api.get<CablesFeature>(
    `/api/v1/cables/infrastructures/${route.params.id}/`
  )
)

const { selectedFeature, center, zoom } = storeToRefs(coordinateStore)

const onUpdate = async () => {
  console.log('get update')
  await refresh()
  zoomTo()
}

const zoomTo = () => {
  console.log('infrastructure', infrastructure.value)
  const infraCentroid = centroid(infrastructure.value)
  console.log('infraCentroid', infraCentroid)
  center.value = infraCentroid?.geometry.coordinates.reverse()
  selectedFeature.value = infrastructure.value
  zoom.value = 14
}

watch(infrastructure, () => {
  zoomTo()
})

onMounted(() => {
  zoomTo()
})

</script>
