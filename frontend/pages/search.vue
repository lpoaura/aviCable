<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map><map-search :edit-mode="false" /></template>
      <display-component />
    </NuxtLayout>
  </v-container>
</template>

<script setup lang="ts">
import type { FeatureCollection } from 'geojson';
import {useDisplay} from 'vuetify'

definePageMeta({
  middleware: 'auth',
  layout: false
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
  if (zoom.value >= 10) {
    cableStore.getInfrstrData({in_bbox: newVal}, abortController.value)
    mortalityStore.getMortalityData({in_bbox: newVal}, abortController.value)

  } else {
    cableStore.setInfrstrData({})
    cableStore.setInfrstrDataLoadingStatus(false)
    mortalityStore.setMortalityData({} as FeatureCollection)
  }
})

onMounted (() => {
  console.debug(`the component is now mounted. mobile`, mobile)
})

</script>
