<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="true" :mode="infrastructure.geometry.type" /></template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition d'une infrastructure
        </v-app-bar-title>
        <v-app-bar-nav-icon>
          <v-btn density="compact" icon="mdi-close" @click="$router.push(`/infrastructures/${infrastructureId}`)" />
        </v-app-bar-nav-icon>
      </v-app-bar>
      <v-main scrollable>
        <v-container>
          <form-infrastructure :infrastructure="infrastructure" :infrastructure-type="infrastructureType" />
        </v-container>
      </v-main>
    </v-layout>

  </NuxtLayout>
</template>



<script setup>

definePageMeta({
  auth: true,
});

const coordinatesStore=useCoordinatesStore()
const route = useRoute()
const infrastructure = ref(null)
const infrastructureId = computed(() => route.params.id)
const infrastructureType = computed(() => route.query.type)

const getData = async () =>{
  if (infrastructureId.value) {
    console.log('route.params.id',route.params.id)
    const {data: resInfrastructure} = await useHttp(`/api/v1/cables/infrastructures/${route.params.id}`)
    infrastructure.value=resInfrastructure
    console.log('getData',infrastructure.value)
    coordinatesStore.setSelectedFeature(infrastructure.value)
  }
}

onMounted(()=> {
  getData()
})

</script>
