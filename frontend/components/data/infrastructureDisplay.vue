<template>
  <div>
    <v-radio-group v-model="display" row density="compact">
      <v-row justify="space-around">
        <v-col><v-radio :label="$t('display.all')" value="both" /></v-col>
        <v-col><v-radio :label="$t('support.supports')" value="poles" /></v-col>
        <v-col><v-radio :label="$t('display.lines')" value="segments" /></v-col>
      </v-row>
    </v-radio-group>
    <v-data-table v-model:expanded="expanded" :headers="tableHeaders" :items="dataSource[display]"
      item-value="properties.id" :loading="!dataSource[display]" :search="search" :loading-text="$t('common.loading')"
      :items-per-page="100" :fixed-header="true" class="elevation-1" density="compact" show-expand
      @click:row="handleRowClick">
      <template v-slot:expanded-row="{ columns, item }">
        <tr>
          <td :colspan="columns.length" height="500px">
            <v-card height="500px" width="100%" class="overflow-y-auto">
              <pre><code>{{ item }}</code></pre>
            </v-card>
            <!-- <data-diagnosis-detail :data="item"></data-diagnosis-detail> -->
          </td>
        </tr>

      </template>
      <template v-slot:item.properties.id="{ value }">
        <v-chip prepend-icon="mdi-eye-circle-outline" @click="showDetail(value)" color="primary" link>
          {{ value }}
        </v-chip>
      </template>
      <template v-slot:item.properties.actions_infrastructure.0="{ _, item }">
        <v-chip prepend-icon="mdi-circle" :color="notationValues(item).color">
          {{ notationValues(item).label }}
        </v-chip>
      </template>
      <template v-slot:item.resourcetype="{ value }">
        <v-chip>
          <v-icon :color="value =='Point' ? 'green' : 'blue'">
            {{ value =='Point' ? 'mdi-transmission-tower' : 'mdi-cable-data'}}
          </v-icon> {{ value == 'Point' ? $t('support.support') : $t('line.line')}}
        </v-chip>
      </template>
      <template v-slot:item.properties.actions_infrastructure.0.neutralized="{ value }">
        <v-chip :prepend-icon="value || value == 'true' ? 'mdi-check-circle' : 'mdi-checkbox-blank-circle-outline'"
          :color="value || value == 'true' ? 'green':'red'">
          {{ value || value == 'true' ? $t('common.yes') : $t('common.no')}}
        </v-chip>
      </template>
    </v-data-table>
  </div>
</template>

<script setup lang="ts">
// import { mapState } from 'pinia'
// import { useCablesStore } from '~/store/cablesStore'
const router = useRouter()
const { t } = useI18n()

// const singleExpand = ref(false)
// const expanded = reactive([])
const display = ref('both')
const search = ref('')
const expanded = ref([])
const selectedData = reactive([])
const tableHeaders = reactive([
  {
    title: t('app.id'),
    align: 'start',
    sortable: true,
    key: 'properties.id'
  },
  { title: t('app.type'), key: 'resourcetype' },
  { title: t('support.owner'), key: 'properties.owner.label' },
  { title: t('common.risks'), key: 'properties.actions_infrastructure.0' },
  {
    title: 'Neutralisé',
    key: 'properties.actions_infrastructure.0.neutralized'
  },
  {
    title: 'Dernier diagnostic',
    key: 'properties.actions_infrastructure.0.date'
  },
  { title: '+', key: 'data-table-expand' },
])


const coordinatesStore = useCoordinatesStore()
const cableStore = useCablesStore()
const mortalityStore = useMortalityStore()
const dataSource = computed(() => {
  return {
    both: cableStore.getInfstrDatafeatures,
    poles: cableStore.getPointDataFeatures,
    segments: cableStore.getLineDataFeatures
  }
})

const bbox : ComputedRef<string> = computed<string>(() => coordinatesStore.mapBounds)
const zoom : ComputedRef<number> = computed<number>(() => coordinatesStore.zoom)
// const bbox: ComputedRef<str> = computed<str>(() => coordinatesStore.getMapBounds);
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

onMounted(() => {
  // setInfrstrData({})
  // cableStore.getInfrstrData({})
  mortalityStore.getMortalityData()
})

// const source = (choice) => {
//   switch (choice) {
//     case 'both':
//       selectedData = infstrDataFeatures
//       break
//     case 'poles':
//       selectedData = pointDataFeatures
//       break
//     case 'segments':
//       selectedData = lineDataFeatures
//       break
//     default:
//     // TODO raise an exception and handle it or display message to user
//   }
// }
const showDetail = (_, rowItem) => {
  const data = rowItem?.item
  const id = data?.properties.id
  console.log('data', id, data)
  if (data?.resourcetype === 'Point' && id) {
    router.push(`/supports/${id}`)
  } else if (data?.resourcetype === 'Line' && id) {
    router.push(`/lines/${id}`)
  }
}

const notationValues =(item) => {
  const risks = {
    'RISK_L': {note: 1, color:'light-green', label: 'faible'},
    'RISK_M': {note: 2, color:'yellow', label: 'modéré'},
    'RISK_H': {note: 3, color:'red lighten-1 white--text', label:'fort'}
  }
  const actions_infrastructure = item.properties.actions_infrastructure[0]
  let result
  if (item.resourcetype == 'Point' && actions_infrastructure) {
    const note = risks[actions_infrastructure.pole_attractivity?.code]?.note + risks[actions_infrastructure.pole_dangerousness?.code]?.note
    result = note < 3 ? 'RISK_L' : note > 5 ? 'RISK_H' : 'RISK_M' 
  } else {
    // Manage lines risks
    result = 'RISK_L'
  }
  return  risks[result]
}

const handleRowClick = (_, object) => {
  console.log(object.item.geometry)
  coordinatesStore.setSelectedFeature(object.item)
}

// export default {
//   name: 'InfrastructureDisplay',

//   data() {
//     return {
//       singleExpand: false,
//       expanded: [],
//       display: 'both',
//       selectedData: [],
//       tableHeaders: [
//         {
//           text: this.$t('app.id'),
//           align: 'start',
//           sortable: true,
//           value: 'properties.id',
//         },
//         { text: this.$t('app.type'), value: 'resourcetype' },
//         { text: this.$t('support.owner'), value: 'properties.owner.label' },
//         { text: 'Notation', value: 'score' },
//         {
//           text: 'Neutralisé',
//           value: 'properties.actions_infrastructure.0.neutralized',
//         },
//         {
//           text: 'Dernier diagnostic',
//           value: 'properties.actions_infrastructure.0.date',
//         },toRaw
//       ],
//     }
//   },
//   async fetch() {
//     const data = await useFetch('/api/v1/cables/infrastructures') // get FeatureCollection
//     this.$store.commit('cablesStore/add', data)
//     // needed to load data at start
//     this.selectedData = this.infstrDataFeatures
//   },
//   computed: {
//     ...mapState(useCablesStore, ['infstrDataFeatures', 'pointDataFeatures', 'lineDataFeatures'])
//   },
//   methods: {
//     source(choice) {
//       switch (choice) {
//         case 'both':
//           this.selectedData = this.infstrDataFeatures
//           break
//         case 'poles':
//           this.selectedData = this.pointDataFeatures
//           break
//         case 'segments':
//           this.selectedData = this.lineDataFeatures
//           break
//         default:
//         // TODO raise an exception and handle it or display message to user
//       }
//     },
//     showDetail(evt) {
//       if (evt.resourcetype === 'Point') {
//         this.$router.push(`/supports/${evt.properties.id}`)
//       } else if (evt.resourcetype === 'Line') {
//         this.$router.push(`/lines/${evt.properties.id}`)
//       }
//     },
//   },
// }
</script>

<style>
.v-data-table /deep/ .v-data-table__wrapper {
  overflow: unset;
}
</style>