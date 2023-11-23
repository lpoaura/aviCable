<template>
  <div>
    <v-radio-group v-model="display" row density="compact">
      <v-row justify="space-around">
        <v-col><v-radio :label="$t('display.all')" value="both" /></v-col>
        <v-col><v-radio :label="$t('support.supports')" value="poles" /></v-col>
        <v-col><v-radio :label="$t('display.lines')" value="segments" /></v-col>
      </v-row>
    </v-radio-group>

    <v-data-table :headers="tableHeaders" :items="dataSource[display]" :loading="!dataSource[display]" :search="search"
      loading-text="Loading... Please wait" :items-per-page="-1" :fixed-header="true" class="elevation-1" density="compact"
      @click:row="showDetail">
      <template #item.value.properties.actions_infrastructure.0.neutralized="{ item }">
        {{ item.value }}
        <v-icon :color="[item.value?.properties.actions_infrastructure[0].neutralized] == 'true'
            ? 'green'
            : 'red'
          " dark>
          {{
          item.value?.properties.actions_infrastructure[0].neutralized
          ? 'mdi-check-circle'
          : 'mdi-checkbox-blank-circle'
          }}
        </v-icon>
      </template>
    </v-data-table>
    {{ selectedData }}
  </div>
</template>

<script setup>
// import { mapState } from 'pinia'
// import { useCablesStore } from '~/store/cablesStore'
const router = useRouter()
const { t } = useI18n()

// const singleExpand = ref(false)
// const expanded = reactive([])
const display = ref('both')
const search = ref('')
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
  { title: 'Notation', key: 'score' },
  {
    title: 'Neutralisé',
    key: 'properties.actions_infrastructure.0.neutralized'
  },
  {
    title: 'Dernier diagnostic',
    key: 'properties.actions_infrastructure.0.date'
  }
])

const cableStore = useCablesStore()
const mortalityStore = useMortalityStore()
const dataSource = computed(() => {
  return {
    both: cableStore.getInfstrDatafeatures,
    poles: cableStore.getPointDataFeatures,
    segments: cableStore.getLineDataFeatures
  }
})

onMounted(() => {
  // setInfrstrData({})
  cableStore.getInfrstrData({})
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
const showDetail = (_, {item}) => {
  const rowData = item.columns
  console.log('_, item', _, item)
  console.log('showDetail rowItem id', rowData['properties.id'])
  if (rowData.resourcetype === 'Point') {
    router.push(`/supports/${rowData['properties.id']}`)
  } else if (rowData.resourcetype === 'Line') {
    router.push(`/lines/${rowData['properties.id']}`)
  }
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