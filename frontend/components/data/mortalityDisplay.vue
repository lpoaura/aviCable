<template>
  <div>
    <v-card>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-select clearable v-model="specie" label="Espèce" :items="speciesList" item-title="state" item-value="value"
              variant="outlined" density="compact"></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line variant="outlined"
              hide-details density="compact"></v-text-field>
          </v-col>
        </v-row>

      </v-card-text>
    </v-card>
    <!-- <v-list>
      <v-list-item v-for="item in observationList" :key="item">
        {{ item }}
      </v-list-item>
    </v-list> -->
   <v-data-table v-model="selected" fixed-header height="100%" :headers="headers" :search="search"
      :items="observationList" :loading="!mortalityStore.getMortalityFeatures"
      loading-text="Loading... Please wait" item-value="name" class="elevation-1" density="compact"
      @click:row="handleRowClick" show-select>
      <template v-slot:item.id="{ value, item }">
        <v-chip prepend-icon="mdi-eye-circle-outline" color="primary">
          {{ value }}
        </v-chip>
      </template>
      <template v-slot:item.properties.death_cause.label="{ value , item}">
        <v-chip>
          <v-icon :color="'red'">
            {{deathCauseIcons[item.properties?.death_cause.code] || 'mdi-help' }}
          </v-icon> {{ value }}
        </v-chip>
      </template>
    </v-data-table> 
  </div>
</template> 

<script setup lang="ts">

import type {GeoJSON} from 'geojson'
// import { FeatureCollection } from 'geojson'
const router = useRouter()
const search = ref('')
const selected= ref([])
const specie = ref(null)
const deathCauseIcons = ref({
  COD_EL: 'mdi-lightning-bolt',
  COD_IM:'mdi-star',
  COD_UNKNOWN: 'mdi-help'
})
const headers = reactive([
  {title: 'ID', align: 'start',sortable:true, key: 'id'},
  {title: 'Nom vernaculaire', align: 'start',sortable:true, key: 'properties.species.vernacular_name'},
  {title: 'Nom scientifique', align: 'start',sortable:true, key: 'properties.species.scientific_name'},
  {title: 'Date', align: 'center',sortable:true, key: 'properties.date'},
  {title: 'Cause', align: 'center',sortable:true, key: 'properties.death_cause.label'},
])



const mortalityStore = useMortalityStore()
const coordinatesStore = useCoordinatesStore()

const speciesList = computed(() => mortalityStore.getMortalitySpecies.map(i => {return {state: i.vernacular_name, value: i.id}}))
const observationList = computed(() => {
  return specie.value !== null ? mortalityStore.getMortalityFeatures.filter(i => i.properties?.species.id == specie.value) : mortalityStore.getMortalityFeatures
})
// const showDetail = async (item) => {
//   console.log('event', `/mortality/${item.id}`)
//   await navigateTo(`/mortality/${item.id}`)
// }

onMounted(() => {
  // setInfrstrData({})
  // mortalityStore.getMortalityData()
})

const handleRowClick = (_, object) => {
  console.log('object', object)
  console.log(object.item)
  coordinatesStore.setSelectedFeature(object.item)
}
</script>

<style>
.v-data-table /deep/ .v-data-table__wrapper {
  overflow: unset;
}
</style>