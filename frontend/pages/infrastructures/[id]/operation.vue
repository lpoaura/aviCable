<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="true" :mode="route.query.type.toLowerCase()" /></template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition d'une opération
        </v-app-bar-title>
        <v-app-bar-nav-icon>
          <v-btn density="compact" icon="mdi-close" @click="router.push(`/infrastructures/${infrastructureId}`)" />
        </v-app-bar-nav-icon>
      </v-app-bar>
      <v-main scrollable>
        <v-container>
          <form-operation />
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
const infrastructureId = computed(() => route.params.id)

onMounted(async ()=> {
  const {data: infrastructure} = await useApi(`/api/v1/cables/infrastructures/${infrastructureId.value}/`)
  cablesStore.setFormInfrastructureId(infrastructureId.value)
  cablesStore.setFormInfrastructure(infrastructure.value)
  coordinatesStore.setSelectedFeature(infrastructure.value)
})

</script>UT
