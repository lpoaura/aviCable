<template>
  <NuxtLayout name="view">
    <template #map><map-search /></template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition du diagnostic
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

<script setup>
const cablesStore = useCablesStore()
const coordinatesStore = useCoordinatesStore()

definePageMeta({
  auth: true,
});

const route = useRoute()
const router = useRouter()
const diagnosis = ref(null)
const infrastructure = ref(null)
const infrastructureId = computed(() => route.params.id)
const infrastructureType = ref(null)

const getData = async () =>{
  const {data: resInfrastructure} = await useHttp(`/api/v1/cables/infrastructures/${route.params.id}`);
  infrastructure.value = resInfrastructure;
  coordinatesStore.setSelectedFeature(infrastructure)
  if (route.query.id_diagnosis) {
   console.debug(`load Diag AdminPageComponentdata ${route.query.id_diagnosis}`)
   await useHttp(`/api/v1/cables/diagnosis/${route.query.id_diagnosis}`).then(res => diagnosis.value=res.data)
   console.debug('DIAG VALUES', diagnosis.value)
  }
}

watch(infrastructure, (newVal) => {
  infrastructureType.value = newVal ? newVal.value.resourcetype : route.query.type;
  cablesStore.setFormInfrastructureId(infrastructureId.value)
});

onMounted(()=> {
  getData()
})

</script>
