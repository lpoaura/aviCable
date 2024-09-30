<template>
  <div>
    <h1>Infrastructure Data</h1>
    <div>
      <v-btn @click="cancelRequest">Cancel</v-btn><v-btn
        @click="cablesStore.getInfstrData(/* params */)">Populate</v-btn>
    </div>
    <div v-if="infstrDataLoadingStatus">Loading...</div>

    <div v-else>
      <pre>{{ infstrData }}</pre>
    </div>
  </div>
</template>

<script setup>
// import type {FeatureCollection} from 'geojson';
import { storeToRefs } from 'pinia'

// Use the store
const cablesStore = useCablesStore()

// Destructure the store's state using storeToRefs
const { infstrData, infstrDataLoadingStatus } = storeToRefs(cablesStore)

// Optionally, you can call actions to fetch data
await cablesStore.getInfstrData(/* params */)

const cancelRequest = () => {
  console.log('cancel')
  cablesStore.cancelRequest()
  infstrData.value = {}
}
</script>
