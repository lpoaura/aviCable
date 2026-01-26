<template>
  <NuxtLayout name="view">
    <template #map><map-search /></template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition du diagnostic ({{infrastructureType}} #{{ infrastructureId }})
        </v-app-bar-title>
        <v-app-bar-nav-icon>
          <v-btn density="compact" icon="mdi-close" @click="router.push(`/infrastructures/${infrastructureId}`)" />
        </v-app-bar-nav-icon>
      </v-app-bar>
      <v-main scrollable>
        <v-container>
          <form-diagnosis :diagnosis="diagnosis" :infrastructure-type="infrastructureType?.toLowerCase()" />
        </v-container>
      </v-main>
    </v-layout>
  </NuxtLayout>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
})


const cablesStore = useCablesStore()
const coordinatesStore = useCoordinatesStore()


const route = useRoute()
const router = useRouter()
const diagnosis = ref(null)
const infrastructure = ref(null)
const {formInfrastructure, formInfrastructureId }= storeToRefs(cablesStore)
const infrastructureId = computed(() => route.params.id)
const infrastructureType = ref(null)

const init = async () =>{
  console.log('diagnosis initial getData')
  const data = await api.get<Infrastructure>(`/api/v1/cables/infrastructures/${route.params.id}`);
  coordinatesStore.setSelectedFeature(data)
  infrastructureType.value = data ? data.resourcetype : route.query.type;
  formInfrastructure.value = data
  formInfrastructureId.value = data?.properties.id;
  if (route.query.id_diagnosis) {
   const data = await api.get<Diagnosis>(`/api/v1/cables/diagnosis/${route.query.id_diagnosis}`)
   diagnosis.value = data
  }
}

watch(infrastructure.value, (newVal) => {
  console.log('WATCH infrastructure.value')
  infrastructureType.value = newVal ? newVal.value.resourcetype : route.query.type;
  formInfrastructure.value = infrastructureId.value
});

onMounted(async ()=> {
  await init()
})

</script>
