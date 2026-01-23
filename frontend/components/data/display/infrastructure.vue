<!-- Creér un option de calcul auto sur une sélection de
- poteaux: nb total vs nb équipé
- tronçons: nb total vs nb equipé
A faire sur l'interface
Dans un modal
-->
<template>
  <v-main class="fill-height">
    <v-card>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-select v-model="display" label="Type d'infrastructure"
              :items="[{ state: $t('display.all'), value: 'both' }, { state: $t('infrastructure.supports'), value: 'poles' }, { state: $t('display.lines'), value: 'segments' }]"
              item-title="state" item-value="value" variant="outlined" density="compact" />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line
              variant="outlined" hide-details density="compact" />
          </v-col>
        </v-row>

      </v-card-text>
    </v-card>
    <v-layout class="fill-height">
      <v-data-table-virtual v-model="selected" :headers="tableHeaders" :items="dataSource[display]"
        item-value="properties.id" :loading="cableStore.infstrDataLoadingStatus" :search="search"
        :loading-text="$t('loading')" :items-per-page="-1" :fixed-header="true" class="elevation-1 fill-height"
        height="200" density="compact" :row-props="colorRowItem" @click:row="handleRowClick">
        <template #item.properties.id="{ value, item }">
          <v-chip prepend-icon="mdi-eye-circle-outline" color="primary" link @click="showDetail(item)">
            {{ value }}
          </v-chip>
        </template>
        <template #item.properties.diagnosis.0="{ _, item }">
          <widgets-risk-level-status :display-mortality="true" :data="item" :detail="false" />
        </template>
        <template #item.resourcetype="{ value }">
          <v-chip :color="value == 'Point' ? 'green' : 'blue'"   variant="flat">
            <v-icon >
              {{ value == 'Point' ? 'mdi-transmission-tower' : 'mdi-cable-data' }}
            </v-icon> {{ value == 'Point' ? $t('infrastructure.support') : $t('line.line') }}
          </v-chip>
        </template>
        <template #item.properties.operations="{ _value, item }">
          <widgets-neutralized-status :data="item" :detail="false" />
        </template>
      </v-data-table-virtual>
    </v-layout>
  </v-main>
</template>

<script setup lang="ts">

import { storeToRefs } from 'pinia';

const router = useRouter()
const { t } = useI18n()

const display = ref('both')
const search = ref('')
const selected = ref([])
const tableHeaders = reactive([
  {
    title: t('app.id'),
    align: 'start',
    sortable: true,
    key: 'properties.id'
  },
  { title: t('app.type'), key: 'resourcetype' },
  { title: t('infrastructure.network_type'), key: 'properties.network_type.code' },
  { title: t('risks'), key: 'properties.diagnosis.0' },
  {
    title: 'Neutralisé',
    key: 'properties.operations'
  },
  {
    title: 'Dernier diagnostic',
    key: 'properties.diagnosis.0.date'
  },
])


const coordinatesStore = useCoordinatesStore()
const cableStore = useCablesStore()



const { infstrDatafeatures, pointData, lineStringData } = storeToRefs(cableStore)
const { selectedFeature } = storeToRefs(coordinatesStore)

const dataSource = computed(() => {
  return {
    both: infstrDatafeatures.value,
    poles: pointData.value,
    segments: lineStringData.value
  }
})


const showDetail = (rowItem) => {
  const id = rowItem?.properties.id
  if (id) {
    router.push(`/infrastructures/${id}`)
  }
}


const handleRowClick = (_, object) => {
  selectedFeature.value = object.item
}

const colorRowItem = (item) => {

  if (item.item.properties.id === selectedFeature.value?.properties.id) {
    return { class: 'bg-light-blue-lighten-5' };
  }
  return { class: "success" }
}

</script>

<style>
.v-data-table /deep/ .v-data-table__wrapper {
  overflow: unset;
}

.selected-row {
  background-color: greenyellow;
}
</style>
