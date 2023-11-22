<template>
  <div>
    <v-data-table fixed-header height="100%" :headers="headers" :search="search"
      :items="mortalityStore.getMortalityFeatures" :loading="!mortalityStore.getMortalityFeatures" loading-text="Loading... Please wait" item-value="name"
      class="elevation-1" density="compact" @click:row="showDetail"></v-data-table>
  </div>
</template> 

<script setup lang="ts">
// import { FeatureCollection } from 'geojson'
const router =useRouter()
const search = ref('')
const itemsPerPage=ref(5)
const mortalityData = ref([])
const headers = reactive([
  {title: 'ID', align: 'start',sortable:true, key: 'id'},
  {title: 'Nom vernaculaire', align: 'start',sortable:true, key: 'properties.species.vernacular_name'},
  {title: 'Nom scientifique', align: 'start',sortable:true, key: 'properties.species.scientific_name'},
  {title: 'Date', align: 'center',sortable:true, key: 'properties.date'},
  {title: 'Cause', align: 'center',sortable:true, key: 'properties.death_cause.label'},
])

const mortalityStore = useMortalityStore()

const showDetail = (_, {item}) => {
  const rowData = item.columns
  router.push(`/mortality/${rowData['id']}`)
}

onMounted(() => {
  // setInfrstrData({})
  mortalityStore.getMortalityData()
})
</script>

<style>
.v-data-table /deep/ .v-data-table__wrapper {
  overflow: unset;
}
</style>