<!-- Creér un option de calcul auto sur une sélection de
- poteaux: nb total vs nb équipé
- tronçons: nb total vs nb equipé
A faire sur l'interface
Dans un modal
-->
<template>
  <div>
    <v-card>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-select v-model="display" label="Type d'infrastructure"
              :items="[{state:$t('display.all') ,value:'both'}, {state:$t('support.supports'),value:'poles'},{state:$t('display.lines'),value:'segments'}]"
              item-title="state" item-value="value" variant="outlined" density="compact" />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" single-line
              variant="outlined" hide-details density="compact" />
          </v-col>
        </v-row>

      </v-card-text>
    </v-card>
    <v-data-table v-model="selected" :headers="tableHeaders" :items="dataSource[display]" item-value="properties.id"
      :loading="cableStore.infrstrDataLoadingStatus" :search="search" :loading-text="$t('loading')" :items-per-page="-1"
      :fixed-header="true" class="elevation-1" density="compact" @click:row="handleRowClick">
      <!-- <template v-slot:expanded-row="{ columns, item }">
        <tr>
          <td :colspan="columns.length" height="500px">
            <data-card-diagnosis :diagnosis="item.properties.diagnosis[0]"></data-card-diagnosis>
          </td>
        </tr>

      </template> -->

      <template #item.properties.id="{ value, item }">
        <v-chip prepend-icon="mdi-eye-circle-outline" color="primary" link @click="showDetail(item)">
          {{ value }}
        </v-chip>
      </template>
      <template #item.properties.diagnosis.0="{ _, item }">
        <v-chip prepend-icon="mdi-circle" :color="notationValues(item).color">
          {{ notationValues(item).label }}
        </v-chip>
      </template>
      <template #item.resourcetype="{ value }">
        <v-chip>
          <v-icon :color="value =='Point' ? 'green' : 'blue'">
            {{ value =='Point' ? 'mdi-transmission-tower' : 'mdi-cable-data'}}
          </v-icon> {{ value == 'Point' ? $t('support.support') : $t('line.line')}}
        </v-chip>
      </template>
      <template #item.properties.operations="{ value }">
        <v-chip :prepend-icon="value.length> 0 ? 'mdi-check-circle' : 'mdi-checkbox-blank-circle-outline'"
          :color="value.length>0 ? 'green':'red'">
          {{ value[0] ? value[0].date : $t('no')}}
        </v-chip>
      </template>
    </v-data-table>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const { t } = useI18n()

const display = ref('both')
const search = ref('')
const selected= ref([])
const tableHeaders = reactive([
  {
    title: t('app.id'),
    align: 'start',
    sortable: true,
    key: 'properties.id'
  },
  { title: t('app.type'), key: 'resourcetype' },
  { title: t('support.owner'), key: 'properties.owner.label' },
  { title: t('common.risks'), key: 'properties.diagnosis.0' },
  {
    title: 'Neutralisé',
    key: 'properties.operations'
  },
  {
    title: 'Dernier diagnostic',
    key: 'properties.diagnosis.0.date'
  },
  { title: '+', key: 'data-table-expand' },
])


const coordinatesStore = useCoordinatesStore()
const cableStore = useCablesStore()
const dataSource = computed(() => {
  return {
    both: cableStore.getInfstrDatafeatures,
    poles: cableStore.getPointDataFeatures,
    segments: cableStore.getLineDataFeatures
  }
})


const showDetail = (rowItem) => {
  const id = rowItem?.properties.id
  if (id) {
    router.push(`/infrastructures/${id}`)
  }
}

const notationValues =(item) => {
  const risks = {
    'RISK_L': {note: 1, color:'blue', label: 'faible'},
    'RISK_M': {note: 2, color:'orange', label: 'fort'},
    'RISK_H': {note: 3, color:'red lighten-1 white--text', label:'très fort'}
  }
  const diagnosis = item.properties.diagnosis[0]
  let result
  if (item.resourcetype == 'Point' && diagnosis) {
    const note = risks[diagnosis.pole_attractivity?.code]?.note + risks[diagnosis.pole_dangerousness?.code]?.note
    result = note < 3 ? 'RISK_L' : note >= 5 ? 'RISK_H' : 'RISK_M'
  } else {
    // TODO: Manage lines risks
    result = 'RISK_L'
  }
  return risks[result]
}

const handleRowClick = (_, object) => {
  console.log(object.item.geometry)
  coordinatesStore.setSelectedFeature(object.item)
}

</script>

<style>
.v-data-table /deep/ .v-data-table__wrapper {
  overflow: unset;
}
</style>
