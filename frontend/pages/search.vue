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
const abortController : Ref<AbortController | undefined> = ref<AbortController|undefined>(undefined)

const coordinatesStore = useCoordinatesStore()
const cableStore = useCablesStore()
const mortalityStore = useMortalityStore()

const bbox : ComputedRef<string|null> = computed<string|null>(() => coordinatesStore.mapBounds)
const zoom : ComputedRef<number> = computed<number>(() => coordinatesStore.zoom)

watch(bbox, (newVal, _oldVal) => {
  console.log('zoom', zoom.value)
  console.log(abortController)
  if (abortController.value) {
    abortController.value.abort();
    console.log("Download aborted");
  }
  abortController.value = new AbortController()
  if (zoom.value >= 9) {
    cableStore.getInfrstrData({in_bbox: newVal}, abortController.value)
    mortalityStore.getMortalityData({in_bbox: newVal}, abortController.value)

  } else {
    cableStore.setInfrstrData({})
    cableStore.setInfrstrDataLoadingStatus(false)
  }
})

onMounted (() => {
  console.debug(`the component is now mounted. mobile`, mobile)
})

</script>
