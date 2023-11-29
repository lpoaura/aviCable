<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="false" /></template>
    <display-component />
  </NuxtLayout>
</template>

<script setup lang="ts">
import {useDisplay} from 'vuetify'

definePageMeta({
  auth: true
})

const {mobile} = useDisplay()

const coordinatesStore = useCoordinatesStore()
const cableStore = useCablesStore()

const bbox : ComputedRef<string> = computed<string>(() => coordinatesStore.mapBounds)
const zoom : ComputedRef<number> = computed<number>(() => coordinatesStore.zoom)

let controller;

watch(bbox, (newVal, _oldVal) => {
  console.log('zoom', zoom.value)
  console.log(controller)
  if (controller) {
    controller.abort();
    console.log("Download aborted");
  }
  controller= new AbortController()
  if (zoom.value > 9) {
    cableStore.getInfrstrData({in_bbox: newVal}, controller)
  }
})

onMounted (() => {
  console.debug(`the component is now mounted. mobile`, mobile)
})

</script>
