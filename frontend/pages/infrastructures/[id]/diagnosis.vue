<template>
  <NuxtLayout name="view">
    <template #map><map-search /></template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition du diagnostic {{ infrastructure?.resourcetype }}
        </v-app-bar-title>
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

definePageMeta({
  auth: true,
});
const route = useRoute()
const diagnosis = ref(null)
const infrastructure = ref(null)
const infrastructureId = computed(() => route.params.id)
const infrastructureType = ref(null)
watch(infrastructure, (_val)=> {
  console.log('VAL', _val)
  console.log('infrastructure', infrastructure)
})

const getData = async () =>{
  if (route.query.id_diagnosis) {
   console.debug(`load Diag AdminPageComponentdata ${route.query.id_diagnosis}`)
   await useHttp(`/api/v1/cables/diagnosis/${route.query.id_diagnosis}`).then(res => diagnosis.value=res.data)
   console.debug('DIAG VALUES', diagnosis.value)
  }
  if (route.params.id) {
    console.log('route.params.id',route.params.id)
    const resInfrastructure = await useHttp(`/api/v1/cables/infrastructures/${route.params.id}`);
    infrastructure.value = resInfrastructure.data;
    console.log('infrastructure.value.resourcetype',infrastructure.value)
  }
}

watch(infrastructure, (newVal) => {
  infrastructureType.value = newVal ? newVal.value.resourcetype : route.query.type;
  cablesStore.setFormInfrastructureId(infrastructureId.value)
});

onMounted(async ()=> {
  getData()
})

</script>
